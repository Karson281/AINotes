#!/usr/bin/env python3
"""
Proma Agent 本機推送腳本
用途：將 Hermes 的股票評級結果透過 Local REST API 寫入本機 Obsidian Vault。
修正：中文目錄路徑使用 urllib.parse.quote() 進行 URL 編碼。
"""

import requests
import json
from datetime import date
import urllib.parse
import urllib3

# 停用自簽憑證警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# 設定區
# ==========================================
# Obsidian Local REST API 設定 (預設 port 為 27124)
OBSIDIAN_API = "https://127.0.0.1:27124"
# 替換為您的 Local REST API Key (在 Obsidian 設定 -> Local REST API 中獲取)
OBSIDIAN_KEY = "YOUR_OBSIDIAN_API_KEY_HERE"

# 【關鍵】：中文目錄必須與 Obsidian Vault 中的實際路徑一致
# 格式：YYYYMMDD-TICKER.md（例如：20260623-0005.HK.md）
TARGET_FOLDER = "02-Wiki/Stocks"

HEADERS = {
    "Authorization": f"Bearer {OBSIDIAN_KEY}",
    "Content-Type": "text/markdown"
}

# 模擬從 Hermes (VPS) 獲取的 JSON 數據
MOCK_HERMES_DATA = {
    "0700.HK": {
        "rating": "密切觀察",
        "technical": "- 均線狀態：股價現報 380 港元，5 日/10 日/20 日均線多頭排列，但上方遇阻。\n- MACD：DIF 與 DEA 均在零軸上方，柱狀圖收窄。\n- RSI：14 日 RSI 為 58，中性偏強。",
        "fundamental": "- 2024 年淨利潤約 1,200 億港元，年增 8.5%。\n- PE 約 10.6 倍，低於 5 年平均。\n- 股息率約 6.5%。",
        "strategy": "- 入場區間：375-385 港元\n- 目標價：400 港元\n- 止損位：365 港元"
    },
    "0941.HK": {
        "rating": "加倉買入",
        "technical": "- 均線狀態：股價 59.80 港元，站穩 5 日/10 日/20 日均線，多頭排列。\n- MACD：DIF 高於 DEA，動能增強。\n- RSI：62.5，未達超買。",
        "fundamental": "- 2024 年營收 1,900 億港元，淨利潤 520 億。\n- PE 10.5 倍，低於行業均值。\n- 股息率 6.8%。",
        "strategy": "- 入場區間：59.00-60.50 港元\n- 目標價：66.00 港元\n- 止損位：55.50 港元"
    },
    "9988.HK": {
        "rating": "觀望",
        "technical": "- 均線狀態：空頭排列，下行趨勢未止。\n- MACD：死叉。\n- RSI：32，偏弱。",
        "fundamental": "- 電商業務增長放緩。\n- 雲業務持續虧損。\n- 監管風險未消。",
        "strategy": "- 暫不建议入場\n- 觀察 80 港元支撐\n- 跌破 75 港元止損"
    }
}

def push_to_obsidian(stock_code: str, data: dict):
    """將評級結果寫入 Obsidian"""
    today = date.today().strftime("%Y%m%d")
    # 檔名格式：YYYYMMDD-TICKER.md（與現有資料一致）
    filename = f"{today}-{stock_code}.md"

    # 構建包含 Frontmatter 的 Markdown 內容（與現有格式一致）
    content = f"""---
type: stock-analysis
ticker: {stock_code}
date: {today}
rating: "{data['rating']}"
status: completed
source: proma-agent
---

【評級】：{data['rating']}
【技術面】：
{data['technical']}

【基本面】：
{data['fundamental']}

【策略】：
{data['strategy']}
"""

    # 【關鍵修正】：對中文目錄和檔名進行 URL Encoding
    encoded_folder = urllib.parse.quote(TARGET_FOLDER, safe='')
    encoded_filename = urllib.parse.quote(filename, safe='')
    url = f"{OBSIDIAN_API}/vault/{encoded_folder}/{encoded_filename}"

    try:
        resp = requests.put(
            url,
            headers=HEADERS,
            data=content.encode("utf-8"),
            verify=False
        )

        if resp.status_code in [200, 201, 204]:
            print(f"✅ 成功推送: {data['name']} ({stock_code})")
        else:
            print(f"❌ 推送失敗: {stock_code} - HTTP {resp.status_code} - {resp.text}")

    except requests.exceptions.ConnectionError:
        print("❌ 連線失敗：請確認 Obsidian 是否已開啟，且 Local REST API 插件已啟用。")

if __name__ == "__main__":
    print(f"🚀 開始執行 Proma Agent 本機推送任務 ({date.today()})")
    print(f"📂 目標目錄: {TARGET_FOLDER}")
    print("-" * 40)

    ratings = MOCK_HERMES_DATA

    for code, data in ratings.items():
        push_to_obsidian(code, data)

    print("-" * 40)
    print("✨ 推送任務完成！請打開 Obsidian 查看最新 Dashboard。")
