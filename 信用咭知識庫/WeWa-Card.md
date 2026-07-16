---
card_name: "WeWa Card"
bank: "WeWa"
spend_mode: "手機二維碼/雲閃付"
expiry_date: 2026-09-30
active: Y
closing_date: 2026-07-25
new_balance: 0
foreign_transaction_fee: 1.0

cashback:
  local_dining: 0
  local_retail: 10.0
  local_online: 0
  overseas_online: 0
  overseas_pos: 10.0
  cn_pos: 10.0
  travel: 0

merchant_specific:
  - store: "中國、台灣、澳門實體商店"
    rate: 10.0
    condition: "手機二維碼/雲閃付"
    expiry: 2026-09-30
  - store: "本地實體商店"
    rate: 10.0
    condition: "手機二維碼/雲閃付·消費$1500-$5556"
    expiry: 2026-09-30

payment_methods:
  physical_card: N
  card_number: N
  gpay: N
  gpay_bonus: 0
  bocpay: N
  unionpay: Y
  alipayhk: N
  wechatpay: N
  qrcode: Y

scenarios:
  - spend_mode: cn_pos
    pay_method: [qrcode, unionpay]
    rate: 10.0
    cap: 5209
    spend_min: 0
    note: "中/台/澳實體店·手機二維碼/雲閃付"
  - spend_mode: local_retail
    pay_method: [qrcode, unionpay]
    rate: 10.0
    cap: 5556
    spend_min: 1500
    note: "本地實體商店·手機二維碼/雲閃付"

spend_min: 0
spend_cap_monthly: 5556

special_rules:
  - "只限手機二維碼或雲閃付，非實咭"
  - "中/台/澳實體商店 10%·無下限·月上限 $5,209"
  - "本地實體商店 10%·消費$1,500-$5,556·至2026-09-30"
  - "FCC 1%（低於一般 1.95%）"

tags: [cn_pos, overseas_pos, local_retail, qrcode, unionpay]
best_for: ["中國簽帳", "台灣簽帳", "澳門簽帳", "本地實體店10%"]

---

# WeWa Card

| 場景 | 回贈率 | 支付方式 | 月上限 | 消費下限 |
|------|--------|----------|--------|----------|
| 中/台/澳 實體店 | **10%** | 手機二維碼/雲閃付 | $5,209 | $0 |
| 本地實體商店 | **10%** | 手機二維碼/雲閃付 | $5,556 | $1,500 |

- **FCC**: 1%
- **截數日**: 每月 25 日
- **回贈到期**: 2026-09-30
