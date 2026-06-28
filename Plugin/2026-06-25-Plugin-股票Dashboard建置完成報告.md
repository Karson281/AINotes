---
type: plugin-doc
status: completed
updated: 2026-06-25
tags:
  - obsidian
  - dashboard
  - dataview
  - stock
---

#  Plugin — 股票 Dashboard 建置完成報告

> **狀態**：✅ 已成功部署  
> **日期**：2026-06-25  
> **耗時**：約 2 小時  
> **維護者**：Proma Agent

---

## 完成項目

### 1. 純 DataviewJS Dashboard（`02-Wiki/01_投資組合總覽.md`）

完全移除 Dashboards 插件依賴，改用 DataviewJS + CSS Grid 渲染。

**功能清單**：
- 導航按鈕（Buttons 插件）
- 每日策略摘要（手動更新）
- 組合概況（6 格統計卡片：追蹤數、今日分析數、各評級數量）
- 今日分析（彩色卡片網格，自動按最新日期篩選）
- 股票總表（每隻最新評級，按評級排序，自動去重 per ticker）
- 市場指數 K 線圖（Stock Blocks 插件）

**所需插件**：
| 插件 | 用途 | 狀態 |
|------|------|------|
| Dataview | 數據查詢與渲染 | 已安裝，JS 查詢已開啟 |
| Stock Blocks | K 線圖 | 已安裝 |
| Buttons | 頁面導航 | 已安裝 |
| Homepage | 啟動頁 | 已安裝，已設定 |
| Local REST API | 接收推送 | 已安裝 |

### 2. 個股分析頁（`02-Wiki/02_個股分析.md`）

- K 線圖顯示（修改 `symbol` 切換股票）
- 最新分析摘要（DataviewJS 自動讀取）
- 快速筆記區

### 3. 交易日誌（`02-Wiki/03_交易日誌.md`）

- 手動記錄或 Journalit 插件整合
- 導航按鈕

### 4. CSS 樣式（`.obsidian/snippets/stock-callouts.css`）

- 彩色評級標籤（綠/橙/灰/紅）
- 統計卡片網格
- 評級卡片網格
- 股票總表樣式
- K 線圖網格
- 響應式設計

### 5. 推送腳本（`scripts/proma_push_script.py`）

- 中文 URL 編碼修正
- 檔名格式：`YYYYMMDD-TICKER.md`
- Frontmatter 與現有數據格式一致
- API Key 已設定

### 6. Bases 設定（`02-Wiki/Stock-Dashboard.base`）

- 讀取 `02-Wiki/Stocks/` 資料夾
- 篩選 `type = "stock-analysis"`
- 4 個視圖：全部記錄、買入評級、密切觀察、最新分析
- 可作為 DataviewJS 的備援方案

---

## 使用說明

### 日常使用

1. **打開 Dashboard**：Obsidian 啟動時自動開啟 `02-Wiki/01_投資組合總覽`
2. **查看今日分析**：彩色卡片顯示最新評級
3. **查看總表**：滾動到「股票總表」查看所有股票最新狀態
4. **查看 K 線圖**：滾動到「市場指數」查看恒指/納指走勢

### 修改組合

**新增股票**：
```bash
# Hermes 自動推送，或手動建立檔案
# 檔名格式：YYYYMMDD-TICKER.md
# 位置：02-Wiki/Stocks/
```

**移除股票**：刪除 `02-Wiki/Stocks/` 下對應檔案

**修改評級**：直接編輯 `Stocks/` 下的 `.md` 檔案 frontmatter

### 每日 18:00 自動更新流程

```
Hermes (VPS) 18:00 觸發
    ↓
掃描投資組合（Stock-Task-List）
    ↓
抓取技術指標 + 基本面數據
    ↓
生成分析報告（frontmatter + 正文）
    ↓
Proma Agent 推送至 02-Wiki/Stocks/
    ↓
Dashboard 即時更新（DataviewJS 自動讀取）
```

### 插件設定修改

- **Dataview**：設定 → 開啟 `Enable JavaScript Queries`
- **Stock Blocks**：無需設定，直接寫代碼
- **Buttons**：無需設定，直接寫代碼
- **Homepage**：設定 → File → `02-Wiki/01_投資組合總覽.md`
- **CSS Snippet**：設定 → 外觀 → CSS 程式碼片段 → 開啟 `stock-callouts`

---

## 有待優化項目

### 高優先級

- [ ] **今日 18:00 驗證**：確認 Hermes 推送後 Dashboard 是否正確更新
- [ ] **個股分析頁動態化**：目前 `symbol` 需手動修改，可改為 DataviewJS 下拉選單動態切換
- [ ] **策略摘要自動化**：目前為手動文字，可改為讀取 Hermes 生成的策略筆記

### 中優先級

- [ ] **歷史趨勢圖**：用 Obsidian Charts 繪製評級變化趨勢
- [ ] **績效追蹤**：記錄每次買入/賣出價格，計算損益
- [ ] **通知整合**：評級變更時發送 Telegram/Email 通知
- [ ] **Bases 與 DataviewJS 整合**：Bases 可編輯 frontmatter，DataviewJS 負責渲染，兩者互補

### 低優先級

- [ ] **主題適配**：測試不同 Obsidian 主題下的顯示效果
- [ ] **行動裝置優化**：手機版 Dashboard 佈局調整
- [ ] **多語言支援**：如需切換中英文界面
- [ ] **Journalit 整合**：交易日誌頁面嵌入 Journalit Dashboard

---

## 檔案結構

```
Vault (D:\kaisu\Google Drive\AINotes)
├── 02-Wiki/
│   ├── Stocks/              ← 數據源（Hermes 每日推送）
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

## 備註

- 本 Dashboard 為**純 DataviewJS 版本**，不依賴 Dashboards 插件
- 所有數據讀取自 `02-Wiki/Stocks/` 資料夾
- 每日 18:00 Hermes 自動推送更新
- 組合管理：增刪 `Stocks/` 資料夾中的檔案即可
