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
    "你是一位資深港股美股投資專家。"
    "對 {t} 進行分析，輸出以下格式：\n\n"
    "【評級】：建倉買入/加倉買入/減倉賣出/清倉賣出/密切觀察/觀望（不可用「中性」）\n"
    "【技術面】：均線狀態、MACD、RSI、成交量\n"
    "【基本面】：盈利狀況、估值水平、股息率\n"
    "【策略】：入場區間、目標價、止損位（如適用）\n\n"
    "分析必須基於真實數據，包含具體價位。"
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
        "🤖 Proma Stock Bot v2 — 24/7 VPS",
        "",
        "📈 股票分析",
        "/stocks — 睇 watchlist",
        "/stocks add TICKER — 加入",
        "/stocks remove TICKER — 移除",
        "/analyze — 分析 watchlist 全部",
        "分析 0941.HK — 分析單隻",
        "",
        "⏰ 每日 18:00 自動分析（HKT）",
        "",
        "🔌 Google 服務",
        "/gmail /calendar /docs /drive /maps /mystatus",
        "",
        gs,
    ]
    await u.message.reply_text("\n".join(lines))

async def cmd_stocks(u, c):
    wl = load_wl()
    args = c.args
    if not args:
        msg = [f"📋 Watchlist ({len(wl)} 隻):"]
        for s in wl:
            msg.append(f"  • {s}")
        await u.message.reply_text("\n".join(msg))
        return
    cmd = args[0].lower()
    if cmd == "add" and len(args) >= 2:
        t = args[1].upper()
        if t not in wl:
            wl.append(t)
            save_wl(wl)
            await u.message.reply_text(f"✅ 已加入 {t} 至 watchlist")
        else:
            await u.message.reply_text(f"⚠️ {t} 已在 watchlist 中")
    elif cmd == "remove" and len(args) >= 2:
        t = args[1].upper()
        if t in wl:
            wl.remove(t)
            save_wl(wl)
            await u.message.reply_text(f"✅ 已從 watchlist 移除 {t}")
        else:
            await u.message.reply_text(f"⚠️ {t} 唔喺 watchlist 入面")

async def cmd_analyze(u, c):
    wl = load_wl()
    if not wl:
        await u.message.reply_text("Watchlist empty")
        return
    await msg.edit_text(f"🔄 開始批量分析 {len(wl)} 隻股票...\n（每隻約需 30-60 秒）")
    results = []
    for i, t in enumerate(wl):
        try:
            await msg.edit_text(f"🔄 分析中 ({i+1}/{len(wl)}): {t}")
            d = await analyze(t)
            op = await write_obs(d)
            results.append(d)
            tk = "✅" if d["rating"] in (BUY, ADD) else "◽"
            sync_info = f" | Obsidian: {op}" if op else ""
            await u.message.reply_text(f"{tk} {d['ticker']} — {d['rating']}{sync_info}")
        except Exception as e:
            await u.message.reply_text(f"❌ {t} 分析失敗：{str(e)[:150]}")
    buy = [r for r in results if r.get("rating") in (BUY, ADD)]
    wat = [r for r in results if r.get("rating") == WATCH]
    sel = [r for r in results if r.get("rating") in (SELL, CLEAR)]
    neu = [r for r in results if r.get("rating") == NEUTRAL]
    parts = [f"📊 批量分析完成 ({len(results)}/{len(wl)})", ""]
    parts.append(f"🟢 建倉/加倉 ({len(buy)}): {','.join(r['ticker'] for r in buy) or '無'}")
    parts.append(f"🟡 密切觀察 ({len(wat)}): {','.join(r['ticker'] for r in wat) or '無'}")
    parts.append(f"🔴 減倉/清倉 ({len(sel)}): {','.join(r['ticker'] for r in sel) or '無'}")
    parts.append(f"⚪ 觀望 ({len(neu)}): {','.join(r['ticker'] for r in neu) or '無'}")
    await u.message.reply_text("\n".join(parts))
    # Auto git push after manual analyze too
    try:
        import subprocess
        subprocess.run(["git", "-C", "/root/vault", "add", "."], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", "/root/vault", "commit", "-m", f"manual analyze {datetime.now():%Y-%m-%d %H:%M}"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", "/root/vault", "push"], capture_output=True, timeout=60)
    except:
        pass

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
    sel = [r for r in results if r.get("rating") in (SELL, CLEAR)]
    neu = [r for r in results if r.get("rating") == NEUTRAL]
    lines = ["📊 每日分析完成 (18:00 HKT)", ""]
    lines.append(f"🟢 建倉/加倉 ({len(buy)}): {','.join(r['ticker'] for r in buy) or '無'}")
    lines.append(f"🟡 密切觀察 ({len(wat)}): {','.join(r['ticker'] for r in wat) or '無'}")
    lines.append(f"🔴 減倉/清倉 ({len(sel)}): {','.join(r['ticker'] for r in sel) or '無'}")
    lines.append(f"⚪ 觀望 ({len(neu)}): {','.join(r['ticker'] for r in neu) or '無'}")
    if buy:
        picks = "\n".join([f"✅ {r['ticker']} — {r['rating']}" for r in buy[:5]])
        lines.append(f"\n🌟 重點關注\n{picks}")
    for cid in cids:
        try:
            await c.bot.send_message(chat_id=cid, text="\n".join(lines))
        except Exception as e:
            print(f"[DAILY] Failed {cid}: {e}")
    print(f"[DAILY] Done {len(results)}")
    # Auto git push
    try:
        import subprocess
        subprocess.run(["git", "-C", "/root/vault", "add", "."], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", "/root/vault", "commit", "-m", f"daily update {datetime.now():%Y-%m-%d}"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", "/root/vault", "push"], capture_output=True, timeout=60)
        print(f"[GIT] Pushed {len(results)} reports to GitHub")
    except Exception as e:
        print(f"[GIT] Sync skipped: {e}")

