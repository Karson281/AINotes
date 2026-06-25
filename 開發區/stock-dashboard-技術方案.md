---
type: architecture-proposal
title: Stock Dashboard on Obsidian — 技術方案
created: 2026-06-24
status: draft
---

# Stock Dashboard on Obsidian

## 目標
將 02-Wiki/Stocks/ 目錄下嘅分析報告，聚合展示成一個一目瞭然嘅 Dashboard，顯示：
- Watchlist 總覽（所有股票 + 最新評級）
- 評級分佈（建倉/加倉/觀察/觀望 各幾多）
- 重點關注（建倉買入股票列表）
- 股價 / RSI / 息率 對比表
- 每日 log timeline

## 現有資料結構

每份報告嘅 YAML frontmatter：
```yaml
---
type: stock-analysis
ticker: 0941.HK
date: 2026-06-23
rating: 加倉買入
status: completed
source: telegram-bot-v2
---
```

報告內容用固定格式 header：
```
【評級】：xxx
【技術面】：均線、MACD、RSI、成交量
【基本面】：盈利、估值、股息率
【策略】：入場區間、目標價、止損位
```

## 方案對比

### 方案 A：Obsidian Bases（推薦 ⭐）
Bases 係 Obsidian 原生資料庫插件，你已經裝咗。

**做法：**
1. 開新 Note `02-Wiki/Stock-Dashboard.md`
2. Insert → Bases → 揀 Sources 為 `02-Wiki/Stocks/`
3. 設定顯示欄位：
   - `ticker` — 股票代號
   - `rating` — 評級（用 color tag）
   - `date` — 分析日期
   - `source` — 來源
4. 可以 group by `rating`、sort by `date`

**優點：** 零 coding、即開即用、支援 filter/sort/group
**缺點：** 只能在 Obsidian desktop 睇，Telegram 睇唔到

### 方案 B：Markdown 聚合表（手動）
每次 /analyze 後，Bot 自動生成一個 summary markdown table：

```markdown
# Stock Dashboard — 2026-06-24

| 股票 | 評級 | 現價 | RSI | 息率 | 目標價1 |
|------|:----:|:----:|:---:|:----:|:-------:|
| 0941.HK | 🟢 加倉買入 | 59.80 | 62.5 | 6.8% | 68.00 |
| 0823.HK | 🟢 加倉買入 | 35.74 | 9.4 | 7.0% | 42.00 |
| 0005.HK | 🟡 密切觀察 | 144.00 | 55.0 | 4.0% | 160.70 |
```

**做法：** Bot 每次 /analyze 時提取關鍵數據，append 一行去 Stock-Dashboard.md

**優點：** Telegram 都睇到、歷史紀錄完整、簡單直接
**缺點：** 要改 Bot code 加 extract 邏輯

### 方案 C：DataviewJS（如果你轉用 Dataview）
```dataviewjs
const stocks = dv.pages('"02-Wiki/Stocks"')
  .where(p => p.rating)
  .groupBy(p => p.rating)
  .map(g => [g.key, g.rows.length])
```
需要裝 Dataview plugin，同 Bases 有啲重疊。

## 推薦做法：Bases + 自動 Table 雙管齊下

| Layer | 工具 | 用途 |
|-------|------|------|
| **Dashboard 主頁** | Obsidian Bases | 互動式瀏覽、filter、sort |
| **每日快照** | Telegram Bot → MD table | 每次 /analyze 自動 append 一行 |
| **History Log** | 已經有 format | Stock-History-Log table |

### Step 1：Bases Dashboard（即時做到）
開新 note → Insert Bases → 揀 `02-Wiki/Stocks/` 做 source
加 fields: `ticker`, `rating`, `date`
Group by `rating` → 即刻有靚靚 dashboard

### Step 2：Bot 自動 Table（要改 code）
每次 /analyze 時 extract 關鍵數據，寫入 `02-Wiki/Stock-Dashboard.md`：

```markdown
## 2026-06-24 分析結果
| 股票 | 評級 | 
|------|:----:|
| 0941.HK | 🟢 加倉買入 |
| 0005.HK | 🟡 密切觀察 |
```

### Step 3：History Timeline（可選）
Bot 幫你每日 append Stock-History-Log table 嘅一行，建立股價 + 評級變遷紀錄。

## 目前進度

- [x] Stock analysis reports 已標準化 YAML frontmatter
- [x] Bot /analyze 已有完整資料
- [ ] 開 Stock-Dashboard.md（等你用 Bases set up）
- [ ] Bot 自動 append summary table（你要我改 code 就出聲）
