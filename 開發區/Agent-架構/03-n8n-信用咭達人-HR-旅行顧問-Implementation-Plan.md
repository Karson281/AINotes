# n8n 三大場景 Implementation Plan

**日期：2026-07-09** | **作者：Proma Agent (CEO)** | **執行：Hermes Agent + n8n**

> 此文件為多方持分者共享 — Karson（人類決策者）、Hermes Agent（VPS 執行者）、Proma Agent（CEO 監察者）

---

## 架構總覽

```
┌─────────────────────────────────────────────────┐
│                    Telegram                       │
│         新 Bot (n8n 專用，獨立 Token)             │
│         舊 Bot (Hermes 專用，格價+閒聊+股票)      │
└──────────────────────┬──────────────────────────┘
                       │ Webhook
                       ▼
┌─────────────────────────────────────────────────┐
│                 n8n (VPS)                        │
│              n8n.tatyan.com                      │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │        AI Node: 意圖分類                  │    │
│  │  DeepSeek Flash · 低成本 · 快速路由       │    │
│  └────────────┬────────────────────────────┘    │
│               │                                   │
│     ┌─────────┼─────────┬──────────┐             │
│     ▼         ▼         ▼          ▼             │
│  信用咭    HR求職   旅行顧問    Simple QA         │
└──────┬───────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────┐
│            Obsidian Vault                        │
│                                                  │
│  信用咭知識庫/    ← 結構化 Dataview 咭片          │
│  求職記錄/        ← HR job 追蹤                  │
│  旅行記錄/        ← 行程偏好                      │
└─────────────────────────────────────────────────┘
```

---

## Part 1: 信用咭達人（核心場景）

### 1.1 五步篩選引擎

```
用戶 Telegram 提問
          │
          ▼
┌─────────────────────────────────────────┐
│ Step 1: AI 摘取關鍵欄位                   │
│  amount, spend_mode, merchant, pay_method│
└────────────┬────────────────────────────┘
             ▼
┌─────────────────────────────────────────┐
│ Step 2: n8n 讀取 Vault 咭片              │
│  FILTER: active=Y, 日期有效              │
│  IF amount < $1300 → 排除 spend_min>0   │
└────────────┬────────────────────────────┘
             ▼
┌─────────────────────────────────────────┐
│ Step 3: 商戶特殊優惠覆蓋                  │
│  merchant_specific > general cashback    │
└────────────┬────────────────────────────┘
             ▼
┌─────────────────────────────────────────┐
│ Step 4: 支付方式匹配                      │
│  商戶支援 ∩ 咭片支援 + 疊加 bonus         │
└────────────┬────────────────────────────┘
             ▼
┌─────────────────────────────────────────┐
│ Step 5: 排名 + 消費限制檢查               │
│  net = amount×rate% + bonus - fee       │
│  check spend_cap 冇爆                    │
└────────────┬────────────────────────────┘
             ▼
         Telegram 回覆 Top 3
```

### 1.2 消費模式 — 七大場景

| 模式    | 英文 key            | 觸發條件            | 例子                   |
| :---- | :---------------- | :-------------- | :------------------- |
| 本地餐飲  | `local_dining`    | 香港餐廳、食肆、快餐、茶記   | 「大家樂 $50」            |
| 本地非餐飲 | `local_retail`    | 香港購物、超市、油站、服務   | 「萬寧 $80」「ESSO 入油」    |
| 本地網購  | `local_online`    | 香港網上商店          | 「HKTVmall $500」      |
| 外幣網購  | `overseas_online` | 外國網站、USD/EUR 結算 | 「Amazon US $200 USD」 |
| 外地簽帳  | `overseas_pos`    | 海外實體店           | 「日本藥妝店 ¥5000」        |
| 內地簽帳  | `cn_pos`          | 深圳、廣州 CNY 結算    | 「深圳食飯 ¥300」          |
| 機票酒店  | `travel`          | 航空公司、酒店、OTA     | 「Agoda 訂東京酒店」        |

### 1.3 查詢範例全覆蓋

