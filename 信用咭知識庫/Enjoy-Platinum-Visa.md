---
card_name: "Enjoy Platinum Visa"
bank: "Hang Seng"
spend_mode: "GPay"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-08-15
new_balance: 20
foreign_transaction_fee: 0

cashback:
  local_dining: 0
  local_retail: 0
  local_online: 0
  overseas_online: 0
  overseas_pos: 0
  cn_pos: 0
  travel: 0

  # 回贈只限特定日期+商戶，見 merchant_specific
  # local_retail=0 避免誤導

merchant_specific:
  - store: "惠康"
    rate: 8.0
    condition: "每月 3/13/23 日"
    expiry: 2026-12-31
  - store: "萬寧"
    rate: 6.0
    condition: "每月 1/20 日"
    expiry: 2026-12-31
  - store: "萬寧"
    rate: 10.0
    condition: "實咭·每單$500·兩天累滿$1000"
    expiry: 2026-08-31

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
  - spend_mode: local_retail
    pay_method: [gpay]
    rate: 8.0
    merchant: "惠康"
    spend_min: 100
    note: "每月 3/13/23 日"
  - spend_mode: local_retail
    pay_method: [gpay]
    rate: 6.0
    merchant: "萬寧"
    note: "每月 1/20 日"
  - spend_mode: local_retail
    pay_method: [physical_card]
    rate: 10.0
    merchant: "萬寧"
    cap: 4000
    spend_min: 1000
    note: "實咭·每單$500·兩天累滿$1000·至8/31"

spend_min: 100
spend_cap_monthly: 0

special_rules:
  - "惠康 8%：每月 3、13、23 日，消費下限 $100"
  - "萬寧 6%：每月 1、20 日（GPay）"
  - "萬寧 10%：實咭·每單$500·兩天累滿$1000·至2026-08-31"
  - "必須 GPay 支付（除萬寧10%可用實咭）"

tags: [gpay, retail, supermarket, physical_card]
best_for: ["惠康", "萬寧", "萬寧實體"]
---

# Enjoy Platinum Visa

| 商戶 | 回贈率 | 條件 | 消費下限 | 上限 |
|------|--------|------|----------|------|
| 惠康 | **8%** | GPay·每月 3/13/23 日 | $100 | — |
| 萬寧 | 6% | GPay·每月 1/20 日 | — | — |
| **萬寧（新）** | **10%** | **實咭·每單$500·兩天$1000** | **$1,000** | **$4,000** |

- **支付**: 必須 GPay（萬寧10%可用實咭）
- **月上限**: 無（萬寧10%上限$4,000）
- **消費餘額**: $20
- **截數日**: 每月 15 日
