---
type: work-log
date: 2026-06-26
tags: 
  - obsidian
  - dashboard
  - stock
  - git
  - vps
  - proma-bot
---

#  工作日誌 — 股票 Dashboard 全線打通

**日期**：2026-06-25 ~ 2026-06-26  
**耗時**：約 2 天  
**狀態**：✅ 全線打通

---

## 完成項目

### 1. Obsidian 股票 Dashboard
- **純 DataviewJS 版本**，無需 Dashboards 插件
- 組合概況（6 格統計卡片）
- 今日分析（彩色評級卡片，自動按最新日期篩選）
- 股票總表（每隻最新評級，按評級排序）
- 市場指數 K 線圖（恒指 + 納指）
- CSS 樣式（彩色評級標籤、響應式設計）

### 2. 推送腳本（`scripts/proma_push_script.py`）
- 中文 URL 編碼修正
- 檔名格式：`YYYYMMDD-TICKER.md`
- API Key 已設定

### 3. VPS Bot 修復
- **Bug 修復**：`write_obs()` 在 Obsidian 離線時仍存本機
- systemd 服務重啟
- 每日 18:00 HKT 自動分析 19 隻股票

### 4. Git 同步
- 本機 Vault → GitHub（已連通）
- VPS Vault → GitHub（已連通）
- `.gitignore` 設定
- Obsidian Git 錯誤消除

---

## 檔案結構

```
Vault (D:\kaisu\Google Drive\AINotes)
─ 02-Wiki/
│   ├── Stocks/              ← 數據源（Hermes / proma-bot 每日推送）
│   ├── 01_投資組合總覽.md    ← 主 Dashboard
│   ├── 02_個股分析.md        ← 個股頁面
│   ├── 03_交易日誌.md        ← 交易日誌
│   ├── Stock-Dashboard.base  ← Bases 設定
│   └── Stock-Task-List      ← 待分析清單
├── .obsidian/snippets/
│   └── stock-callouts.css    ← CSS 樣式
└── scripts/
    └── proma_push_script.py  ← 推送腳本
```

---

## 有待改進

- [ ] Tab Pages 個股深入數據（方案 B）
- [ ] 策略摘要自動化
- [ ] 歷史趨勢圖（Obsidian Charts）
- [ ] 主題適配優化

---

## 技術細節

### VPS 端
- **主機**：srv1740946 (Ubuntu 22.04)
- **Bot**：`proma-bot.py`（Telegram Bot + DeepSeek API）
- **服務**：systemd `proma-bot.service`
- **排程**：每日 10:00 UTC = 18:00 HKT
- **分析**：DeepSeek Chat API，19 隻股票
- **同步**：Git → GitHub → 本機 Obsidian

### 數據流
```
VPS (proma-bot) 18:00 HKT
  → DeepSeek API 分析 19 隻股票
  → 存檔 /root/vault/02-Wiki/Stocks/
  → Git Push → GitHub
  → 本機 Git Pull → Obsidian
  → Dashboard DataviewJS 即時更新
```
