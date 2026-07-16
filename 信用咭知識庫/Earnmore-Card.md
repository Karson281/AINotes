---
card_name: "Earnmore Card"
bank: "Earnmore"
spend_mode: "實咭/手機二維碼/雲閃付"
expiry_date: 2027-06-30
active: Y
closing_date: 2026-07-25
new_balance: 0
foreign_transaction_fee: 0

cashback:
  local_dining: 2.0
  local_retail: 2.0
  local_online: 2.0
  overseas_online: 2.0
  overseas_pos: 2.0
  cn_pos: 2.0
  cn_online: 2.0
  travel: 2.0

merchant_specific:
  - store: "內地/台灣/澳門簽帳"
    rate: 6.0
    condition: "QR Pay/手機閃付/雲閃付/實體咭·消費$1800-$5000"
    expiry: 2027-10-31

payment_methods:
  physical_card: Y
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
    pay_method: [physical_card, unionpay, qrcode]
    rate: 6.0
    cap: 5000
    spend_min: 1800
    note: "QR Pay/手機閃付/雲閃付/實體咭·內地/台灣/澳門·FCC 1%"
  - spend_mode: overseas_pos
    pay_method: [physical_card, unionpay, qrcode]
    rate: 6.0
    cap: 5000
    spend_min: 1800
    note: "QR Pay/雲閃付/實體咭·內地/台灣/澳門·FCC 1%"

spend_min: 0
spend_cap_monthly: 75000

special_rules:
  - "全場景無上限回贈（月上限 $75,000）"
  - "無外幣手續費"
  - "內地/台灣/澳門簽帳：6%·消費$1800-$5000·FCC 1%·至2027-10-31"

tags: [cashback, no_fee, all_round, cn_pos, overseas]
best_for: ["通用消費", "內地簽帳", "網購", "中台澳6%"]

---

# Earnmore Card

| 場景 | 回贈率 | 支付方式 | 月上限 | 消費下限 |
|------|--------|----------|--------|----------|
| 全場景（通用） | 2% | 實咭/手機二維碼/雲閃付 | $75,000 | $0 |
| 內地/台灣/澳門簽帳 | **6%** | QR Pay/雲閃付/實體咭 | $5,000 | $1,800 |

- **FCC**: 0%（通用）/ 1%（6%推廣）
- **截數日**: 每月 25 日
- **回贈到期**: 通用至 2027-06-30 · 6%推廣至 2027-10-31
