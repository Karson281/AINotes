#!/usr/bin/env python3
"""每日股票分析 v3 — Google Finance (HK) + Alpha Vantage (US) + Framework Rules + 股息日曆"""
import asyncio, httpx, json, re, os, subprocess
from datetime import datetime, date
from pathlib import Path

# ── Config ──
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY", os.environ.get("DEEPSEEK_API_KEY", ""))
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")
WATCHLIST_FILE = "/root/vault/stock-watchlist.json"
TARGET_FOLDER = "/root/vault/02-Wiki/Stocks"

GF_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-HK,zh;q=0.9,en;q=0.8",
}

MONTHS_ZH = {
    "Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6",
    "Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"
}

# ── Helpers ──

def load_wl():
    return json.loads(Path(WATCHLIST_FILE).read_text()) if Path(WATCHLIST_FILE).exists() else []

def get_rating(text):
    """Extract rating from 【評級】 section only."""
    m = re.search(r'【評級】[：:]\s*(.+)', text)
    if m:
        section = m.group(1)
        for r in ("建倉買入", "加倉買入", "減倉賣出", "清倉賣出", "密切觀察", "觀望"):
            if r in section:
                return r
    matches = re.findall(r'(?:密切觀察|觀望|建倉買入|加倉買入|減倉賣出|清倉賣出)', text)
    return matches[-1] if matches else "觀望"

def parse_gf_date(s):
    """Parse 'Jun 11, 2026' => '2026-06-11'."""
    s = s.strip()
    try:
        for eng, num in MONTHS_ZH.items():
            s = s.replace(eng, num)
        parts = s.replace(",", "").split()
        if len(parts) == 3:
            m, d, y = parts
            return f"{y}-{int(m):02d}-{int(d):02d}"
    except:
        pass
    return None

def days_until(d_str):
    """Calculate days from today until date string."""
    try:
        target = datetime.strptime(d_str, "%Y-%m-%d").date()
        delta = (target - date.today()).days
        return delta
    except:
        return None

# ── Google Finance (HK) ──

def gf_fetch_price(ticker):
    """Fetch HK stock price + dividend data from Google Finance."""
    code = ticker.replace(".HK", "").upper()
    url = f"https://www.google.com/finance/quote/{code}:HKG"
    try:
        r = httpx.get(url, headers=GF_HEADERS, timeout=15, follow_redirects=True)
        html = r.text

        result = {"ok": False, "source": "Google Finance", "ticker": ticker}

        # Price data
        pat = (re.escape(code) + r'","HKG"\]\],null,([^,]+),"[^"]*",([^,]+),([^,]+),([^,]+),'
               r'2,([^,]+),2,([^,]+),2,"([^"]+)","' + re.escape(code) +
               r':HKG","([^"]+)",([^,]+),([^,]+),([^,]+)')
        m = re.search(pat, html)
        if m:
            result.update({
                "price": float(m.group(4)) if m.group(4) != 'null' else None,
                "change": float(m.group(5)) if m.group(5) != 'null' else None,
                "change_pct": float(m.group(6)) if m.group(6) != 'null' else None,
                "high": float(m.group(3)) if m.group(3) != 'null' else None,
                "low": float(m.group(2)) if m.group(2) != 'null' else None,
                "open": float(m.group(1)) if m.group(1) != 'null' else None,
                "prev_close": float(m.group(9)) if m.group(9) != 'null' else None,
                "volume": int(float(m.group(11))) if m.group(11) != 'null' else None,
                "market_cap": float(m.group(10)) if m.group(10) != 'null' else None,
                "currency": m.group(7),
                "name": m.group(8),
                "ok": True,
            })

        # Ex-dividend date
        em = re.search(r'Ex-dividend date[^<]*<[^>]*>[^<]*<[^>]*>([^<]+)', html)
        if em:
            result["ex_div_date"] = parse_gf_date(em.group(1))
        # Quarterly dividend amount
        qm = re.search(r'Quarterly dividend[^<]*<[^>]*>[^<]*<[^>]*>([^<]+)', html)
        if qm:
            result["div_amount"] = qm.group(1).strip()

        return result
    except Exception as e:
        return {"ok": False, "source": "Google Finance", "ticker": ticker, "error": str(e)}