| #   | 用戶提問                      | spend_mode      | merchant | 預期結果                                      |
| :-- | :------------------------ | :-------------- | :------- | :---------------------------------------- |
| 1   | 「$1500 網購用邊張卡？」           | local_online    | null     | DBS Live Fresh 6% = $90                   |
| 2   | 「萬寧 $80 點俾？」              | local_retail    | 萬寧       | Citi Cash Back (星期五 5%) vs HSBC EveryMile |
| 3   | 「深圳 $500 食飯」              | cn_pos          | null     | BOC Chill + 雲閃付 疊加 ~10%                   |
| 4   | 「Amazon US $200 USD 電子產品」 | overseas_online | null     | DBS Live Fresh 6% - 1.95% fee             |
| 5   | 「ESSO 入油 $800 星期五」        | local_retail    | ESSO     | Citi Cash Back 獨家 -$2/L                   |
| 6   | 「用 BOC Pay 俾錢，邊張最抵？」      | (由 AI 判斷)       | null     | 只掃 bocpay=Y 嘅卡                            |
| 7   | 「日本旅行機票 $6000」            | travel          | null     | HSBC EveryMile HK$2=1mile                 |

### 1.4 消費下限 $1,300 分界規則（重要）

```
用戶消費金額
    │
    ├─ < $1,300 → 排除所有 spend_min > 0 的咭片
    │   （呢啲卡有最低消費要求，細額簽帳根本唔會達標）
    │
    └─ ≥ $1,300 → 納入有 spend_min 的咭片
        但只推薦 spend_min ≤ 消費金額 的卡
        （未達最低消費的仍然排除）
```

**例子**：
- 用戶 $500 網購 → 排除 AE Platinum（spend_min=$0，但此卡網購回贈低，自然排名低）
- 用戶 $3,000 海外簽帳 → 納入所有卡，但 spend_min=$5,000 的卡仍排除（未達標）

### 1.5 外幣簽帳規則 — DCC 陷阱防護

```
外幣簽帳 (overseas_pos) 或外幣網購 (overseas_online)
    → AI 必須提醒用戶：
       「⚠️ 必須用當地貨幣結算，拒絕 DCC（動態貨幣轉換）。
         否則會被收取額外 3-5% 手續費 + 喪失外幣回贈資格。」
    
本地網購 (local_online)
    → AI 必須提醒：
       「先確認商戶是香港註冊，才用港幣結算。
        外國網站（如 Amazon US）= overseas_online，唔係 local_online。」
```

### 1.6 特殊回贈條件處理

部分咭片有非常規回贈規則，不能單靠 `rate%` 表達。在 `special_rules` 欄位描述，AI 需在推薦時引用：

```yaml
special_rules:
  - "BOC Pay：每月 8 日、18 日、28 日積分抵扣 85 折"
  - "指定商戶消費需主動登記優惠才生效"
  - "回贈以里數計算，非現金（HK$2 = 1 mile）"
```

---

## Part 2: HR 求職顧問

### 2.1 Workflow

```
[Cron Trigger 09:00 + 14:00]
    → [HTTP: SerpAPI / Firecrawl]
    → [AI: 篩選匹配職位]
    → [AI: 格式化摘要]
    → [Telegram Push] + [Write Obsidian 求職記錄/]
```

### 2.2 搜尋條件（待你定義）

```
關鍵詞: "part-time", "兼職", "freelance"
行業: 科技 / 顧問 / 教育 / 翻譯 / 設計
地區: 香港 / Remote
平台: JobsDB, LinkedIn, Indeed, HKGoodJobs
薪資: 時薪 ≥ $X
```

---

## Part 3: 旅行顧問

輕量 Telegram 查詢，n8n AI node 處理：

```
用戶：「我想去東京 5 日，邊張卡最好？」
  → AI 摘取：destination=東京, duration=5日
  → 咭片掃描：overseas_pos + travel + foreign_fee
  → 推薦：HSBC EveryMile（機票酒店 HK$2=1mile）+ AE Platinum（保險+貴賓室）
```

---

## Part 4: 角色分工

| 角色                | 實體             | 負責                                        |
| :---------------- | :------------- | :---------------------------------------- |
| **人類決策者**         | Karson         | 定義需求、提供咭片 raw data（~20 張）、最終審批              |
| **CEO 監察**        | Proma (Pro)    | 架構設計、品質評鑑、危機處理、監察 compliance              |
| **Manager 執行**    | Hermes (Flash) | n8n workflow 建立、VPS infra、Telegram Bot 管理 |
| **股票達人**          | Hermes (Flash) | 每日 18:00 股票分析 → Telegram + Vault            |
| **Secretary 自動化** | n8n (Flash)    | Telegram 路由、信用咭查詢、HR 排程、旅行推薦              |
| **知識庫**           | Obsidian Vault | 咭片數據（~20 張）、求職記錄、旅行偏好、股票報告                |

---

## 實施路線

