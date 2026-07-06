#!/usr/bin/env python3
"""每日股票分析 v2 - 含真實股價"""
import asyncio, httpx, json, re, os, subprocess, yfinance as yf
from datetime import datetime
from pathlib import Path

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY", os.environ.get("DEEPSEEK_API_KEY", ""))
WATCHLIST_FILE = "/root/vault/stock-watchlist.json"
TARGET_FOLDER = "/root/vault/02-Wiki/Stocks"
OBSIDIAN_URL = "http://100.98.113.30:8766/obsidian/vault"
OBSIDIAN_AUTH = os.environ.get("OBSIDIAN_AUTH", "")
RATINGS = ("建倉買入", "加倉買入", "減倉賣出", "清倉賣出", "密切觀察", "觀望")

def load_wl():
    return json.loads(Path(WATCHLIST_FILE).read_text()) if Path(WATCHLIST_FILE).exists() else []

def get_rating(text):
    for r in RATINGS:
        if r in text: return r
    return "密切觀察"

def fetch_price(ticker):
    """從 Yahoo Finance 獲取真實股價"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
        change = info.get("regularMarketChangePercent")
        high = info.get("dayHigh")
        low = info.get("dayLow")
        vol = info.get("regularMarketVolume")
        pe = info.get("trailingPE")
        div = info.get("dividendYield")
        results = {"price": price, "change": change, "high": high, "low": low,
                   "vol": vol, "pe": pe, "div": div, "ok": price is not None}
        return results
    except:
        return {"ok": False}

async def analyze(ticker):
    # 先抓真實股價
    mkt = fetch_price(ticker)
    price_info = ""
    if mkt["ok"]:
        price_info = (
            f"\n【即時股價】\n"
            f"現價: {mkt['price']}\n"
            f"日內波幅: {mkt.get('low','N/A')} - {mkt.get('high','N/A')}\n"
            f"變動: {mkt.get('change','N/A')}%\n"
            f"成交量: {mkt.get('vol','N/A')}\n"
            f"市盈率: {mkt.get('pe','N/A')}\n"
        )
    else:
        price_info = f"\n【即時股價】無法獲取，請自行查詢\n"

    p = (
        f"你是一位資深港股美股投資專家。"
        f"對 {ticker} 進行分析，參考以下即時數據：\n{price_info}\n"
        f"輸出格式：\n"
        f"【評級】：建倉買入/加倉買入/減倉賣出/清倉賣出/密切觀察/觀望\n"
        f"【技術面】：均線狀態、MACD、RSI\n"
        f"【基本面】：盈利狀況、估值\n"
        f"【策略】：入場區間、目標價、止損位（基於真實價格計算）"
    )
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post("https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"},
            json={"model":"deepseek-chat","messages":[
                {"role":"system","content":"用繁體中文。分析必須基於提供的真實股價數據。"},
                {"role":"user","content":p}
            ],"max_tokens":2048})
    txt = r.json()["choices"][0]["message"]["content"]
    return {"content":txt,"rating":get_rating(txt),"ticker":ticker.upper()}

async def save(d):
    today=datetime.now(); fn=f"{today:%Y%m%d}-{d['ticker']}.md"
    content=f"---\ntype: stock-analysis\nticker: {d['ticker']}\ndate: {today:%Y%m%d}\nrating: {d['rating']}\nstatus: completed\n---\n\n{d['content']}"
    Path(f"{TARGET_FOLDER}/{fn}").parent.mkdir(parents=True, exist_ok=True)
    Path(f"{TARGET_FOLDER}/{fn}").write_text(content, encoding="utf-8")
    print(f"  ✅ {d['ticker']} → {d['rating']}")
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            await c.put(f"{OBSIDIAN_URL}/{fn}", headers={"Authorization":OBSIDIAN_AUTH}, json={"content":content})
    except: pass

async def main():
    wl=load_wl(); print(f"🔄 {len(wl)} 隻股票（含真實股價）"); results=[]
    for i,t in enumerate(wl,1):
        try:
            print(f"   [{i}/{len(wl)}] {t} 查價中...")
            d=await analyze(t); await save(d); results.append(d)
            print(f"      → {d['rating']}")
        except Exception as e:
            print(f"   ❌ {t}: {str(e)[:100]}")
    if len(results) >= len(wl) * 0.5:
        today_str = datetime.now().strftime("%Y%m%d")
        count = 0
        for f in Path(TARGET_FOLDER).glob("*.md"):
            if today_str not in f.name and "-" in f.name and f.name[0].isdigit():
                f.unlink(); count += 1
        print(f"  🗑️ 清理 {count} 個舊報告")
    try:
        subprocess.run(["git","-C","/root/vault","add","."],capture_output=True,timeout=30)
        subprocess.run(["git","-C","/root/vault","commit","-m",f"stock daily {datetime.now():%Y%m%d}"],capture_output=True,timeout=30)
        subprocess.run(["git","-C","/root/vault","push"],capture_output=True,timeout=60)
        print("✅ Git push 完成")
    except Exception as e: print(f"⚠️ Git: {e}")

if __name__=="__main__":
    today=datetime.now(); asyncio.run(main())
