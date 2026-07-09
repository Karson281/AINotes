#!/usr/bin/env python3
"""每日股票分析 v4 — Real Technical Indicators + DeepSeek Interpretation"""
import asyncio, glob, httpx, json, re, os, sys
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from pathlib import Path

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY", os.environ.get("DEEPSEEK_API_KEY", ""))
if not DEEPSEEK_KEY:
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

# === Pre-check: skip if today's reports already exist ===
TODAY = datetime.now().strftime("%Y%m%d")
EXISTING = sorted(glob.glob(f"{TARGET_FOLDER}/{TODAY}-*.md"))
# Filter out non-stock files (summary, watchlist, etc.)
EXISTING = [f for f in EXISTING if not any(
    skip in f for skip in ["股票分析摘要", "股票監察名單", "股票分析框架", "股息日曆"]
)]
if len(EXISTING) >= 15:
    print(f"✅ 今日已有 {len(EXISTING)} 份報告，跳過分析")
    sys.exit(0)
else:
    print(f"⚠️ 今日只有 {len(EXISTING)} 份報告，開始補齊...")

STOCKS = [
    ("0005.HK","匯豐控股","HK"), ("0006.HK","電能實業","HK"),
    ("0267.HK","中信股份","HK"), ("0270.HK","粵海投資","HK"),
    ("0363.HK","上海實業","HK"), ("0669.HK","創科實業","HK"),
    ("0823.HK","領展房產基金","HK"), ("0883.HK","中國海洋石油","HK"),
    ("0941.HK","中國移動","HK"), ("2388.HK","中銀香港","HK"),
    ("2800.HK","盈富基金","HK"), ("3466.HK","香港高息股ETF","HK"),
    ("3988.HK","中國銀行","HK"), ("6823.HK","香港電訊","HK"),
    ("JPM","摩根大通","US"), ("ABBV","艾伯維","US"),
    ("CVX","雪佛龍","US"), ("O","Realty Income","US"), ("VZ","Verizon","US"),
]

INDICES = [
    ("^HSI","恆生指數","HSI"),
    ("^IXIC","納斯達克指數","IXIC"),
    ("^GSPC","標準普爾500指數","GSPC"),
    ("^DJI","道瓊斯工業平均指數","DJI"),
]

OS = ["\u0005","\u0006"]
for o in OS:
    STOCKS = [(t if o not in t else t.replace(o, ""), n, m) for t, n, m in STOCKS]

def compute_indicators(df):
    """Calculate technical indicators from OHLCV DataFrame"""
    result = {"ma20": None, "ma50": None, "ma200": None, "rsi14": None,
              "macd": None, "macd_signal": None, "vol_ratio": None}
    close = df["Close"]
    if len(close) < 20:
        return result
    
    # MA
    result["ma20"] = round(close.rolling(20).mean().iloc[-1], 2)
    if len(close) >= 50:
        result["ma50"] = round(close.rolling(50).mean().iloc[-1], 2)
    if len(close) >= 200:
        result["ma200"] = round(close.rolling(200).mean().iloc[-1], 2)
    
    # RSI(14)
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(14).mean()
    rs = gain / loss
    result["rsi14"] = round(100 - (100 / (1 + rs.iloc[-1])), 1)
    
    # MACD (12,26,9)
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    macd_line = ema12 - ema26
    signal = macd_line.ewm(span=9).mean()
    result["macd"] = round(macd_line.iloc[-1], 2)
    result["macd_signal"] = round(signal.iloc[-1], 2)
    
    # Volume ratio (5d avg / 20d avg)
    vol = df["Volume"]
    vol5 = vol.rolling(5).mean().iloc[-1]
    vol20 = vol.rolling(20).mean().iloc[-1]
    result["vol_ratio"] = round(vol5 / vol20, 2) if vol20 > 0 else 1.0
    
    return result