### Phase 1 — 基建（Hermes 今日）
- [ ] 建立 Telegram Bot for n8n（經 @BotFather，獨立 Token）
- [ ] n8n 連接 Telegram Bot（Webhook node）
- [ ] 測試：Telegram → n8n → echo 回覆
- [ ] n8n 配置 DeepSeek Flash AI node

### Phase 2 — 咭片數據化（Karson 1-2 天）
- [ ] 建立 `信用咭知識庫/` 目錄 on Vault
- [ ] 將信用咭回贈.pdf 內容整理為原始 Markdown
- [ ] AI 轉換為 Dataview 結構化格式（按 Template v3）
- [ ] 建立 5 張主力咭片 frontmatter

### Phase 3 — 信用咭查詢（Hermes 2-3 天）
- [ ] n8n Workflow: Telegram → 意圖分類 → 信用咭 route
- [ ] AI Node 1: 欄位摘取（見 Prompt A）
- [ ] HTTP Node: Read Obsidian Vault 咭片
- [ ] AI Node 2: 排名計算（見 Prompt B）
- [ ] 測試 7 個查詢範例

### Phase 4 — HR 求職（Hermes 1 天）
- [ ] Cron trigger 設定 (09:00 + 14:00)
- [ ] SerpAPI / Firecrawl search 整合
- [ ] Telegram push + Obsidian 記錄

### Phase 5 — 旅行顧問（Hermes 1 天）
- [ ] 旅行查詢 workflow
- [ ] 偏好讀取 + 推薦邏輯

---

## 附錄 A：咭片 Template v3

```yaml
---
card_name: "DBS Live Fresh"
bank: "DBS"
card_network: mastercard
annual_fee: 0
effective_date: 2026-01-01
expiry_date: 2027-01-01
active: Y

cashback:
  local_dining: 0.4
  local_retail: 0.4
  local_online: 6.0
  overseas_online: 6.0
  overseas_pos: 0.4
  cn_pos: 0.4
  travel: 0.4

merchant_specific:
  - store: 百佳
    rate: 8.0
    condition: "星期五"
    expiry: 2026-12-31
  - store: HKTVmall
    rate: 10.0
    condition: "每月 8 號"

payment_methods:
  physical_card: Y
  card_number: Y
  gpay: Y
  gpay_bonus: 0
  bocpay: N
  unionpay: N
  alipayhk: Y
  alipayhk_bonus: 0
  wechatpay: Y
  wechatpay_bonus: 0

spend_min: 0
spend_cap_monthly: 500
spend_cap_scope: "網購"
spend_min_note: "無最低消費要求"
foreign_transaction_fee: 1.95

special_rules:
  - "網購只限電子商戶 MCC (網上交易)"
  - "每月 8 號 HKTVmall 10% (上限 $100)"
  - "BOC Pay 每月 8/18/28 日積分抵扣 85 折（如適用）"

tags: [online_shopping, cashback, no_annual_fee]
best_for: ["本地網購", "外幣網購"]
---
```

## 附錄 B：n8n AI Prompts

### Prompt A — 欄位摘取

```
你係一個信用咭查詢分類器。根據用戶訊息，摘取欄位並回傳 JSON。

## 消費模式分類
- local_dining：香港餐廳、食肆、快餐
- local_retail：香港購物、超市、油站
- local_online：香港網上商店
- overseas_online：Amazon US、外國網站
- overseas_pos：海外實體店簽帳
- cn_pos：深圳、內地 CNY 結算
- travel：機票、酒店

## 支付方式識別
GPay / BOC Pay / 雲閃付 / AlipayHK / 微信 / 實咭 / 咭號

## 回傳 JSON
{
  "intent": "credit_card_query",
  "amount_hkd": 金額或null,
  "spend_mode": "分類",
  "merchant": "商戶名或null",
  "pay_method": "支付方式或null",
  "day_of_week": "星期X"
}
```

### Prompt B — 咭片排名

```
你係信用咭回贈計算專家。根據查詢條件排名。

## 計算規則
1. 基礎回贈 = amount × cashback.{spend_mode}%
2. merchant 匹配 merchant_specific → 用 special rate
3. pay_method_bonus → 疊加
4. foreign_transaction → 扣減 fee
5. check spend_cap 是否爆

## 輸出格式
🏆 **$XXX 消費回贈推薦**
1. **[卡名]** → ~HK$XX（X%）
   💡 原因
2. **[卡名]** → ~HK$XX（X%）
⚠️ 注意事項
```

---

*此文件由 Proma Agent (CEO) 撰寫，存放於 Obsidian Vault Agent-架構/ 供多方參閱。*
*最後更新：2026-07-09*
