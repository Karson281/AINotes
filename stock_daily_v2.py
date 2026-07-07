#!/usr/bin/env python3
"""每日股票分析 v4 — Real Technical Indicators + DeepSeek Interpretation"""
import asyncio, httpx, json, re, os, sys
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from pathlib import Path

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY", os.environ.get("DEEPSEEK_API_KEY", ""))
if not DEEPSEEK_KEY:
    # Try reading from .env
    env_path = "/root/.env"
    if os.path.exists(env_path):
        for line in open(env_path):
            if "DEEPSEEK_API_KEY" in line or "DEEPSEEK_KEY" in line:
                m = re.match(r'(?:export\s+)?(?:DEEPSEEK_API_KEY|DEEPSEEK_KEY)=["\']?([^"\'\n]+)', line)
                if m:
                    DEEPSEEK_KEY = m.group(1).strip()
                    break
WATCHLIST_FILE = "/root/vault/stock-watchlist.json"
TARGET_FOLDER = "/root/vault/02-Wiki/Stocks"

STOCKS = [
    ("0005.HK","匯豐控股","HK"), ("0006.HK","電能實業","HK"),
    ("0267.HK","中信股份","HK"), ("0270.HK","粵海投資","HK"),
    ("0363.HK","上海實業","HK"), ("0669.HK","創科實業","HK"),
    ("0823.HK","領展房產基金","HK"), ("0883.HK","中國海洋石油","HK"),
    ("0941.HK","中國移動","HK"), ("2388.HK","中銀香港","HK"),
    ("2800.HK","盈富基金","HK"), ("3466.HK","香港高息股ETF","HK"),
    ("3988.HK","中國銀行","HK"), ("6823.HK","香港電訊","HK"),
    ("JPM","摩根大通","US"), ("ABBV","艾伯維","US"),
    ("CVX","雪佛龍","US"), ("O","Realty Income","US"),
    ("VZ","Verizon","US"),
]

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else None

def calc_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast).mean()
    ema_slow = series.ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]

def fetch_technical(ticker):
    """Fetch historical data and calculate real technical indicators."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        if hist.empty or len(hist) < 200:
            hist = stock.history(period="max")
            if hist.empty or len(hist) < 200:
                return None, "Insufficient historical data"

        close = hist["Close"]
        volume = hist["Volume"]
        current = close.iloc[-1]
        prev_close = close.iloc[-2] if len(close) > 1 else current

        # Moving Averages
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]
        ma200 = close.rolling(200).mean().iloc[-1]
        ma20_slope = ((ma20 / close.rolling(20).mean().iloc[-5]) - 1) * 100 if len(close) >= 25 else 0
        ma50_slope = ((ma50 / close.rolling(50).mean().iloc[-10]) - 1) * 100 if len(close) >= 60 else 0

        # RSI
        rsi = calc_rsi(close)
        rsi_val = round(rsi, 1) if rsi else None
        rsi_signal = "超買" if rsi_val and rsi_val > 70 else ("超賣" if rsi_val and rsi_val < 30 else "中性")

        # MACD
        macd_line, signal_line, histogram = calc_macd(close)
        macd_signal = "金叉" if macd_line > signal_line else "死叉"
        macd_zero = "零軸上" if macd_line > 0 else "零軸下"

        # Volume
        avg_vol_20 = volume.rolling(20).mean().iloc[-1]
        vol_ratio = round(volume.iloc[-1] / avg_vol_20, 2) if avg_vol_20 > 0 else 1
        vol_signal = "放量" if vol_ratio > 1.5 else ("縮量" if vol_ratio < 0.7 else "正常")

        # Trend strength (distance between MAs)
        ma_arrangement = ""
        if ma20 > ma50 > ma200:
            ma_arrangement = "多頭排列 MA20>MA50>MA200"
        elif ma20 < ma50 < ma200:
            ma_arrangement = "空頭排列 MA20<MA50<MA200"
        elif ma50 > ma200 and ma20 < ma50:
            ma_arrangement = "糾纏 MA20<MA50>MA200"
        elif ma50 < ma200 and ma20 > ma50:
            ma_arrangement = "糾纏 MA20>MA50<MA200"
        else:
            ma_arrangement = "交叉排列"

        # Price change
        change_pct = round((current - prev_close) / prev_close * 100, 2)

        # Div info
        info = {}
        try:
            raw_info = stock.info
            if raw_info and isinstance(raw_info, dict):
                info = raw_info
        except:
            info = {}
        div_yield = info.get("dividendYield")
        div_yield_pct = round(div_yield * 100, 2) if div_yield else None
        try:
            cal = stock.calendar
            ex_div = cal.get("Ex-Dividend Date") if cal and isinstance(cal, dict) else None
        except:
            ex_div = None
        ex_div_str = ex_div.strftime("%Y-%m-%d") if hasattr(ex_div, "strftime") else (str(ex_div)[:10] if ex_div else "")
        name = info.get("shortName") or info.get("longName") or ticker

        return {
            "name": name,
            "ticker": ticker,
            "price": round(current, 3),
            "prev_close": round(prev_close, 3),
            "change_pct": change_pct,
            "ma20": round(ma20, 3),
            "ma50": round(ma50, 3),
            "ma200": round(ma200, 3),
            "ma20_slope": round(ma20_slope, 2),
            "ma50_slope": round(ma50_slope, 2),
            "ma_arrangement": ma_arrangement,
            "rsi": rsi_val,
            "rsi_signal": rsi_signal,
            "macd_line": round(macd_line, 4),
            "signal_line": round(signal_line, 4),
            "macd_histogram": round(histogram, 4),
            "macd_signal": macd_signal,
            "macd_zero": macd_zero,
            "volume": int(volume.iloc[-1]),
            "avg_vol_20": int(avg_vol_20),
            "vol_ratio": vol_ratio,
            "vol_signal": vol_signal,
            "div_yield_pct": div_yield_pct,
            "ex_div_date": ex_div_str,
            "52w_high": round(info.get("fiftyTwoWeekHigh", close.max()), 2) if not pd.isna(close.max()) else None,
            "52w_low": round(info.get("fiftyTwoWeekLow", close.min()), 2) if not pd.isna(close.min()) else None,
            "market_cap": info.get("marketCap"),
        }, None
    except Exception as e:
        return None, str(e)

def build_prompt(t):
    """Build prompt with REAL technical indicators for DeepSeek."""
    div_info = ""
    if t["ex_div_date"]:
        dd = (datetime.strptime(t["ex_div_date"], "%Y-%m-%d").date() - date.today()).days
        if dd >= 0 and dd <= 30:
            div_info = f"\n🔥 {dd}日後除淨"
        elif dd >= 0:
            div_info = f"\n📅 {dd}日後除淨"
        else:
            div_info = f"\n⏰ 已除淨 {abs(dd)}天"
    if t["div_yield_pct"]:
        div_info += f"\n股息率: {t['div_yield_pct']}%"

    risk_items = []
    if t["ex_div_date"] and "已除" not in div_info:
        risk_items.append("除息壓力")
    risk_items.append("宏觀風險")
    risk_str = " + ".join(risk_items)

    return f"""你是一位資深港股美股投資專家，基於以下真實技術指標進行分析。