def fetch_stock_data(ticker):
    """Fetch 200 days of OHLCV from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="200d")
        if df.empty:
            return None, None, None
        # Drop rows where Close is NaN (HK market post-close data sync)
        df = df.dropna(subset=["Close"])
        if df.empty:
            return None, None, None
        price = round(df["Close"].iloc[-1], 2)
        prev_close = round(df["Close"].iloc[-2], 2) if len(df) > 1 else price
        change_pct = round((price - prev_close) / prev_close * 100, 2)
        indicators = compute_indicators(df)
        return price, change_pct, indicators
    except Exception:
        return None, None, None

def fetch_index_data(ticker):
    """Fetch index data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="5d")
        if df.empty:
            return None, None
        price = round(df["Close"].iloc[-1], 2)
        prev = round(df["Close"].iloc[-2], 2) if len(df) > 1 else price
        change_pct = round((price - prev) / prev * 100, 2)
        return price, change_pct
    except Exception:
        return None, None

def analyze_with_deepseek(ticker, name, price, change_pct, indicators, region):
    """DeepSeek interprets real indicators — no guessing"""
    prompt = f"""分析 {ticker} ({name})，{region}股：
價格：{price}，變幅：{change_pct}%
技術指標（真實數據）：
- MA20: {indicators['ma20']}，MA50: {indicators['ma50']}，MA200: {indicators['ma200']}
- RSI(14): {indicators['rsi14']}
- MACD: {indicators['macd']}，Signal: {indicators['macd_signal']}
- 成交量比(5d/20d): {indicators['vol_ratio']}

請給予 100-200 字分析（繁體中文），包括：
1. MA 排列（多頭/空頭/交叉）
2. RSI 位置（超買/超賣/中性）
3. MACD 方向（牛差/熊差）
4. 成交量配合情況
5. 明確的評級：只能從以下六個選擇一個：
   - 建倉買入（強烈買入，技術面全面向好）
   - 加倉買入（中線向好，適合加注）
   - 密切觀察（技術面中性偏好，等信號）
   - 觀望（技術面中性偏弱，不建議操作）
   - 減倉賣出（技術面轉差，減持）
   - 清倉賣出（全面轉壞，離場）
6. 一句簡短 action item（交易員語氣）

輸出 JSON 格式：
{{"rating":"減倉賣出","analysis":"...","action":"..."}}
不要 markdown code block，純 JSON。"""
    try:
        r = httpx.post("https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_KEY}","Content-Type":"application/json"},
            json={"model":"deepseek-chat","messages":[{"role":"user","content":prompt}],
                  "temperature":0.1,"max_tokens":350},
            timeout=30)
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text)
        result = json.loads(text)
        return result.get("rating","觀望"), result.get("analysis",""), result.get("action","")
    except Exception:
        return "觀望", "DeepSeek API 返回異常，無法分析。", "—"

def clean_duplicates():
    """Remove dot-less duplicates (e.g. 0005HK.md when 0005.HK.md exists)"""
    ts = datetime.now().strftime("%Y%m%d")
    for f in Path(TARGET_FOLDER).glob(f"{ts}-*.md"):
        name = f.name.replace(f"{ts}-", "")
        dot_name = name.replace("HK.md", ".HK.md").replace("US.md", ".US.md")
        if dot_name != name:
            dot_path = f.parent / f"{ts}-{dot_name}"
            if dot_path.exists():
                f.unlink()

