---
card_name: "BOC SOGO VS Visa"
bank: "BOC"
spend_mode: "GPay"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-07-09
new_balance: 357.10
foreign_transaction_fee: 0

cashback:
  local_dining: 5.4
  local_retail: 5.4
  local_online: 5.0
  overseas_online: 5.0
  overseas_pos: 0
  cn_pos: 0
  travel: 0

merchant_specific: []

payment_methods:
  physical_card: N
  card_number: N
  gpay: Y
  gpay_bonus: 0
  bocpay: N
  unionpay: N
  alipayhk: N
  wechatpay: N

scenarios:
  - spend_mode: local_pos
    pay_method: [gpay]
    rate: 5.4
    cap: 2000
    spend_min: 0
    note: "本地簽帳（餐飲及其他消費）"
  - spend_mode: local_pos
    pay_method: [gpay]
    rate: 10.0
    cap: 2000
    spend_min: 5000
    note: "6大類別：寵物/休閒/機票酒店/電子/餐飲/醫療/珠寶（星期日及公眾假期）"
  - spend_mode: overseas_online
    pay_method: [gpay]
    rate: 5.0
    cap: 4000
    spend_min: 0
    note: "外幣網購：FCC 1.95%（星期日及公眾假期）"

spend_min: 0
spend_cap_monthly: 2000

special_rules:
  - "必須 GPay 支付"
  - "場景 2: $2,000 內 10% + $2,000-$6,000 5%（星期日及公眾假期）"
  - "場景 3: 只限星期日及公眾假期，FCC 1.95%"

tags: [gpay, dining, retail, online]
best_for: ["本地簽帳", "餐飲", "外幣網購"]
---

# BOC SOGO VS Visa

| 場景 | 回贈率 | 條件 | 月上限 | 消費下限 |
|------|--------|------|--------|----------|
| 本地簽帳（一般） | 5.4% | GPay | $2,000 | $0 |
| 本地簽帳（6大類別）| **10%+5%** | 日/假期 GPay | $6,000 | $5,000 |
| 外幣網購 | 5% | 日/假期 GPay | $4,000 | $0 |

**6大類別**: 寵物生活、休閒娛樂、機票酒店、電子產品、餐飲、醫療、珠寶服飾  
⚠️ 場景 2+3 只限星期日及公眾假期

- **FCC**: 本地不適用 / 外幣 1.95%
- **消費餘額**: $357.10
- **截數日**: 每月 9 日
