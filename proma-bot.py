from dotenv import load_dotenv
load_dotenv("/root/.env")
import os, json, asyncio, re
from datetime import datetime, time
from pathlib import Path
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue

try:
    from google_services import GoogleServices
    google = GoogleServices()
except ImportError:
    google = None

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY", os.getenv("DEEPSEEK_API_KEY"))
OBSIDIAN_AUTH = os.getenv("OBSIDIAN_AUTH", "Bearer proma-secret-2026")
WATCHLIST = [
    "0005.HK","0006.HK","0267.HK","0270.HK","0363.HK",
    "0823.HK","0941.HK","2388.HK","2638.HK","2800.HK",
    "3466.HK","3988.HK","6823.HK",
    "JPM","ABBV","CVX","O","VZ"
]
WL_PATH = Path("/root/vault/stock-watchlist.json")
CID_PATH = Path("/root/bot-chat-ids.json")
# Unicode ratings to avoid encoding issues
BUY = "建倉買入"
ADD = "加倉買入"
SELL = "減倉賣出"
CLEAR = "清倉賣出"
WATCH = "密切觀察"
NEUTRAL = "觀望"
RATINGS = [BUY, ADD, SELL, CLEAR, WATCH, NEUTRAL]
NEUTRAL_MAP = {
    "中性": WATCH,
    "中立": WATCH,
    "持有": WATCH,
}

def load_wl():
    if WL_PATH.exists():
        return json.loads(WL_PATH.read_text("utf-8"))
    save_wl(WATCHLIST)
    return WATCHLIST

def save_wl(s):
    WL_PATH.parent.mkdir(parents=True, exist_ok=True)
    WL_PATH.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")

def load_cids():
    return json.loads(CID_PATH.read_text("utf-8")) if CID_PATH.exists() else []

def save_cid(c):
    ids = load_cids()
    if c not in ids:
        ids.append(c)
        CID_PATH.write_text(json.dumps(ids), encoding="utf-8")

async def obs_up():
    try:
        async with httpx.AsyncClient(verify=False, timeout=5) as c:
            return (await c.get("http://100.98.113.30:8766/health")).status_code == 200
    except:
        return False

async def write_obs(d):
    if not await obs_up():
        return None
    fn = f"{datetime.now():%Y%m%d}-{d['ticker']}.md"
    fp = f"02-Wiki/Stocks/{fn}"
    fm = (
        f"---\ntype: stock-analysis\nticker: {d['ticker']}\n"
        f"date: {datetime.now():%Y-%m-%d}\nrating: {d['rating']}\n---\n\n"
    )
    async with httpx.AsyncClient(timeout=30) as c:
        await c.put(
            f"http://100.98.113.30:8766/obsidian/vault/{fp}",
            headers={"Authorization": OBSIDIAN_AUTH, "Content-Type": "application/json"},
            json={"content": fm + d["content"]},
        )
    # Also save locally to VPS vault
    try:
        lp = Path(f"/root/vault/02-Wiki/Stocks/{d['ticker']}.md")
        lp.parent.mkdir(parents=True, exist_ok=True)
        lp.write_text(d["content"], encoding="utf-8")
    except:
        pass
    return fp

def get_rating(t):
    for w, m in NEUTRAL_MAP.items():
        if w in t:
            return m
    for r in RATINGS:
        if r in t:
            return r
    return NEUTRAL

PROMPT = (
    "你是資深股票分析師。"
    "對 {t} 分析：\n"
    "【評級】：建倉買入/加倉買入/"
    "減倉賣出/清倉賣出/密切觀察/觀望"
    "\n【技術面】\n【基本面】\n【策略】"
)

async def analyze(ticker):
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "用繁體中文。"},
                    {"role": "user", "content": PROMPT.format(t=ticker)},
                ],
                "max_tokens": 2048,
            },
        )
    r.raise_for_status()
    txt = r.json()["choices"][0]["message"]["content"]
    return {"content": txt, "rating": get_rating(txt), "ticker": ticker.upper()}

