---
card_name: "Travel+ VS Visa"
bank: "Standard Chartered"
spend_mode: "實咭 / GPay"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-08-11
new_balance: 0
foreign_transaction_fee: 1.95

cashback:
  local_dining: 5.0
  local_retail: 0
  local_online: 0
  overseas_online: 0
  overseas_pos: 7.0
  cn_pos: 7.0
  travel: 7.0

merchant_specific:
  - store: "日本、南韓、泰國、內地、澳門及台灣實體商店"
    rate: 7.0
    condition: "實咭/GPay"
    expiry: 2026-12-31

payment_methods:
  physical_card: Y
  card_number: N
  gpay: Y
  gpay_bonus: 0
  bocpay: N
  unionpay: N
  alipayhk: N
  wechatpay: N

scenarios:
  - spend_mode: overseas_pos
    pay_method: [physical_card, gpay]
    rate: 7.0
    cap: 7576
    spend_min: 6000
    note: "日本/南韓/泰國/內地/澳門/台灣實體店"
  - spend_mode: local_dining
    pay_method: [physical_card, gpay]
    rate: 5.0
    cap: 10000
    spend_min: 6000
    note: "本地餐飲"

spend_min: 6000
spend_cap_monthly: 7576

special_rules:
  - "消費下限 $6,000"
  - "FCC 1.95%"

tags: [travel, overseas_pos, dining, gpay]
best_for: ["日本旅行", "南韓旅行", "外地簽帳", "本地餐飲"]
---

# Travel+ VS Visa

| 場景 | 回贈率 | 地區 | 月上限 | 消費下限 |
|------|--------|------|--------|----------|
| 外地簽帳 | **7%** | 日/韓/泰/中/澳/台 | $7,576 | $6,000 |
| 本地餐飲 | 5% | 香港 | $10,000 | $6,000 |

- **支付**: 實咭/GPay
- **FCC**: 1.95%
- **截數日**: 每月 11 日
