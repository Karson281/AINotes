# 2026-07-20 n8n Ledger 記帳系統 + Price Bot 完善

## 摘要

建立第 8 個 n8n workflow：Telegram `/log` 命令 → Google Sheets append → Telegram reply。完成 n8n operations hub 最終形態——7 個 workflow + 2 個 Telegram bot 全部運行。

---

## Ledger Workflow（第 8 個 workflow）

### 架構
```
Telegram @PriceChecker_K281_bot
  │  user sends /log 超市 百佳買餸 $168 八達通
  ▼
Python polling script (price-bot.py)
  │  polls getUpdates, parses /log command
  ▼
n8n Webhook (/webhook/Ledger)
  │
  ├── Code: parse command → date, category, item, amount, payment, card
  ├── Google Sheets: Append Row → n8n-expenditure
  ├── Code: format reply text
  └── Telegram: send confirmation
```

### 技術細節
- **Google Sheets credential**: Service Account (n8n-ledger@consummate-rush...)
- **Sheet ID**: 1QxeqTKtnwCxbWGJ4Mw1SUP8uvrdtB7P2jWJXnBSz5KU
- **Sheet name**: sheet1
- **Tab headers**: Date | 類別 | 項目 | 金額 | 支付方式 | 信用咭 | 備註
- **Bot**: @PriceChecker_K281_bot (systemd service)
- **Python bot**: /opt/n8n/price-bot.py (fire-and-forget pattern)

### 克服的挑戰
| # | 問題 | 解決方案 |
|---|------|---------|
| 1 | Telegram Trigger 需 HTTPS | 改用 Python polling script |
| 2 | Bot token 錯誤 | 建立新 bot + 修正 script |
| 3 | n8n localhost:5678 連接失敗 | 改為 10.99.99.1:5678 |
| 4 | Google Sheets credential 格式 | 用 Service Account JSON |
| 5 | Sheet dropdown "No results" | Enable Sheets API + share sheet |
| 6 | "Append or Update" vs "Append Row" | 改用 Define Below 模式 |
| 7 | Code node 引用不存在的節點 | 改用 $('Webhook').first().json |
| 8 | payment 欄位缺失 | Code1 需 return 所有 fields |

---

## 最終 n8n Workflows（8 個）

| # | Name | Trigger | Purpose |
|---|------|---------|---------|
| 1 | Stock Alert | VPS cron 18:55 | Monitor Hermes reports |
| 2 | Git Sync | Windows Task 21:00 | Sync work logs |
| 3 | Stock Price Push | VPS cron 16:30 | 27 stock prices |
| 4 | Backup Health | VPS cron 03:15 | Verify dumps |
| 5 | N8N Self Monitor | VPS cron */30min | Check n8n alive |
| 6 | Kanban Health | VPS cron 08:00, 18:00 | Task counts |
| 7 | Price Check | Telegram /price | Taobao/Tmall search |
| 8 | **Ledger** | **Telegram /log** | **記帳 → Google Sheets** |

## Telegram Bots

| Bot | Token | Purpose |
|-----|-------|---------|
| @Stock_K281_bot | 8623443686:... | n8n notifications |
| @PriceChecker_K281_bot | 8657011042:... | /price + /log commands |

## systemD Services

| Service | Status |
|---------|--------|
| price-bot.service | enabled + running (auto-restart) |

## Google Cloud

| Resource | Detail |
|----------|--------|
| Project | consummate-rush-500205-r2 |
| Service Account | n8n-ledger@... |
| API | Google Sheets API (enabled) |

---

## 今日所有 Token Savings

| 原 Proma automation | 新方案 | Token Saved |
|---------------------|--------|-------------|
| 監察 Hermes 股市報告 | n8n Stock Alert | ✅ |
| Git Pull 股票報告 | VPS cron | ✅ |
| Git Sync 工作日誌 | n8n Git Sync + Windows Task | ✅ |
| **合計** | **3 個 AI agent → n8n** | **~5 min AI/day** |

Plus: Price Check + Ledger 全零 token，完全由 n8n + Python script 接管。
