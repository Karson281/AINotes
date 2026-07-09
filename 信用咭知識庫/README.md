# 信用咭知識庫

> **由 Proma CEO 建立 · 2026-07-09**

---

## 目錄結構

```
信用咭知識庫/
├── README.md              ← 你而家睇緊呢份
├── raw/                   ← Karson 丟 raw data 嘅地方
│   ├── 信用咭回贈.md       （手動整理，自由格式）
│   └── *.md
├── DBS-LiveFresh.md       ← AI 轉換後的 Dataview 咭片
├── HSBC-EveryMile.md
├── BOC-Chill.md
├── AE-Platinum.md
└── ... (~20 張)
```

---

## 範圍

**只收錄現金回贈卡（cashback）。**
里數卡（如 HSBC EveryMile、AE Platinum）只有少數幾張，不由系統分析——使用者自行判斷使用時機。

---

## Raw Data 格式（自由格式）

你只需要按以下結構寫 raw data，AI 會自動轉換成 Dataview YAML：

```markdown
# 卡名 - 銀行

## 基本
- 網絡：Visa / Mastercard / Amex / UnionPay
- 年費：$0（永久免年費）/ $1,800（可 waiver）
- 有效日期：2026-01-01 至 2027-01-01

## 回贈
- 本地餐飲：X%
- 本地非餐飲：X%
- 本地網購：X%
- 外幣網購：X%
- 外幣簽帳：X%
- 內地簽帳：X%
- 機票酒店：X%

## 指定商店優惠
- 商店名：優惠內容，條件（如有）
- 萬寧：星期五 5% 回贈
- ESSO：入油 -$2/L

## 支付方式
- 實咭：✅/❌
- GPay：✅/❌
- BOC Pay：✅/❌ + 額外優惠（如有）
- 雲閃付：✅/❌
- AlipayHK：✅/❌
- WeChat Pay：✅/❌
- 網購咭號：✅/❌

## 消費限制
- 最低消費：$0（無）/ $1,300
- 月回贈上限：$0（無）/ $500
- 適用範圍：網購 / 全部 / 指定類別

## 外幣手續費
- X% （例如 1.95%）

## 特殊條件
- 任何非常規回贈規則
- 例如：BOC Pay 每月 8/18/28 日積分抵扣 85 折
- 例如：里數卡非現金回贈（HK$2 = 1 mile）
```

---

## AI 轉換規則

收到 raw data 後，AI 會：

1. 保留 `raw/` 原檔（唔修改）
2. 在 `信用咭知識庫/` 根目錄建立結構化 `.md`（每卡一個）
3. Frontmatter 格式跟 Template v3 標準
4. 自動判斷 `active: Y/N`（根據有效日期）
5. 自動 normalize 回贈率為數字（例如 `5%` → `5.0`）

---

## 轉換指令

當你丟完 raw data 後，叫 Hermes 或 Proma：

```
請讀取 信用咭知識庫/raw/ 入面所有檔案，
按 Agent-架構/03 入面嘅 Template v3 格式，
轉換為結構化 Dataview 咭片，存入 信用咭知識庫/ 根目錄。
每張卡一個獨立 .md 檔案。
```
