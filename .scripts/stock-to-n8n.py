#!/usr/bin/env python3
"""Post today's stock report summary to Telegram"""
import json, glob, os, re, sys, httpx
from datetime import datetime
from pathlib import Path

# Config
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
if not BOT_TOKEN:
    print("❌ TELEGRAM_TOKEN not set in environment")
    sys.exit(1)
CHAT_ID = "1992453360"
WATCHLIST_FILE = "/root/vault/stock-watchlist.json"
STOCKS_DIR = "/root/vault/02-Wiki/Stocks"

def send_telegram(msg):
    """Send message directly to Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        resp = httpx.post(url, json=payload, timeout=10)
        data = resp.json()
        if data.get("ok"):
            print(f"✅ Telegram: message sent")
        else:
            print(f"❌ Telegram error: {data}")
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")

def parse_stock_report(filepath):
    """Parse frontmatter from a stock markdown report"""
    content = Path(filepath).read_text(encoding="utf-8")
    # Extract YAML frontmatter
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val
    return fm

def main():
    today = datetime.now().strftime("%Y%m%d")
    files = sorted(glob.glob(f"{STOCKS_DIR}/{today}-*.md"))
    # Filter out non-stock files
    skip_patterns = ["股票分析摘要", "股票監察名單", "股票分析框架", "股息日曆"]
    files = [f for f in files if not any(s in f for s in skip_patterns)]
    
    if not files:
        print(f"No stock reports found for {today}")
        sys.exit(1)
    
    stocks = []
    for f in files:
        data = parse_stock_report(f)
        if data and data.get("ticker") and data.get("price"):
            stocks.append(data)
    
    payload = {
        "date": today,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M HKT"),
        "total": len(stocks),
        "stocks": stocks,
        "summary": {
            "positive": sum(1 for s in stocks if float(s.get("change_percent", 0)) > 0),
            "negative": sum(1 for s in stocks if float(s.get("change_percent", 0)) < 0),
            "buy_signals": sum(1 for s in stocks if s.get("rating") in ["建倉買入", "加倉買入", "偏好"]),
            "watch": sum(1 for s in stocks if s.get("rating") in ["密切觀察", "觀望", "中性"]),
            "sell_signals": sum(1 for s in stocks if s.get("rating") in ["減倉賣出", "規避"]),
        }
    }
    
    # Try to include index data from dashboard
    dashboard_path = "/root/vault/02-Wiki/01_投資組合總覽.md"
    if os.path.exists(dashboard_path):
        content = Path(dashboard_path).read_text(encoding="utf-8")
        # Extract HSI line
        for line in content.split('\n'):
            if 'HSI' in line or '恆生指數' in line:
                m = re.search(r'\|\s*[🟢🔴]\s*\S+\s*\|\s*([\d,]+\.?\d*)\s*\|\s*([+-]?\d+\.?\d*)%', line)
                if m:
                    payload["hsi"] = {"price": m.group(1).replace(',', ''), "change": m.group(2)}
                break
    
    print(f"📊 Parsed {len(stocks)} stock reports")
    
    # === Format Telegram message ===
    ts = datetime.now().strftime("%Y-%m-%d %H:%M HKT")
    summary = payload["summary"]
    hsi = payload.get("hsi")
    
    msg = f"<b>📊 每日股票報告</b>\n📅 {today} {ts}\n"
    
    if hsi:
        sign = "+" if float(hsi["change"]) >= 0 else ""
        emoji = "🟢" if float(hsi["change"]) >= 0 else "🔴"
        msg += f"{emoji} 恆生指數: <b>{hsi['price']}</b> ({sign}{hsi['change']}%)\n"
    
    msg += f"\n📊 <b>概要</b>\n"
    msg += f"🟢 上升: {summary['positive']}  |  🔴 下跌: {summary['negative']}  |  ⚪ 持平: {len(stocks) - summary['positive'] - summary['negative']}\n"
    msg += f"⭐ 買入: {summary['buy_signals']}  |  👀 觀望: {summary['watch']}  |  ⚠️ 賣出: {summary['sell_signals']}\n"
    
    # HK stocks
    hk = [s for s in stocks if s.get("ticker","").endswith(".HK")]
    if hk:
        msg += f"\n<b>🔹 港股</b>\n"
        for s in hk:
            pct = float(s.get("change_percent", 0))
            sign = "+" if pct >= 0 else ""
            emoji = "🟢" if pct > 0.3 else ("🔴" if pct < -0.3 else "⚪")
            msg += f"{emoji} <b>{s['name']}</b> ({s['ticker']})\n"
            msg += f"   💰 {s['price']} ({sign}{s['change_percent']}%) ⭐{s.get('rating','—')}\n"
    
    # US stocks
    us = [s for s in stocks if not s.get("ticker","").endswith(".HK")]
    if us:
        msg += f"\n<b>🔹 美股</b>\n"
        for s in us:
            pct = float(s.get("change_percent", 0))
            sign = "+" if pct >= 0 else ""
            emoji = "🟢" if pct > 0.3 else ("🔴" if pct < -0.3 else "⚪")
            msg += f"{emoji} <b>{s['name']}</b> ({s['ticker']})\n"
            msg += f"   💰 ${s['price']} ({sign}{s['change_percent']}%) ⭐{s.get('rating','—')}\\n"

    msg += "\\n<i>🤖 Generated by Hermes</i>"

    # Send to Telegram
    send_telegram(msg)
    print(f"📊 Done: {len(stocks)} stocks reported")

if __name__ == "__main__":
    main()