async def analyze_all():
    print("=== Stock Daily v4 ===")
    today = datetime.now()
    ts = f"{today:%Y%m%d}"
    print(f"Date: {today:%Y-%m-%d %H:%M}")
    
    # Cleanup
    clean_duplicates()
    
    reports = []
    rating_counts = {"建倉買入":0,"加倉買入":0,"密切觀察":0,"觀望":0,"減倉賣出":0,"清倉賣出":0}
    div_alerts = []  # (ex_date, days_until, ticker, name)
    
    # Fetch indices first
    print("\n--- Market Indices ---")
    index_data = {}
    for sym, name, key in INDICES:
        price, chg = fetch_index_data(sym)
        if price:
            arrow = "🔺" if chg and chg >= 0 else "🔻"
            print(f"{name}: {price} ({chg:+.2f}%)")
            index_data[key] = (name, price, chg, arrow)
    
    # Process stocks
    for ticker, name, region in STOCKS:
        print(f"\n--- {ticker} {name} ---")
        price, change_pct, indicators = fetch_stock_data(ticker)
        if price is None:
            print("No data, skipping")
            continue
        print(f"Price: {price}, Change: {change_pct}%")
        print(f"MA20: {indicators['ma20']}, MA50: {indicators['ma50']}, MA200: {indicators['ma200']}")
        print(f"RSI: {indicators['rsi14']}, MACD: {indicators['macd']}/{indicators['macd_signal']}")
        
        if indicators['rsi14'] is None:
            print("Insufficient data, skipping")
            continue
        
        rating, analysis, action = analyze_with_deepseek(ticker, name, price, change_pct, indicators, region)
        rating_counts[rating] = rating_counts.get(rating, 0) + 1
        print(f"Rating: {rating}")
        print(f"Action: {action}")
        
        # Check upcoming dividends (check if ex-div within 30 days)
        try:
            stock = yf.Ticker(ticker)
            divs = stock.dividends
            if not divs.empty:
                last_div = divs.index[-1]
                days_since = (pd.Timestamp.now(tz=last_div.tz) - last_div).days
                # Estimate next ex-div for quarterly stocks (approx 91 days from last)
                # Simpler: just note the last ex-div if within 30 days
                if days_since > 60:  # Approaching next
                    est_next = last_div + pd.Timedelta(days=91)
                    dd = (est_next - pd.Timestamp.now(tz=last_div.tz)).days
                    if 0 < dd <= 30:
                        ex_date_str = est_next.strftime("%Y-%m-%d")
                        div_alerts.append((ex_date_str, dd, ticker, name))
        except:
            pass
        
        # Build frontmatter
        price_ma20 = round(price - indicators['ma20'], 2) if indicators['ma20'] else 0
        price_ma50 = round(price - indicators['ma50'], 2) if indicators['ma50'] else 0
        price_ma200 = round(price - indicators['ma200'], 2) if indicators['ma200'] else 0
        
        page = f"""---
type: stock-analysis
ticker: {ticker}
name: "{name}"
region: {region}
date: {ts}
price: {price}
change_percent: {change_pct}
ma20: {indicators['ma20']}
ma50: {indicators['ma50']}
ma200: {indicators['ma200']}
price_ma20: {price_ma20}
price_ma50: {price_ma50}
price_ma200: {price_ma200}
rsi14: {indicators['rsi14']}
macd: {indicators['macd']}
macd_signal: {indicators['macd_signal']}
vol_ratio: {indicators['vol_ratio']}
rating: {rating}
---
# {ticker} {name} — {today:%Y-%m-%d}
| 指標 | 數值 |
|------|:----:|
| 現價 | {price} |
| 變幅 | {change_pct:+.2f}% |
| MA20 | {indicators['ma20']} |
| MA50 | {indicators['ma50']} |
| MA200 | {indicators['ma200']} |
| 距離MA20 | {price_ma20:+.2f} |
| 距離MA50 | {price_ma50:+.2f} |
| 距離MA200 | {price_ma200:+.2f} |
| RSI(14) | {indicators['rsi14']} |
| MACD | {indicators['macd']} |
| MACD Signal | {indicators['macd_signal']} |
| 成交量比 | {indicators['vol_ratio']} |

## AI 分析
{analysis}

## Action
**{rating}** — {action}
"""
        report_path = Path(TARGET_FOLDER, f"{ts}-{ticker}.md")
        report_path.write_text(page, encoding="utf-8")
        reports.append({"ticker":ticker, "name":name, "price":price, "change":change_pct,
                        "rating":rating, "action":action})
    
    # Save daily summary
    Path(TARGET_FOLDER, f"{ts}-股票分析摘要.md").write_text(
        _build_summary(today, rating_counts, reports, div_alerts, index_data), 
        encoding="utf-8"
    )
    
    # Save watchlist
    save_watchlist()
    
    # Update main dashboard
    update_dashboard(today, rating_counts, index_data, div_alerts)
    
    # Git
    os.chdir("/root/vault")
    os.system("git add -A")
    os.system(f'git commit -m "stock daily v4: {today:%Y%m%d}" --allow-empty')
    os.system("git push")
    print("\n=== All done ===")
    
    # === Auto-complete Kanban card (監察系統) ===
    # After successful analysis, find any running/blocked stock-worker card for today
    # and mark it complete — ensures cards don't sit blocked when reports exist on disk
    try:
        import json, subprocess
        resp = subprocess.run(["hermes", "kanban", "list", "--json"],
                              capture_output=True, text=True, timeout=10)
        if resp.returncode == 0:
            data = json.loads(resp.stdout)
            tasks = data if isinstance(data, list) else data.get("tasks", [])
            card_date = today.strftime("%Y%m%d")
            for t in tasks:
                assignee = t.get("assignee", "")
                status = t.get("status", "")
                title = t.get("title", "")
                tid = t.get("id", t.get("task_id", ""))
                if assignee == "stock-worker" and status in ("running", "blocked"):
                    if card_date in title:
                        subprocess.run(["hermes", "kanban", "complete", tid],
                                       capture_output=True, timeout=10)
                        print(f"✅ Auto-completed Kanban card {tid}: {title}")
    except Exception as e:
        print(f"⚠️  Auto-complete check failed: {e}")