async def cmd_analyze_single(u, c):
    """Handle single stock analysis via '分析 0941.HK' text input"""
    text = u.message.text.strip().upper()
    ticker = re.sub(r'^(分析|/STOCK)\s*', '', text).strip()
    if not ticker or len(ticker) < 1:
        await u.message.reply_text("請輸入股票代號，例如：分析 0941.HK")
        return
    await u.message.reply_text(f"🔍 分析 {ticker}，請稍候...")
    try:
        d = await analyze(ticker)
        op = await write_obs(d)
        msg = f"✅ {d['ticker']}\n評級：{d['rating']}"
        if op:
            msg += f"\n📂 {op}"
        else:
            msg += "\n⚠️ Windows 未開機，報告僅存 VPS"
        await u.message.reply_text(msg)
        full = d["content"]
        if len(full) > 4000:
            full = full[:4000] + "\n\n...(truncated)"
        await u.message.reply_text(full)
    except Exception as e:
        await u.message.reply_text(f"❌ 分析失敗：{str(e)[:200]}")

async def cmd_gmail(u, c):
    if not google:
        await u.message.reply_text("❌ Google 模組未安裝")
        return
    args = c.args
    if args and args[0].lower() == "read" and len(args) >= 2:
        try:
            idx = int(args[1]) - 1
            emails = google.gmail_unread(10)
            if 0 <= idx < len(emails):
                body = google.gmail_read(emails[idx]["id"])
                msg = (
                    f"📧 {emails[idx]['subject']}\n"
                    f"From: {emails[idx]['from']}\n\n"
                    f"{body or '(empty)'}"
                )
                await u.message.reply_text(msg)
            else:
                await u.message.reply_text("❌ 無效序號")
        except Exception:
            await u.message.reply_text("用法: /gmail read N")
        return
    emails = google.gmail_unread(8)
    if not emails:
        await u.message.reply_text("📧 無未讀郵件")
        return
    lines = [f"📧 未讀郵件 ({len(emails)})"]
    for i, e in enumerate(emails, 1):
        frm = e["from"].split("<")[0]
        lines.append(f"{i}. {frm} - {e['subject'][:40]}")
    await u.message.reply_text("\n".join(lines))

async def cmd_calendar(u, c):
    if not google:
        await u.message.reply_text("❌ Google 模組未安裝")
        return
    args = c.args
    if args and args[0].lower() == "week":
        evts = google.calendar_week()
        ttl = "📅 未來 7 日行程"
    else:
        evts = google.calendar_today()
        ttl = "📅 今日行程"
    if not evts:
        await u.message.reply_text(f"{ttl}\n（無行程）")
        return
    lines = [ttl]
    for e in evts:
        lines.append(f"• {e['start']} — {e['summary'][:50]}")
    await u.message.reply_text("\n".join(lines))

async def cmd_drive(u, c):
    if not google:
        await u.message.reply_text("❌ Google 模組未安裝")
        return
    q = " ".join(c.args) if c.args else ""
    if q:
        rs = google.drive_search(q)
        if not rs:
            await u.message.reply_text(f"🔍 搜尋「{q}」無結果")
            return
        lines = [f"🔍 Drive 搜尋: {q}"]
        for f in rs:
            lines.append(f"• {f['name']} ({f['type']})")
        await u.message.reply_text("\n".join(lines))
        return
    fs = google.drive_list()
    if not fs:
        await u.message.reply_text("📁 無最近檔案")
        return
    lines = ["📁 最近 Drive 檔案"]
    for f in fs[:10]:
        lines.append(f"• {f['name']} ({f['type']}, {f['modified']})")
    await u.message.reply_text("\n".join(lines))

async def cmd_maps(u, c):
    if not google:
        await u.message.reply_text("❌ Google 模組未安裝")
        return
    q = " ".join(c.args) if c.args else ""
    if not q:
        await u.message.reply_text("🔍 用法: /maps 關鍵字\n例: /maps 中環咖啡")
        return
    await u.message.reply_text(f"🔍 搜尋: {q}")
    lat = lng = None
    if u.message.location:
        lat = u.message.location.latitude
        lng = u.message.location.longitude
    rs = google.maps_search(q, lat, lng)
    if not rs:
        await u.message.reply_text("❌ 無結果")
        return
    lines = [f"📍 搜尋結果: {q}"]
    for r in rs[:5]:
        stars = "⭐" * max(1, round(float(r['rating']))) if r['rating'] != 'N/A' else ""
        lines.append(f"• **{r['name']}** {stars}")
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
    # Single stock analysis via text: "分析 0941.HK"
    app.add_handler(MessageHandler(filters.Regex(r'^分析\s+'), cmd_analyze_single))
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
