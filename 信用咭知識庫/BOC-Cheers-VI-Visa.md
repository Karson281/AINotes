---
card_name: "BOC Cheers VI Visa"
bank: "BOC"
spend_mode: "實體咭 / GPay"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-07-28
new_balance: 0
foreign_transaction_fee: 1.95

cashback:
  local_dining: 4.0
  local_retail: 4.0
  local_online: 4.0
  overseas_online: 4.0
  overseas_pos: 4.0
  cn_pos: 0
  travel: 4.0

merchant_specific: []

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
  - spend_mode: local_dining
    pay_method: [physical_card, gpay]
    rate: 4.0
    cap: 100000
    spend_min: 5000
    note: "本地餐飲/外地簽帳"
  - spend_mode: local_retail
    pay_method: [physical_card, gpay]
    rate: 4.0
    cap: 6000
    spend_min: 5000
    note: "寵物/休閒/機票酒店/電子/餐飲/醫療/珠寶（星期日及公眾假期）"
  - spend_mode: local_online
    pay_method: [gpay]
    rate: 4.0
    cap: 4000
    spend_min: 0
    note: "本地網購（星期日及公眾假期）"

spend_min: 5000
spend_cap_monthly: 100000

special_rules:
  - "場景 2+3 只限星期日及公眾假期"
  - "場景 1 消費下限 $5,000"
  - "FCC: 場景 1 有 1.95%，場景 2/3 不適用"

tags: [dining, travel, retail, gpay]
best_for: ["餐飲", "機票酒店", "電子產品"]
---

# BOC Cheers VI Visa

| 場景 | 回贈率 | 支付方式 | 月上限 | 消費下限 |
|------|--------|----------|--------|----------|
| 本地餐飲/外地簽帳 | 4% | 實咭/GPay | $100,000 | $5,000 |
| 本地簽帳（6大類別）| 4% | 實咭/GPay | $6,000 | $5,000 |
| 本地網購 | 4% | GPay | $4,000 | $0 |

**6大類別**: 寵物生活、休閒娛樂、機票酒店、電子產品、餐飲、醫療、珠寶服飾  
⚠️ 場景 2+3 只限星期日及公眾假期

- **FCC**: 場景 1 有 1.95%
- **截數日**: 每月 28 日