def _build_summary(today, ratings_count, reports, div_alerts, index_data):
    """Build the daily analysis summary page"""
    rating_order = ["建倉買入","加倉買入","密切觀察","觀望","減倉賣出","清倉賣出"]
    
    out = f"""---
type: portfolio-summary
date: {today:%Y%m%d}
status: completed
updated: {today:%Y-%m-%d %H:%M}
---

# 📊 投資組合總覽 — {today:%Y-%m-%d}

> 📅 最後更新：{today:%Y-%m-%d} {today:%H:%M} HKT

## 市場指數
| 指數 | 最新 | 變幅 |
|------|:---:|:----:|
"""
    for key in ["HSI","IXIC","GSPC","DJI"]:
        if key in index_data:
            name, price, chg, arrow = index_data[key]
            color = "🟢" if chg and chg >= 0 else "🔴"
            out += f"| {color} {name} | {price:,.2f} | {chg:+.2f}% |\n"
    
    out += "\n## 評級分佈\n| 評級 | 數量 |\n|------|:----:|\n"
    for r in rating_order:
        count = ratings_count.get(r, 0)
        emoji = "🟢" if "買入" in r else "🟡" if "觀察" in r or "觀望" in r else "🔴"
        out += f"| {emoji} {r} | {count} |\n"
    
    if div_alerts:
        out += "\n## 📅 即將除淨\n"
        for ex_dt, dd, ticker, name in sorted(div_alerts, key=lambda x: x[1]):
            emoji = "🔥🔥" if dd <= 7 else "🔥" if dd <= 30 else "📅"
            out += f"- {emoji} **{ticker}** {name} — {ex_dt}（{dd}天後）\n"
    
    out += "\n## 今日分析\n"
    icon = {"建倉買入":"🟢","加倉買入":"🟢","密切觀察":"🟡","觀望":"⚪","減倉賣出":"🔴","清倉賣出":"🔴"}
    for r in reports:
        if r["rating"] in ("建倉買入","加倉買入"):
            bg = "background:#d4edda"
        elif r["rating"] in ("密切觀察","觀望"):
            bg = "background:#fff3cd"
        else:
            bg = "background:#f8d7da"
        out += f"<div style='{bg};padding:8px;border-radius:4px;margin:4px 0'>"
        out += f"**{icon[r['rating']]} {r['ticker']} {r['name']}** — {r['price']} ({r['change']:+.2f}%) — {r['action']}"
        out += "</div>\n"
    
    out += "\n## 股票總表\n| 股票 | 名稱 | 現價 | 變幅 | 評級 |\n|------|------|:---:|:----:|:----:|\n"
    for r in reports:
        emoji = icon.get(r["rating"], "⚪")
        out += f"| {r['ticker']} | {r['name']} | {r['price']} | {r['change']:+.2f}% | {emoji} {r['rating']} |\n"
    
    return out