async def cmd_start(u, c):
    save_cid(u.effective_chat.id)
    gs = google.status() if google else "Google not installed"
    lines = [
        "Proma Stock Bot v2",
        "",
        "Stock:",
        "/stocks",
        "/stocks add TICKER",
        "/stocks remove TICKER",
        "/analyze",
        "分析 0941.HK",
        "",
        "Google:",
        "/gmail /calendar /sheets /docs /drive /maps /mystatus",
        "",
        gs,
    ]
    await u.message.reply_text("\n".join(lines))

async def cmd_stocks(u, c):
    wl = load_wl()
    args = c.args
    if not args:
        msg = [f"Watchlist ({len(wl)}):"]
        for s in wl:
            msg.append(f"  {s}")
        await u.message.reply_text("\n".join(msg))
        return
    cmd = args[0].lower()
    if cmd == "add" and len(args) >= 2:
        t = args[1].upper()
        if t not in wl:
            wl.append(t)
            save_wl(wl)
            await u.message.reply_text(f"Added {t}")
        else:
            await u.message.reply_text(f"{t} already in list")
    elif cmd == "remove" and len(args) >= 2:
        t = args[1].upper()
        if t in wl:
            wl.remove(t)
            save_wl(wl)
            await u.message.reply_text(f"Removed {t}")
        else:
            await u.message.reply_text(f"{t} not found")

async def cmd_analyze(u, c):
    wl = load_wl()
    if not wl:
        await u.message.reply_text("Watchlist empty")
        return
    msg = await u.message.reply_text(f"Analyzing {len(wl)} stocks...")
    results = []
    for i, t in enumerate(wl):
        try:
            await msg.edit_text(f"({i+1}/{len(wl)}) {t}")
            d = await analyze(t)
            await write_obs(d)
            results.append(d)
            tk = "YES" if d["rating"] in (BUY, ADD) else "no"
            await u.message.reply_text(f"{tk} {d['ticker']} - {d['rating']}")
        except Exception as e:
            await u.message.reply_text(f"ERR {t}: {str(e)[:100]}")
    buy = [r for r in results if r.get("rating") in (BUY, ADD)]
    wat = [r for r in results if r.get("rating") == WATCH]
    sel = [r for r in results if r.get("rating") in (SELL, CLEAR)]
    neu = [r for r in results if r.get("rating") == NEUTRAL]
    parts = [f"Done {len(results)}/{len(wl)}", ""]
    parts.append(f"Buy({len(buy)}): {','.join(r['ticker'] for r in buy) or 'none'}")
    parts.append(f"Watch({len(wat)}): {','.join(r['ticker'] for r in wat) or 'none'}")
    parts.append(f"Sell({len(sel)}): {','.join(r['ticker'] for r in sel) or 'none'}")
    parts.append(f"Neutral({len(neu)}): {','.join(r['ticker'] for r in neu) or 'none'}")
    await u.message.reply_text("\n".join(parts))

async def daily_job(c):
    wl = load_wl()
    cids = load_cids()
    if not wl or not cids:
        return
    print(f"[DAILY] {len(wl)} stocks -> {len(cids)} chats")
    results = []
    for t in wl:
        try:
            d = await analyze(t)
            await write_obs(d)
            results.append(d)
        except Exception as e:
            results.append({"ticker": t, "rating": "ERR", "content": str(e)[:100]})
    buy = [r for r in results if r.get("rating") in (BUY, ADD)]
    wat = [r for r in results if r.get("rating") == WATCH]
    lines = ["Daily 18:00 HKT", ""]
    lines.append(f"Buy({len(buy)}): {','.join(r['ticker'] for r in buy) or 'none'}")
    lines.append(f"Watch({len(wat)}): {','.join(r['ticker'] for r in wat) or 'none'}")
    for cid in cids:
        try:
            await c.bot.send_message(chat_id=cid, text="\n".join(lines))
        except Exception as e:
            print(f"[DAILY] Failed {cid}: {e}")
    print(f"[DAILY] Done {len(results)}")

