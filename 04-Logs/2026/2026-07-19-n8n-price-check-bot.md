# 2026-07-19 n8n Price Check Bot — Telegram 淘寶格價

## 摘要

成功建立第 7 個 n8n workflow：Telegram `/price` 命令 → SerpAPI Google Search → 淘寶/天貓商品查詢 → Telegram 回覆。過程中克服了 Telegram HTTPS webhook 限制、Python polling script 多重 debug、n8n node 回應格式等多項技術挑戰。

---

## 架構

```
Telegram @PriceChecker_K281_bot
  │  (user sends /price iPhone 15 128GB)
  ▼
Python polling script (VPS /opt/n8n/price-bot.py)
  │  (polls getUpdates, parses /price command)
  ▼
n8n Webhook (/webhook/price-check)
  │
  ├── Code (parse input)
  ├── HTTP Request (SerpAPI Google Search)
  ├── Code (format results)
  └── Telegram node (send reply)
```

---

## 克服的挑戰

| # | 挑戰 | 解決方案 |
|---|------|---------|
| 1 | Telegram Trigger 需 HTTPS，n8n HTTP only | 改用 Python 輪詢 Telegram getUpdates |
| 2 | Python bot 用錯 bot token（Hermes → PriceChecker） | 修正 token 指向新 bot |
| 3 | n8n Webhook 回應格式多次不對 | 多次調整 Code node 數據路徑 + Respond mode |
| 4 | SSH 連線不穩 | 部分操作由用戶在 VPS terminal 直接執行 |
| 5 | Code node 引用不存在的節點 | 改用 `$('Webhook').first().json` 直接引用 |
| 6 | HTTP Request `gl=us` 回美國結果 | 改為 `gl=hk` + `hl=zh-TW` |
| 7 | Tmall 搜尋結果較少 | 使用 `site:taobao.com OR site:tmall.com` 雙站搜尋 |

---

## 最終結果

✅ Telegram `/price iPhone 15 128GB` → 5 個淘寶商品鏈接（含價格與商店來源）→ 5 秒內回覆

---

## 今日所有 n8n Workflows

| # | Name | Trigger |
|---|------|---------|
| 1 | Stock Alert | VPS cron Mon-Fri 18:55 |
| 2 | Git Sync | Windows Task Mon-Fri 21:00 |
| 3 | Stock Price Push | VPS cron Mon-Fri 16:30 |
| 4 | Backup Health | VPS cron Daily 03:15 |
| 5 | N8N Self Monitor | VPS cron Every 30min |
| 6 | Kanban Health | VPS cron Daily 08:00, 18:00 |
| 7 | **Price Check** | **Telegram /price command** ← NEW |

---

## 待辦

- [ ] price-bot.py 轉為 systemd service（auto-start on reboot）
- [ ] 下次項目：n8n Ledger（記帳自動化）