# ── Alpha Vantage (US) ──

def av_fetch_price(ticker):
    """Fetch US stock data from Alpha Vantage + yfinance for dividends."""
    result = {"ok": False, "source": "Alpha Vantage", "ticker": ticker}

    # Get dividends from yfinance (fast, reliable for ex-div dates)
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        cal = stock.calendar
        if cal and isinstance(cal, dict):
            ex = cal.get('Ex-Dividend Date')
            if ex:
                if hasattr(ex, 'strftime'):
                    result["ex_div_date"] = ex.strftime("%Y-%m-%d")
                else:
                    result["ex_div_date"] = str(ex)[:10]
            dr = cal.get('Dividend Rate')
            if dr:
                result["div_amount"] = f"${dr:.2f}"
        info = stock.info
        result["dividend_yield"] = info.get('dividendYield')
        result["name"] = info.get('shortName') or info.get('longName', ticker)

        # Fallback price from yfinance if AV fails
        result["price"] = info.get("currentPrice") or info.get("regularMarketPrice")
        result["change_pct"] = info.get("regularMarketChangePercent")
        result["volume"] = info.get("regularMarketVolume")
        result["market_cap"] = info.get("marketCap")
        if result.get("price"):
            result["ok"] = True
            result["source"] = "yfinance"
    except:
        pass

    # Try Alpha Vantage for price if available
    if ALPHA_VANTAGE_KEY:
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_KEY}"
            r = httpx.get(url, timeout=10)
            q = r.json().get("Global Quote", {})
            if q and q.get("05. price"):
                result.update({
                    "price": float(q.get("05. price", 0)),
                    "change_pct": float(q.get("10. change percent", "0").replace("%", "")),
                    "volume": int(q.get("06. volume", 0)),
                    "ok": True,
                    "source": "Alpha Vantage",
                })
                url2 = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={ALPHA_VANTAGE_KEY}"
                r2 = httpx.get(url2, timeout=10)
                ov = r2.json()
                if ov and ov.get("Symbol"):
                    result["market_cap"] = float(ov.get("MarketCapitalization", 0)) if ov.get("MarketCapitalization") else result.get("market_cap")
        except:
            pass

    return result


# ── DeepSeek Analysis ──

def build_prompt(ticker, mkt):
    price_info = ""
    if mkt.get("ok"):
        div_info = ""
        if mkt.get("ex_div_date"):
            dd = days_until(mkt["ex_div_date"])
            label = "🔥 即將到來" if dd is not None and dd <= 30 else "📅 未來"
            if dd is not None and dd < 0:
                label = "⏰ 已除淨"
            div_info = f"除淨日: {mkt['ex_div_date']} ({label})\n股息金額: {mkt.get('div_amount', 'N/A')}\n"
        price_info = (
            f"\n【即時股價】（來源: {mkt['source']}）\n"
            f"現價: {mkt.get('price', 'N/A')}\n"
            f"日內波幅: {mkt.get('low', 'N/A')} - {mkt.get('high', 'N/A')}\n"
            f"變動: {mkt.get('change_pct', 'N/A')}%\n"
            f"成交量: {mkt.get('volume', 'N/A')}\n"
            f"市值: {mkt.get('market_cap', 'N/A')}\n"
            f"股息資訊:\n{div_info}"
        )
    else:
        price_info = "\n【即時股價】無法獲取\n"

    return (
        f"你是一位資深港股美股投資專家，嚴格按照以下框架進行分析。\n\n"
        f"對 {ticker} 進行分析，參考以下即時數據：\n{price_info}\n\n"
        f"【框架規則 — 嚴格遵守】\n\n"
        f"### 技術面評級標準\n"
        f"1. 強共振（建倉買入）：MA20 > MA50 > MA200 且 MA20 斜率上升\n"
        f"2. 弱共振（密切觀察）：MA20 > MA50 > MA200 但 MA20 斜率下降\n"
        f"3. 中性（觀望）：MA50 與 MA200 糾纏（差距 < 2%）\n"
        f"4. 弱死亡交叉（減倉賣出）：MA20 < MA50 且 MA50 斜率下降\n"
        f"5. 強死亡交叉（清倉賣出）：MA50 < MA200 且 MA50 月跌幅 > 5%\n"
        f"6. RSI < 30：超賣留意反彈；RSI > 70：超買警惕回調\n"
        f"7. MACD 金叉零軸上：多頭確認；MACD 死叉零軸下：空頭確認\n"
        f"8. 成交量 > 20日均量×1.5：放量確認趨勢\n\n"
        f"### 評級五選一\n- 建倉買入\n- 加倉買入\n- 減倉賣出\n- 清倉賣出\n- 觀望\n\n"
        f"【強制輸出格式】\n"
        f"【評級】：五選一\n"
        f"【技術面】：均線排列、MACD（金叉/死叉+零軸）、RSI（數值+判斷）、成交量\n"
        f"【基本面】：盈利狀況、估值分析、派息能力\n"
        f"【策略】：入場區間（基於真實價格±1%）、目標價、止損位\n"
        f"【風險提示】：宏觀因素、行業風險\n"
        f"注意：評級只能從【評級】段落提取，策略段「可轉為XX」不算。"
    )

