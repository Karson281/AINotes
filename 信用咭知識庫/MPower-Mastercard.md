---
card_name: "MPower Mastercard"
bank: "Standard Chartered"
spend_mode: "實咭 / GPay"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-08-15
new_balance: 0
foreign_transaction_fee: 1.95

cashback:
  local_dining: 0
  local_retail: 0
  local_online: 5.0
  overseas_online: 8.0
  overseas_pos: 4.0
  cn_pos: 0
  travel: 0

merchant_specific:
  - store: "Amazon, GU, lululemon, 淘寶, Uniqlo"
    rate: 8.0
    condition: "外幣網購"
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
  - spend_mode: overseas_online
    pay_method: [physical_card]
    rate: 8.0
    cap: 6539
    spend_min: 3000
    note: "指定商戶：Amazon, GU, lululemon, 淘寶, Uniqlo"
  - spend_mode: local_online
    pay_method: [physical_card]
    rate: 5.0
    cap: 10870
    spend_min: 3000
    note: "本地網購/外幣網購（非指定商戶）"
  - spend_mode: overseas_pos
    pay_method: [physical_card, gpay]
    rate: 4.0
    cap: 12500
    spend_min: 3000
    note: "外地簽帳"

spend_min: 3000
spend_cap_monthly: 12500

special_rules:
  - "消費下限 $3,000"
  - "指定網購商戶 8%（Amazon, GU, lululemon, 淘寶, Uniqlo）"
  - "FCC 1.95%"

tags: [online_shopping, overseas_online, cashback]
best_for: ["Amazon", "淘寶", "外幣網購", "Uniqlo"]
---

# MPower Mastercard

| 場景 | 回贈率 | 月上限 | 消費下限 |
|------|--------|--------|----------|
| 外幣網購（指定商戶）| **8%** | $6,539 | $3,000 |
| 本地/外幣網購（一般）| 5% | $10,870 | $3,000 |
| 外地簽帳 | 4% | $12,500 | $3,000 |

**指定商戶**: Amazon, GU, lululemon, 淘寶, Uniqlo

- **支付**: 實咭/GPay
- **FCC**: 1.95%
- **截數日**: 每月 15 日