async def cmd_gmail(u, c):
    if not google:
        await u.message.reply_text("Google not installed")
        return
    args = c.args
    if args and args[0].lower() == "read" and len(args) >= 2:
        try:
            idx = int(args[1]) - 1
            emails = google.gmail_unread(10)
            if 0 <= idx < len(emails):
                body = google.gmail_read(emails[idx]["id"])
                msg = (
                    f"{emails[idx]['subject']}\n"
                    f"From: {emails[idx]['from']}\n\n"
                    f"{body or '(empty)'}"
                )
                await u.message.reply_text(msg)
            else:
                await u.message.reply_text("Invalid number")
        except Exception:
            await u.message.reply_text("Usage: /gmail read N")
        return
    emails = google.gmail_unread(8)
    if not emails:
        await u.message.reply_text("No unread")
        return
    lines = [f"Unread ({len(emails)})"]
    for i, e in enumerate(emails, 1):
        frm = e["from"].split("<")[0]
        lines.append(f"{i}. {frm} - {e['subject'][:40]}")
    await u.message.reply_text("\n".join(lines))

async def cmd_calendar(u, c):
    if not google:
        await u.message.reply_text("Google not installed")
        return
    args = c.args
    if args and args[0].lower() == "week":
        evts = google.calendar_week()
        ttl = "Next 7 days"
    else:
        evts = google.calendar_today()
        ttl = "Today"
    if not evts:
        await u.message.reply_text(f"{ttl}: none")
        return
    lines = [ttl]
    for e in evts:
        lines.append(f"  {e['start']} - {e['summary'][:50]}")
    await u.message.reply_text("\n".join(lines))

async def cmd_drive(u, c):
    if not google:
        await u.message.reply_text("Google not installed")
        return
    q = " ".join(c.args) if c.args else ""
    if q:
        rs = google.drive_search(q)
        if not rs:
            await u.message.reply_text("No results")
            return
        lines = [f"Search: {q}"]
        for f in rs:
            lines.append(f"  {f['name']} ({f['type']})")
        await u.message.reply_text("\n".join(lines))
        return
    fs = google.drive_list()
    if not fs:
        await u.message.reply_text("Empty")
        return
    lines = ["Recent files"]
    for f in fs[:10]:
        lines.append(f"  {f['name']} ({f['type']}, {f['modified']})")
    await u.message.reply_text("\n".join(lines))

async def cmd_maps(u, c):
    if not google:
        await u.message.reply_text("Google not installed")
        return
    q = " ".join(c.args) if c.args else ""
    if not q:
        await u.message.reply_text("Usage: /maps keyword")
        return
    await u.message.reply_text(f"Searching: {q}")
    lat = lng = None
    if u.message.location:
        lat = u.message.location.latitude
        lng = u.message.location.longitude
    rs = google.maps_search(q, lat, lng)
    if not rs:
        await u.message.reply_text("No results")
        return
    lines = [f"Places: {q}"]
    for r in rs[:5]:
        lines.append(f"  {r['name']}")
        lines.append(f"  {r['address']}")
        lines.append(f"  {r['maps_url']}")
    await u.message.reply_text("\n".join(lines))

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).job_queue(JobQueue()).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("stocks", cmd_stocks))
    app.add_handler(CommandHandler("analyze", cmd_analyze))
    app.add_handler(CommandHandler("gmail", cmd_gmail))
    app.add_handler(CommandHandler("calendar", cmd_calendar))
    app.add_handler(CommandHandler("drive", cmd_drive))
    app.add_handler(CommandHandler("maps", cmd_maps))
    app.job_queue.run_daily(
        daily_job,
        time=time(hour=10, minute=0),
        days=tuple(range(7)),
    )
    print("[SCHEDULER] Daily 18:00 HKT set")
    print("[START] Proma Bot v2 running with .env")
    app.run_polling()

if __name__ == "__main__":
    main()
