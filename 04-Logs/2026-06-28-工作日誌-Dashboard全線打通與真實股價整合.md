---
type: work-log
date: 2026-06-28
tags:
  - obsidian
  - dashboard
  - stock
  - yfinance
  - vps
  - github
status: completed
---

#  工作日誌 — Dashboard 全線打通與真實股價整合

**日期**：2026-06-28（週日）  
**耗時**：約 3.5 小時  
**狀態**：✅ 全部打通

---

## 背景

Dashboard 在 2026-06-25 建立後存在多個問題：
- 股價全為 AI 偽造
- Dashboard 日期格式亂碼
- VPS 離線不存檔
- Git sync 衝突不斷
- K 線圖太大
- 指數重複顯示

## 解決方案

### 1. 真實股價整合（yfinance）
- 在 VPS 安裝 `yfinance` 套件
- 分析前先抓取真實股價
- 直接寫入 frontmatter `price` 欄位
- Dashboard 自動讀取顯示

### 2. Dashboard 日期格式修復
- 自訂 `getDate()` 函數兼容兩種日期格式（`2026-06-28` 和 `20260628`）
- 應用到所有 3 個 DataviewJS 區塊（總覽、卡片、總表）

### 3. VPS stock_daily.py 獨立腳本
- 獨立運行，無需 Telegram
- 含 yfinance 真實股價 + DeepSeek AI 分析
- 自動清理舊報告（成功 ≥50% 才刪）
- 自動 Git push

### 4. Git 同步修復
- VPS → GitHub 多輪衝突修復（rebase + force sync）
- 本機 ← GitHub 正常 pull
- Token 更新

### 5. K 線圖移除
- 因 Stock Blocks 無法縮小，改用文字指數顯示
- CSS 清理

### 6. 指數顯示
- 用 yfinance history API 抓取真實指數
- 恒指：22671.86
- 納指：25297.62

---

## Dashboard 最終結構

```
01_投資組合總覽.md
├── 導航按鈕（個股分析 / 交易日誌）
├── 市場指數（恒指 22671 / 納指 25297）
├── 每日策略摘要
├── 組合概況（6 格統計卡片）
├── 今日分析（彩色評級卡片 + 真實股價）
└── 股票總表（代碼 / 股價 / 評級 / 狀態 / 日期）
```

## 所需插件

| 插件 | 用途 | 狀態 |
|------|------|------|
| Dataview | 數據查詢與渲染（JS 查詢已開啟） | ✅ |
| Buttons | 頁面導航 | ✅ |
| Homepage | 啟動頁（設為 Dashboard） | ✅ |
| Obsidian Git | Git 同步 | ✅ |

**不再需要**：Dashboards、Stock Blocks

---

## 系統流程

```
VPS 18:00 HKT（stock_daily.py）
  → yfinance 抓真實股價 + 指數
  → DeepSeek API 分析
  → 寫入 02-Wiki/Stocks/YYYYMMDD-TICKER.md
  → 寫入 index-HSI.md + index-IXIC.md
  → Git Push → GitHub
  → 本機 Git Pull → Obsidian
  → Dashboard DataviewJS 即時更新
```

---

## 待改進

- [ ] Tab Pages 個股深入數據（方案 B）
- [ ] 每日指數自動抓取整合到 stock_daily.py 排程
- [ ] 策略摘要自動化
- [ ] 歷史趨勢圖