【{t['ticker']} {t['name']} — 即時技術數據】

📊 價格
現價: ${t['price']} | 變動: {t['change_pct']}% | 前收: ${t['prev_close']}
52W範圍: ${t['52w_low']} - ${t['52w_high']}
市值: {'${:,}'.format(t['market_cap']) if t['market_cap'] else 'N/A'}

📈 均線
{t['ma_arrangement']}
MA20: ${t['ma20']} (斜率: {t['ma20_slope']}%/月)
MA50: ${t['ma50']} (斜率: {t['ma50_slope']}%/月)
MA200: ${t['ma200']}

🔧 動量
RSI(14): {t['rsi']} ({t['rsi_signal']})
MACD: {t['macd_signal']} {t['macd_zero']} | 柱: {t['macd_histogram']}
成交量: {t['volume']:,} | 20日均量: {t['avg_vol_20']:,} | 比: {t['vol_ratio']}x ({t['vol_signal']}){div_info}

【分析要求】
1. 趨勢判斷：基於均線排列及斜率，判斷當前趨勢方向
2. 動能分析：RSI 位置 + MACD 信號，判斷短期動能
3. 成交量驗證：放量/縮量是否支持當前趨勢
4. 關鍵價位：計算真實支撐位（前低/MA50/MA200）和阻力位（前高/MA20）
5. 除息影響：如有即將除淨，分析價格調整預期

【強制輸出格式 — 嚴格遵守】
評級：五選一（建倉買入/加倉買入/密切觀察/觀望/減倉賣出/清倉賣出）
技術面：趨勢判斷 + RSI({t['rsi']}) + MACD({t['macd_signal']}) + 成交量({t['vol_signal']})
關鍵價位：支撐 $X.XX-$X.XX | 阻力 $X.XX-$X.XX
策略：具體入場區間（基於支撐位±1%）/ 目標價 / 止損位
風險提示：{risk_str}

注意：所有價位必須基於以上真實數據推算，不能憑空猜測。"""

async def deepseek_analyze(t, prompt):
    async with httpx.AsyncClient(timeout=120) as c:
        try:
            r = await c.post(
                "https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是資深投資專家。用繁體中文。根據提供的真實技術指標進行分析，給出精確價位和可執行建議。"},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2048
                }
            )
            data = r.json()
            txt = data["choices"][0]["message"]["content"]
            rating = extract_rating(txt)
            return {"content": txt, "rating": rating, "tech": t}
        except Exception as e:
            return {"content": f"Error: {e}", "rating": "觀望", "tech": t}

def extract_rating(text):
    m = re.search(r'【評級】[：:]\s*(.+)', text)
    if m:
        section = m.group(1)
        for r in ("建倉買入","加倉買入","減倉賣出","清倉賣出","密切觀察","觀望"):
            if r in section:
                return r
    matches = re.findall(r'(建倉買入|加倉買入|減倉賣出|清倉賣出|密切觀察|觀望)', text)
    return matches[-1] if matches else "觀望"

def save_report(d):
    today = datetime.now()
    t = d["tech"]
    fn = f"{today:%Y%m%d}-{t['ticker']}.md"
    
    ticker = t['ticker']
    content = f"""---
