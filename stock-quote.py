#!/usr/bin/env python3
"""Fetch stock quote + today's vault analysis. Outputs formatted text for Telegram."""
import sys, json, os, re
from datetime import datetime
import yfinance as yf

ticker = sys.argv[1].strip().upper()

# Auto-suffix HK for plain 4-5 digit codes like 0941 → 0941.HK
raw_ticker = ticker
if ticker.isdigit() and len(ticker) <= 5:
    ticker += ".HK"

STOCKS_DIR = "/root/vault/02-Wiki/Stocks"
today = datetime.now().strftime("%Y%m%d")

# ── 1. Fetch real-time price ──
live = {"price": "N/A", "change_val": 0, "change_pct": 0, "currency": "HKD"}
try:
    stock = yf.Ticker(ticker)
    info = stock.info
    if info and info.get("regularMarketPrice") is not None:
        p = info.get("regularMarketPrice", 0)
        cv = info.get("regularMarketChange", 0)
        cp = info.get("regularMarketChangePercent", 0)
        prev = info.get("regularMarketPreviousClose", 0) or 0
        if cv == 0 and cp == 0 and prev > 0:
            cv = p - prev
            cp = (cv / prev) * 100
        live = {
            "price": p,
            "change_val": cv,
            "change_pct": cp,
            "currency": info.get("currency", "HKD"),
            "name": info.get("shortName") or info.get("longName") or ticker,
            "day_high": info.get("dayHigh", "N/A"),
            "day_low": info.get("dayLow", "N/A"),
            "volume": info.get("volume", 0),
        }
    else:
        live["name"] = ticker
except Exception:
    live["name"] = ticker

# ── 2. Read vault analysis ──
# Try multiple date patterns: today, yesterday, or any existing file
analysis = {}
for d in [today, (datetime.now().strftime("%Y%m%d"))]:
    candidates = [
        f"{STOCKS_DIR}/{d}-{raw_ticker}.md",
        f"{STOCKS_DIR}/{d}-{ticker}.md",
        f"{STOCKS_DIR}/{d}-{raw_ticker.replace('.', '-')}.md",
        f"{STOCKS_DIR}/{d}-{ticker.replace('.', '-')}.md",
    ]
    # Also try with date like 20260711-0941-HK.md (hyphen before HK)
    candidates.append(f"{STOCKS_DIR}/{d}-{raw_ticker.replace('.', '-')}-{raw_ticker.split('.')[-1] if '.' in raw_ticker else ''}.md")
    candidates.append(f"{STOCKS_DIR}/{d}-{ticker.replace('.', '-')}.md")
    
    for c in candidates:
        if os.path.exists(c):
            content = open(c, encoding="utf-8").read()
            m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if m:
                fm = {}
                for line in m.group(1).split('\n'):
                    if ':' in line:
                        k, _, v = line.partition(':')
                        fm[k.strip()] = v.strip().strip('"').strip("'")
                # Get AI analysis paragraph
                ai_m = re.search(r'## AI 分析\n(.+?)(?:\n##|\Z)', content, re.DOTALL)
                if ai_m:
                    fm['ai_analysis'] = ai_m.group(1).strip()
                # Get action recommendation
                action_m = re.search(r'## Action\n(.+)', content)
                if action_m:
                    fm['action'] = action_m.group(1).strip()
                analysis = fm
                break
    if analysis:
        break

# ── 3. Build message ──
name = live.get("name", analysis.get("name", ticker))
p = live["price"]
cv = live["change_val"]
cp = live["change_pct"]
currency = live["currency"]

if isinstance(p, (int, float)):
    sign = "+" if cv >= 0 else ""
    emoji = "🟢" if cv >= 0 else "🔴"
    price_line = f"{emoji} <b>{name}</b> ({ticker})\n💰 {currency} {p}  ({sign}{cv:.3f} / {sign}{cp:.2f}%)"
else:
    price_line = f"<b>{name}</b> ({ticker})\n💰 價格獲取失敗"

msg = price_line

# Rating from analysis
rating = analysis.get("rating", "")
if rating:
    rating_emoji = {"建倉買入": "🟢", "加倉買入": "🟢", "密切觀察": "🟡", "觀望": "🟡", "減倉賣出": "🔴", "清倉賣出": "🔴"}
    re = rating_emoji.get(rating, "⚪")
    msg += f"\n📊 {re} 評級: <b>{rating}</b>"

# Technical context
rsi = analysis.get("rsi14", "")
ma20 = analysis.get("ma20", "")
ma50 = analysis.get("ma50", "")
if rsi:
    rsi_val = float(rsi)
    rsi_note = "超買" if rsi_val > 70 else ("超賣區邊緣" if rsi_val < 35 else ("中性偏弱" if rsi_val < 45 else "中性"))
    msg += f"\n📉 RSI(14): {rsi} ({rsi_note})"
if ma20 and ma50 and isinstance(p, (int, float)):
    dist_ma20 = ((p - float(ma20)) / float(ma20)) * 100
    dist_ma50 = ((p - float(ma50)) / float(ma50)) * 100
    ma20_signal = "📈 上穿" if dist_ma20 > 0 else "📉 下穿"
    ma50_signal = "📈 上穿" if dist_ma50 > 0 else "📉 下穿"
    msg += f"\n📐 MA20: {ma20}"
    msg += f"\n📐 MA50: {ma50}"

# Volume
vol = live.get("volume", 0)
if isinstance(vol, (int, float)) and vol > 0:
    msg += f"\n📊 成交量: {vol:,.0f}"

# AI analysis
ai = analysis.get("ai_analysis", "")
if ai:
    # Truncate to keep message reasonable
    if len(ai) > 300:
        ai = ai[:297] + "..."
    msg += f"\n\n💡 {ai}"

# Action
action = analysis.get("action", "")
if action:
    msg += f"\n\n🎯 <b>{action}</b>"

# Source note
if analysis:
    msg += "\n\n<small>📋 分析來自每日報告</small>"
else:
    msg += "\n\n<small>⚠️ 今日未有詳細分析</small>"

print(msg)
