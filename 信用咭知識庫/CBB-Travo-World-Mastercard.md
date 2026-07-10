---
card_name: "CBB Travo World Mastercard"
bank: "CBB"
spend_mode: "實咭 / GPay"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-08-03
new_balance: 0
foreign_transaction_fee: 1.95

cashback:
  local_dining: 0
  local_retail: 0
  local_online: 0
  overseas_online: 6.0
  overseas_pos: 15.0
  cn_pos: 15.0
  travel: 0

merchant_specific:
  - store: "支付寶/滴滴（內地）"
    rate: 15.0
    condition: "消費滿 ¥40"
    expiry: 2026-12-31
  - store: "美團/大眾點評（內地）"
    rate: 15.0
    condition: "消費滿 ¥100"
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
    rate: 6.0
    cap: 8334
    spend_min: 8000
    note: "外地簽帳/外幣網購（消費下限 $8,000）"
  - spend_mode: overseas_pos
    pay_method: [physical_card, gpay]
    rate: 4.0
    cap: 25000
    spend_min: 0
    note: "外地簽帳（無消費下限）"
  - spend_mode: cn_pos
    pay_method: [physical_card, gpay]
    rate: 15.0
    cap: 0
    spend_min: 40
    note: "內地簽帳：支付寶/滴滴（滿 ¥40）"
  - spend_mode: cn_pos
    pay_method: [physical_card, gpay]
    rate: 15.0
    cap: 0
    spend_min: 100
    note: "內地簽帳：美團/大眾點評（滿 ¥100）"

spend_min: 0
spend_cap_monthly: 8334

special_rules:
  - "內地支付寶/滴滴 15%（滿 ¥40）"
  - "內地美團/大眾點評 15%（滿 ¥100）"
  - "外地簽帳 6% 需消費滿 $8,000"
  - "FCC 1.95%"

tags: [cn_pos, overseas_pos, gpay, high_rebate]
best_for: ["內地簽帳", "支付寶", "美團", "滴滴"]
---

# CBB Travo World Mastercard

| 場景 | 回贈率 | 消費下限 | 月上限 |
|------|--------|----------|--------|
| 內地 支付寶/滴滴 | **15%** 🔥 | ¥40 | 無 |
| 內地 美團/大眾點評 | **15%** 🔥 | ¥100 | 無 |
| 外地簽帳/外幣網購 | 6% | $8,000 | $8,334 |
| 外地簽帳（一般） | 4% | $0 | $25,000 |

- **支付**: 實咭/GPay
- **FCC**: 1.95%
- **截數日**: 每月 3 日
- ⚠️ 場景 1 回贈至 2026-08-31
