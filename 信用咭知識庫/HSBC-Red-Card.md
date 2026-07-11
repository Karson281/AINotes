---
card_name: "HSBC Red Card"
bank: "HSBC"
spend_mode: "實咭"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-07-20
new_balance: 0
foreign_transaction_fee: 0

cashback:
  local_dining: 0
  local_retail: 0
  local_online: 4.0
  overseas_online: 4.0
  overseas_pos: 0
  cn_pos: 0
  travel: 0

  # local_dining/retail 8% 只限指定商戶+實咭，見 merchant_specific
  # 設為 0 避免誤導

merchant_specific:
  - store: "香港壽司郎"
    rate: 8.0
    condition: "實咭"
  - store: "譚仔三哥米線"
    rate: 8.0
    condition: "實咭"
  - store: "譚仔雲南米線"
    rate: 8.0
    condition: "實咭"
  - store: "Bakehouse"
    rate: 8.0
    condition: "實咭"
  - store: "Decathlon Hong Kong"
    rate: 8.0
    condition: "實咭"
  - store: "NAMCO"
    rate: 8.0
    condition: "實咭"
  - store: "TAITO STATION"
    rate: 8.0
    condition: "實咭"
  - store: "Sephora"
    rate: 8.0
    condition: "實咭"
  - store: "@cosme STORE"
    rate: 8.0
    condition: "實咭"
  - store: "3COINS"
    rate: 8.0
    condition: "實咭"

payment_methods:
  physical_card: Y
  card_number: N
  gpay: N
  gpay_bonus: 0
  bocpay: N
  unionpay: N
  alipayhk: N
  wechatpay: N

scenarios:
  - spend_mode: local_pos
    pay_method: [physical_card]
    rate: 8.0
    cap: 1250
    spend_min: 0
    note: "指定商戶：壽司郎、譚仔、Bakehouse、Decathlon 等"
  - spend_mode: local_online
    pay_method: [physical_card]
    rate: 4.0
    cap: 10000
    spend_min: 0
    note: "本地網購/外幣網購"

spend_min: 0
spend_cap_monthly: 1250

special_rules:
  - "本地簽帳 8% 只限指定商戶（壽司郎、譚仔、Bakehouse、Decathlon 等）"
  - "網購 4% FCC 1.95%（外幣）"

tags: [dining, local_pos, cashback]
best_for: ["指定餐飲", "指定零售"]
---

# HSBC Red Card

| 場景 | 回贈率 | 支付方式 | 月上限 | 消費下限 |
|------|--------|----------|--------|----------|
| 本地簽帳（指定商戶） | **8%** | 實咭 | $1,250 | $0 |
| 本地網購/外幣網購 | 4% | 實咭 | $10,000 | $0 |

**指定商戶**: 壽司郎、譚仔三哥/雲南、Bakehouse、Decathlon、NAMCO、TAITO、Sephora、@cosme、3COINS

- **FCC**: 本地不適用 / 外幣 1.95%
- **截數日**: 每月 20 日