ticker: {ticker}
name: {t['name']}
date: {today:%Y%m%d}
type: stock-analysis
rating: {d['rating']}
price: {t['price']}
change_pct: {t['change_pct']}
ma20: {t['ma20']}
ma50: {t['ma50']}
ma200: {t['ma200']}
rsi: {t['rsi']}
macd: {t['macd_signal']}
status: completed
dividend_yield: {t['div_yield_pct']}
ex_div_date: {t['ex_div_date']}
---

# {ticker} {t['name']} — {today:%Y-%m-%d}

## 技術指標
| 指標 | 數值 |
|------|:----:|
| 現價 | ${t['price']} ({t['change_pct']:+.2f}%) |
| MA20 | ${t['ma20']} |
| MA50 | ${t['ma50']} |
| MA200 | ${t['ma200']} |
| 均線排列 | {t['ma_arrangement']} |
| RSI(14) | {t['rsi']} ({t['rsi_signal']}) |
| MACD | {t['macd_signal']} {t['macd_zero']} |
| 成交量比 | {t['vol_ratio']}x ({t['vol_signal']}) |
| 股息率 | {t['div_yield_pct']}%{' ' + div_info if d.get('div_info') else ''} |

## AI 分析
{d['content']}

---
*數據來源：Yahoo Finance | DeepSeek AI 分析*
"""

    # Also collect for summary
    d["content"] = d["content"][:200]

    Path(TARGET_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(TARGET_FOLDER, fn).write_text(content, encoding="utf-8")

async def main():
    print(f"🔄 {len(STOCKS)} 隻股票分析開始\n")
    results = []
    ratings_count = {}
    div_alerts = []

    for idx, (ticker, name, market) in enumerate(STOCKS, 1):
        print(f"  [{idx}/{len(STOCKS)}] {ticker} {name}...", end=" ", flush=True)
        
        tech, err = fetch_technical(ticker)
        if err or not tech:
            print(f"❌ {err or 'No data'}")
            continue
        
        prompt = build_prompt(tech)
        d = await deepseek_analyze(tech, prompt)
        save_report(d)
        
        ratings_count[d["rating"]] = ratings_count.get(d["rating"], 0) + 1
        
        if tech["ex_div_date"]:
            dd = (datetime.strptime(tech["ex_div_date"], "%Y-%m-%d").date() - date.today()).days
            if dd >= 0 and dd <= 30:
                div_alerts.append((tech["ex_div_date"], dd, ticker, name))
        
        print(f"✅ → {d['rating']}")
        await asyncio.sleep(0.3)  # rate limit

    # Save summary
    save_summary(results, ratings_count, div_alerts)
    
    # Git push
    try:
        import subprocess
        subprocess.run(["git", "-C", "/root/vault", "add", "."], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", "/root/vault", "commit", "-m", f"stock daily {datetime.now():%Y%m%d} v4"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", "/root/vault", "push"], capture_output=True, timeout=60)
        print("\n✅ Git push 完成")
    except Exception as e:
        print(f"\n⚠️ Git: {e}")

def save_summary(results, ratings_count, div_alerts):
    today = datetime.now()
    rating_order = ["建倉買入","加倉買入","密切觀察","觀望","減倉賣出","清倉賣出"]
    
    summary = f"""---
type: portfolio-summary
date: {today:%Y%m%d}
status: completed
---

# 📊 投資組合總覽 — {today:%Y-%m-%d}

## 評級分佈
| 評級 | 數量 |
|------|:----:|
"""
    for r in rating_order:
        count = ratings_count.get(r, 0)
        summary += f"| {'🟢' if '買入' in r else '🟡' if '觀察' in r or '觀望' in r else '🔴'} {r} | {count} |\n"
    
    if div_alerts:
        summary += "\n## 📅 即將除淨\n"
        for ex_dt, dd, ticker, name in sorted(div_alerts, key=lambda x: x[1]):
            emoji = "🔥🔥" if dd <= 7 else "🔥" if dd <= 30 else "📅"
            summary += f"- {emoji} **{ticker}** {name} — {ex_dt}（{dd}天後）\n"
    
    Path(TARGET_FOLDER, f"{today:%Y%m%d}-股票分析摘要.md").write_text(summary, encoding="utf-8")

if __name__ == "__main__":
    asyncio.run(main())