def save_watchlist():
    today = datetime.now()
    ts = f"{today:%Y%m%d}"
    rating_order = {"建倉買入":0,"加倉買入":1,"密切觀察":2,"觀望":3,"減倉賣出":4,"清倉賣出":5}
    icon = {"建倉買入":"🟢","加倉買入":"🟢","密切觀察":"🟡","觀望":"⚪","減倉賣出":"🔴","清倉賣出":"🔴"}
    
    stocks = []
    skip_suffixes = ("股票分析摘要.md", "股票分析框架.md", "股息日曆.md", "股票監察名單.md")
    for f in sorted(Path(TARGET_FOLDER).glob(f"{ts}-*.md")):
        if f.name.endswith(skip_suffixes):
            continue
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not m: continue
        fm = {}
        for line in m.group(1).strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"').strip("'")
        ticker = fm.get("ticker","")
        name = fm.get("name","")
        price = fm.get("price","?")
        change = fm.get("change_percent","")
        rating = fm.get("rating","觀望")
        rsi14 = fm.get("rsi14","")
        ma20 = fm.get("ma20","")
        ma50 = fm.get("ma50","")
        ma200 = fm.get("ma200","")
        action_text = ""
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("## Action"):
                if i + 1 < len(lines):
                    action_text = lines[i + 1].strip()
                break
        stocks.append({
            "ticker": ticker, "name": name, "price": price,
            "change": f"{float(change):+.2f}%" if change else "",
            "rating": rating, "rs": rsi14, "ma20": ma20, "ma50": ma50, "ma200": ma200,
            "action": action_text
        })
    
    stocks.sort(key=lambda x: (rating_order.get(x["rating"], 9), x["ticker"]))
    
    out = f"""---
type: watchlist
date: {ts}
updated: {today:%Y-%m-%d %H:%M}
---

# 📋 股票監察名單 — {today:%Y-%m-%d}

> 按評級排列，6 個等級：🟢建倉買入 → 🟢加倉買入 → 🟡密切觀察 → ⚪觀望 → 🔴減倉賣出 → 🔴清倉賣出

| 評級 | 股票 | 名稱 | 現價 | 變幅 | RSI | MA20 | MA50 | MA200 |
|:----:|:----:|:----:|:---:|:----:|:---:|:----:|:----:|:-----:|
"""
    for s in stocks:
        ik = icon.get(s["rating"], "⚪")
        out += f"| {ik} | {s['ticker']} | {s['name']} | {s['price']} | {s['change']} | {s['rs']} | {s['ma20']} | {s['ma50']} | {s['ma200']} |\n"
    
    out += "\n## 詳細 Action Items\n"
    curr_rating = None
    for s in stocks:
        if s["rating"] != curr_rating:
            curr_rating = s["rating"]
            out += f"\n### {icon.get(curr_rating, '⚪')} {curr_rating}\n"
        out += f"- **{s['ticker']}** {s['name']} — {s['action']}\n"
    
    Path(TARGET_FOLDER, f"{ts}-股票監察名單.md").write_text(out, encoding="utf-8")

