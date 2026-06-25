---
type: reference
title: Telegram Bot v2 完整參考手冊
created: 2026-06-23
updated: 2026-06-24
status: active
---

# Telegram Bot v2 完整參考手冊

> Proma Telegram Bot — 24/7 VPS 運作，自帶 watchlist + 每日 18:00 自動分析 + Google 整合

---

## 架構

```
用戶 (Telegram)
  │
  ▼
VPS (root@187.127.96.73)
  ├── proma-bot.py           ← Bot 主程式（DeepSeek API + Google API）
  ├── google_services.py     ← Google 模組（選裝）
  ├── stock-watchlist.json   ← Watchlist（本機儲存，24/7）
  ├── bot-chat-ids.json      ← 已註冊嘅 Telegram chat ID
  ├── google-token.json      ← Google OAuth token（選裝）
  ├── api-key.txt            ← Maps API key（選裝）
  └── bot.log                ← 運行日誌
        │
        ▼
Windows (100.98.113.30:8766) ← 可選，用嚟 sync Obsidian
  └── obsidian-write-proxy.py
```

---

## Telegram Commands

### 📈 股票分析

| Command          | 用法                       | 範例                    | 說明                  |
| ---------------- | ------------------------ | --------------------- | ------------------- |
| `分析 {代號}`        | `分析 0941.HK`             | `分析 0941.HK`          | 單隻股票即時分析            |
| `分析 {代號}`        | `分析 AAPL`                | `分析 AAPL`             | 美股都得                |
| `/stocks`        | `/stocks`                | `/stocks`             | 列出 watchlist        |
| `/stocks add`    | `/stocks add 0700.HK`    | `/stocks add 0700.HK` | 加入股票                |
| `/stocks remove` | `/stocks remove 0700.HK` | `/stocks remove AAPL` | 移除股票                |
| `/analyze`       | `/analyze`               | `/analyze`            | 批量分析全部 watchlist 股票 |
| `/start`         | `/start`                 | `/start`              | 顯示 menu + 註冊每日排程    |

**實例：**

```
你：分析 0941.HK
Bot：🔍 分析 0941.HK，請稍候...
Bot：✅ 0941.HK
     評級：加倉買入
     📂 02-Wiki/Stocks/20260623-0941.HK.md
     【評級】：加倉買入
     【技術面】...
```

```
你：/stocks
Bot：📋 Watchlist (18 隻):
     • 0005.HK
     • 0941.HK
     ...

你：/stocks add TSLA
Bot：✅ 已加入 TSLA 至 watchlist

你：/stocks remove O
Bot：✅ 已從 watchlist 移除 O
```

```
你：/analyze
Bot：🔄 開始批量分析 18 隻股票...
Bot：✅ 0363.HK — 建倉買入
Bot：✅ 0823.HK — 加倉買入
Bot：◽ O — 觀望
...
Bot：📊 批量分析完成 (18/18)
     🟢 建倉/加倉 (7): 0363, 0823, 0941, 3988, JPM, CVX, VZ
     🟡 密切觀察 (9): 0005, 0267, 0270, ...
     🔴 減倉/清倉 (0): 無
     ⚪ 觀望 (2): 0006, O
```

### 🔌 Google 服務（需先完成 OAuth 授權）

| Command          | 用法               | 範例                 | 說明                 |
| ---------------- | ---------------- | ------------------ | ------------------ |
| `/gmail`         | `/gmail`         | `/gmail`           | 列出未讀郵件             |
| `/gmail read N`  | `/gmail read 1`  | `/gmail read 2`    | 睇第 N 封郵件內容         |
| `/calendar`      | `/calendar`      | `/calendar`        | 今日行程               |
| `/calendar week` | `/calendar week` | `/calendar week`   | 未來 7 日行程           |
| `/sheets`        | `/sheets`        | `/sheets`          | 列出最近 Google Sheets |
| `/docs`          | `/docs`          | `/docs`            | 列出最近 Google Docs   |
| `/docs read N`   | `/docs read 1`   | `/docs read 3`     | 睇第 N 份文件內容         |
| `/drive`         | `/drive`         | `/drive`           | 列出最近 Drive 檔案      |
| `/drive {關鍵字}`   | `/drive budget`  | `/drive Q4 report` | 搜尋 Drive 檔案        |
| `/maps {關鍵字}`    | `/maps 中環咖啡`     | `/maps 銅鑼灣日本菜`     | 搜尋地點               |
| `/mystatus`      | `/mystatus`      | `/mystatus`        | 顯示 Google 授權狀態     |

---

## 常見 Google 實用場景

### 🏛 朝早 check email + calendar
```
你：/gmail
Bot：📧 未讀郵件 (3)
     1. [Boss] Today's meeting agenda
     2. [Bank] Payment received
     3. [Amazon] Package delivered

你：/gmail read 1
Bot：📧 **Today's meeting agenda**
     從: Boss <ceo@company.com>
     
     Hi team, let's discuss Q3 results at 10am...

你：/calendar
Bot：📅 今日行程
     • 10:00 — Team standup
     • 14:30 — Client presentation
     • 18:00 — 睇 stock report
```