async def analyze(ticker):
    mkt = fetch_price(ticker)
    prompt = build_prompt(ticker, mkt)

    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "用繁體中文。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2048
            }
        )
    txt = r.json()["choices"][0]["message"]["content"]
    rating = get_rating(txt)
    return {"content": txt, "rating": rating, "ticker": ticker.upper(), "market_data": mkt}


# ── Save ──

def fetch_price(ticker):
    is_hk = ticker.upper().endswith(".HK")
    result = None
    if is_hk:
        result = gf_fetch_price(ticker)
        if not result.get("ok"):
            result = yf_fetch_price(ticker)
    else:
        result = av_fetch_price(ticker)
        if not result.get("ok"):
            result = yf_fetch_price(ticker)
    if not result or not result.get("ok"):
        return {"ok": False, "ticker": ticker}
    return result

def yf_fetch_price(ticker):
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        if not price:
            return {"ok": False}
        cal = stock.calendar
        ex_div = None
        if cal and isinstance(cal, dict):
            ex = cal.get('Ex-Dividend Date')
            if ex:
                ex_div = ex.strftime("%Y-%m-%d") if hasattr(ex, 'strftime') else str(ex)[:10]
        return {
            "ok": True, "source": "yfinance fallback", "ticker": ticker,
            "price": price,
            "change_pct": info.get("regularMarketChangePercent"),
            "volume": info.get("regularMarketVolume"),
            "market_cap": info.get("marketCap"),
            "name": info.get("shortName") or info.get("longName"),
            "ex_div_date": ex_div,
        }
    except:
        return {"ok": False}

async def save(d):
    today = datetime.now()
    fn = f"{today:%Y%m%d}-{d['ticker']}.md"
    mkt = d.get("market_data", {})
    source = mkt.get("source", "N/A")

    ex_div = mkt.get("ex_div_date", "")
    div_amt = mkt.get("div_amount", "")
    div_info = ""
    if ex_div:
        dd = days_until(ex_div)
        if dd is not None:
            if dd < 0:
                div_info = f"\n\n【股息資訊】\n- 除淨日：{ex_div}（⏰ 已除淨 {abs(dd)} 天）"
            elif dd <= 30:
                div_info = f"\n\n【股息資訊】\n- 除淨日：{ex_div}（🔥 {dd} 日後除淨）"
            else:
                div_info = f"\n\n【股息資訊】\n- 除淨日：{ex_div}（📅 {dd} 日後）"
            if div_amt:
                div_info += f"\n- 股息金額：{div_amt}"

    content = (
        f"---\n"
        f"type: stock-analysis\n"
        f"ticker: {d['ticker']}\n"
        f"date: {today:%Y%m%d}\n"
        f"rating: {d['rating']}\n"
        f"ex_div_date: \"{ex_div}\"\n"
        f"div_amount: \"{div_amt}\"\n"
        f"data_source: {source}\n"
        f"status: completed\n"
        f"---\n\n"
        f"{d['content']}"
        f"{div_info}"
        f"\n\n【數據來源審計】\n"
        f"- 股價：{source}\n"
        f"- 股息日曆：{'Google Finance' if '.HK' in d['ticker'] else 'Yahoo Finance (yfinance calendar)'}\n"
    )

    Path(f"{TARGET_FOLDER}/{fn}").parent.mkdir(parents=True, exist_ok=True)
    Path(f"{TARGET_FOLDER}/{fn}").write_text(content, encoding="utf-8")
    print(f"  ✅ {d['ticker']} → {d['rating']} {div_info[:30] if div_info else ''}")