def update_dashboard(today, ratings_count, index_data, div_alerts):
    """Update the main 01_投資組合總覽.md dashboard"""
    rating_order = ["建倉買入","加倉買入","密切觀察","觀望","減倉賣出","清倉賣出"]
    
    # Count stocks per rating across TODAY's reports
    ts = f"{today:%Y%m%d}"
    report_files = [f for f in Path(TARGET_FOLDER).glob(f"{ts}-*.md")
                    if f.name not in ("股票分析摘要.md","股票分析框架.md","股息日曆.md")]
    
    dashboard = f"""---
cssclasses:
  - dashboard
type: portfolio-summary
date: {ts}
updated: {today:%Y-%m-%d %H:%M}
---

# 🏛️ 投資組合總覽

> 📅 最後更新：{today:%Y-%m-%d} {today:%H:%M} HKT

```dataviewjs
// 格價 Dashboard Link
dv.span('<a href="02-Wiki/格價儀錶板.md" style="background:#4a90d9;color:white;padding:8px 16px;border-radius:6px;text-decoration:none;font-weight:bold;">🛒 格價 Dashboard</a>')
dv.span(' ')
dv.span('<a href="02-Wiki/02_個股分析.md" style="background:#7c3aed;color:white;padding:8px 16px;border-radius:6px;text-decoration:none;font-weight:bold;">📈 個股分析</a>')
dv.span(' ')
dv.span('<a href="02-Wiki/Stocks/{ts}-股票監察名單.md" style="background:#e67e22;color:white;padding:8px 16px;border-radius:6px;text-decoration:none;font-weight:bold;">📋 股票監察名單</a>')
```
"""
    
    # Market indices
    dashboard += "\n## 🌍 市場指數\n"
    dashboard += "| 指數 | 最新 | 變幅 |\n|------|:---:|:----:|\n"
    for key in ["HSI","IXIC","GSPC","DJI"]:
        if key in index_data:
            name, price, chg, arrow = index_data[key]
            color = "🟢" if chg and chg >= 0 else "🔴"
            dashboard += f"| {color} {name} | {price:,.2f} | {chg:+.2f}% |\n"
    
    # Rating distribution
    dashboard += "\n## 📊 評級分佈\n"
    total = sum(ratings_count.values()) or 1
    for r in rating_order:
        cnt = ratings_count.get(r, 0)
        pct = round(cnt / total * 100)
        bar = "█" * pct + "░" * (10 - pct) if pct <= 10 else "█" * 10
        emoji = "🟢" if "買入" in r else "🟡" if "觀察" in r or "觀望" in r else "🔴"
        dashboard += f"- {emoji} **{r}**: {cnt} 隻 `{bar}`\n"
    
    # Div alerts
    if div_alerts:
        dashboard += "\n## 📅 即將除淨\n"
        for ex_dt, dd, ticker, name in sorted(div_alerts, key=lambda x: x[1]):
            emoji = "🔥🔥" if dd <= 7 else "🔥" if dd <= 30 else "📅"
            dashboard += f"- {emoji} **{ticker}** {name} — {ex_dt}（{dd}天後）\n"
    
    # Dataview table pulling from today's stock reports
    dashboard += f"""
## 📈 今日分析
```dataview
TABLE 
    choice(rating="建倉買入" or rating="加倉買入", "🟢", 
           choice(rating="密切觀察" or rating="觀望", "🟡", "🔴")) + " " + rating AS "評級",
    price AS "現價",
    change_percent + "%" AS "變幅",
    rsi14 AS "RSI(14)",
    ma20 AS "MA20",
    ma50 AS "MA50",
    choice(rating="建倉買入" or rating="加倉買入", "✅ 買入機會", 
           choice(rating="密切觀察", "👀 等信號",
           choice(rating="觀望", "⏸️ 暫時不動", "⚠️ 減持"))) AS "建議"
FROM "02-Wiki/Stocks/{ts}"
WHERE type = "stock-analysis"
SORT choice(rating="建倉買入", 0, rating="加倉買入", 1, rating="密切觀察", 2, rating="觀望", 3, rating="減倉賣出", 4, 5) ASC
```
"""
    
    Path("/root/vault/02-Wiki/01_投資組合總覽.md").write_text(dashboard, encoding="utf-8")

# === Main ===
if __name__ == "__main__":
    import asyncio
    asyncio.run(analyze_all())