### 📁 搵文件 + 睇內容
```
你：/drive Q4 report
Bot：🔍 Drive 搜尋: Q4 report
     • Q4-2025-financial-report.xlsx (spreadsheet)
     • Q4-sales-summary.pptx (presentation)

你：/docs
Bot：📄 最近 Docs
     1. Meeting Notes (2026-06-23)
     2. Project Plan (2026-06-20)

你：/docs read 1
Bot：# Meeting Notes
     Attendees: John, Sarah, Mike
     Agenda:
     1. Q3 results review
     2. Budget allocation
```

### 🍜 搵食 / 地圖搜尋
```
你：/maps 中環平價午餐
Bot：📍 搜尋結果: 中環平價午餐
     • **孖沙茶餐廳** ⭐⭐⭐⭐
       中環禧利街XX號
       https://google.com/maps/place/?q=place_id:xxx
     • **泰昌餅家** ⭐⭐⭐
       中環擺花街XX號
```

### 📊 Sheets 快速睇
```
你：/sheets
Bot：📊 最近 Sheets
     • Stock Portfolio Tracker (updated 2026-06-23)
     • Budget 2026 (updated 2026-06-20)
```

---

## 每日 18:00 自動分析

- **時間：** 每日 18:00 HKT（UTC+8）
- **觸發：** Bot 自動運行 `/analyze` 功能
- **結果：** 發送到所有註冊咗嘅 Telegram chat
  - Summary + 重點關注列表（建倉/加倉股票會 highlight）
  - 如果 Windows 開機中，同步寫入 Obsidian
- **註冊：** 同 Bot 講 `/start` 就會自動註冊

**如何更改 watchlist：**
1. `/stocks add TICKER` — 加入新股票
2. `/stocks remove TICKER` — 移除
3. 或者直接改 Obsidian Stock-Task-List.md（Windows 開機時 sync）

---

## Stock-Task-List.md 雙向同步

Bot 同 Obsidian Stock-Task-List.md 嘅 sync 機制：

```
VPS stock-watchlist.json  ←→  Windows Stock-Task-List.md
      (主要 source)           (Windows 開機時 sync)
```

- Bot 以 **VPS watchlist** 為準（24/7）
- Windows 開機 → Proxy reachable → Bot 會 sync 返去 Obsidian
- Obsidian 嘅 stock 會 merge 入 VPS watchlist

---

## 評級說明

| 評級 | 意思 | 策略 |
|:----:|------|------|
| 建倉買入 | 估值吸引，可開始買入 | 分注建倉 |
| 加倉買入 | 已持倉，可加注 | 現有基礎上加碼 |
| 減倉賣出 | 估值偏高或風險升溫 | 減持部份倉位 |
| 清倉賣出 | 基本面轉差 | 全數賣出 |
| 密切觀察 | 值得留意但未到入市時機 | 等更好價位 |
| 觀望 | 不建議買入 | 避開 |

以前 Bot 會將「中性」誤判為「觀望」，**已修復** ✅

---

## 部署維護

### VPS start/stop/restart
```bash
# 啟動（background）
cd /root && nohup python3 /root/proma-bot.py > /root/bot.log 2>&1 &

# 睇 log
tail -f /root/bot.log

# 搜尋 log
grep "DAILY\|ERROR\|SCHEDULER" /root/bot.log

# Kill
pkill -f proma-bot.py

# Check 行緊
ps aux | grep proma-bot | grep -v grep
```

### 更新 Bot code
```bash
nano /root/proma-bot.py        # 貼新版
pkill -f proma-bot.py          # 停舊
cd /root && nohup python3 /root/proma-bot.py > /root/bot.log 2>&1 &   # 開新
```

### Google 未授權時
Bot 嘅 Stock 功能完全唔需要 Google，可以直接用。
只有 `/gmail` `/calendar` `/sheets` `/docs` `/drive` `/maps` 需要 Google OAuth。

---

## 疑難排解

**Q: Bot 冇反應 / 收唔到 message**
```
cat /root/bot.log | tail -20
```
Check `Conflict: terminated by other getUpdates request` → kill 舊 instance。

**Q: 18:00 冇自動分析**
```
grep DAILY /root/bot.log
```
如果冇 output → 同 Bot 講一次 `/start` 註冊 chat ID。

**Q: Google 功能出 error**
```
/mystatus 睇授權狀態
```
如果冇授權 → 跟部署指南 Part B 做 OAuth。

**Q: 分析結果 rating 同預期唔同**
DeepSeek 每次分析獨立 run，rating 會跟 market sentiment 浮動。可以試多次 `/analyze` 對比。

---

## 檔案位置

| 檔案 | 本地 (Windows) | VPS |
|------|---------------|-----|
| Bot v2 | `.../workspace-files/hermes-mqtt-bridge/proma-bot-v2.py` | `/root/proma-bot.py` |
| Google module | `.../google_services.py` | `/root/google_services.py` |
| Proxy | `.../obsidian-write-proxy.py` | — |
| OAuth Setup | `.../google-oauth-setup.py` | — |
| Deploy Script | `.../deploy-vps.sh / deploy-vps.ps1` | — |
| 部署指南 | Obsidian `開發區/telegram-bot-v2-部署指南.md` | — |
| 本參考手冊 | Obsidian `開發區/telegram-bot-v2-參考手冊.md` | — |