# ── Dividend Calendar Report ──

def write_dividend_calendar(results):
    today_str = datetime.now().strftime("%Y%m%d")
    rows = []
    for d in results:
        mkt = d.get("market_data", {})
        ex = mkt.get("ex_div_date", "")
        amt = mkt.get("div_amount", "")
        dd = days_until(ex) if ex else None
        if dd is None:
            continue

        if dd < 0:
            marker = "⏰"
        elif dd <= 7:
            marker = "🔥🔥"
        elif dd <= 30:
            marker = "🔥"
        elif dd <= 90:
            marker = "🟡"
        else:
            marker = "📅"

        rows.append((dd, d['ticker'], marker, ex, amt or "—", f"{dd}天"))

    rows.sort(key=lambda x: x[0])  # Sort by upcoming first

    lines = [
        "---",
        f"type: dividend-calendar",
        f"date: {today_str}",
        "status: completed",
        "---",
        "",
        f"# 📅 股息日曆 — {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "| 距除淨 | 股票 | 除淨日 | 股息金額 |",
        "|:------:|:----:|:------:|:--------:|",
    ]
    for dd, ticker, marker, ex, amt, label in rows:
        lines.append(f"| {marker} {label} | {ticker} | {ex} | {amt} |")

    lines.extend([
        "",
        "### 圖例",
        "- 🔥🔥 本週除淨",
        "- 🔥 30日內除淨",
        "- 🟡 90日內除淨",
        "- 📅 未來除淨",
        "- ⏰ 已除淨",
    ])

    Path(f"{TARGET_FOLDER}/{today_str}-股息日曆.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  📅 股息日曆已生成")


# ── Main ──

async def main():
    wl = load_wl()
    print(f"🔄 {len(wl)} 隻股票（含股息日曆）")

    results = []
    for i, t in enumerate(wl, 1):
        try:
            print(f"  [{i}/{len(wl)}] {t}...", end=" ")
            d = await analyze(t)
            await save(d)
            results.append(d)
        except Exception as e:
            print(f"❌ {t}: {str(e)[:100]}")

    # Dividend calendar
    if results:
        write_dividend_calendar(results)

    # Clean old reports
    if len(results) >= len(wl) * 0.5:
        today_str = datetime.now().strftime("%Y%m%d")
        count = 0
        for f in Path(TARGET_FOLDER).glob("*.md"):
            # Delete old dated reports (keep today only)
            if today_str not in f.name and "-" in f.name and f.name[0].isdigit():
                f.unlink()
                count += 1
            # Delete orphan files without YAML frontmatter
            elif f.is_file() and f.stat().st_size > 0:
                content = f.read_text(encoding="utf-8", errors="replace")
                if not content.startswith("---"):
                    f.unlink()
                    count += 1
                    print(f"  🗑️ 清除殘檔: {f.name}")
        print(f"  🗑️ 清理 {count} 個舊報告")

    # Git push
    try:
        subprocess.run(["git", "-C", "/root/vault", "add", "."], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", "/root/vault", "commit", "-m", f"stock daily {datetime.now():%Y%m%d}"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", "/root/vault", "push"], capture_output=True, timeout=60)
        print("✅ Git push 完成")
    except Exception as e:
        print(f"⚠️ Git: {e}")

if __name__ == "__main__":
    today = datetime.now()
    asyncio.run(main())
