---
card_name: "AEON Card Purple"
bank: "AEON"
spend_mode: "手機二維碼 / 實體咭"
expiry_date: 2026-08-31
active: Y
closing_date: 2026-07-12
new_balance: 0
foreign_transaction_fee: 0

cashback:
  local_dining: 6.0
  local_retail: 0
  local_online: 0
  overseas_online: 6.0
  overseas_pos: 6.0
  cn_pos: 6.0
  travel: 6.0

merchant_specific:
  - store: "AEON Stores (Mono Mono, Daiso Japan, Living Plaza)"
    rate: 6.0
    condition: "手機二維碼"
    expiry: 2026-08-31

payment_methods:
  physical_card: Y
  card_number: N
  gpay: N
  gpay_bonus: 0
  bocpay: N
  unionpay: N
  alipayhk: Y
  wechatpay: N
  qrcode: Y

scenarios:
  - spend_mode: local_dining
    pay_method: [qrcode]
    rate: 6.0
    cap: 5000
    spend_min: 0
    note: "手機二維碼：餐飲/交通/AEON店舖"
  - spend_mode: overseas_pos
    pay_method: [physical_card]
    rate: 6.0
    cap: 1786
    spend_min: 0
    note: "實體咭：中國、台灣、澳門及世界各地"

spend_min: 0
spend_cap_monthly: 5000

special_rules:
  - "手機二維碼模式：餐飲、交通（Uber/MTR/巴士/隧道/高鐵）6%"
  - "實體咭模式：外地簽帳/網購 6%，至 2026-07-31"
  - "二維碼回贈至 2026-08-31"

tags: [dining, transport, overseas, qrcode, aeon]
best_for: ["餐飲", "交通", "AEON店舖", "外地簽帳"]
---

# AEON Card Purple

| 場景 | 回贈率 | 支付方式 | 月上限 |
|------|--------|----------|--------|
| 餐飲/交通/AEON店舖 | **6%** | 手機二維碼 | $5,000 |
| 外地簽帳/網購（中台澳+全球） | 6% | 實體咭 | $1,786 |

- **FCC**: 不適用
- **截數日**: 每月 12 日
- ⚠️ **回贈到期**: 2026-08-31
