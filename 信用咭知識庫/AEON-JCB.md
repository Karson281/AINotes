---
card_name: "AEON JCB"
bank: "AEON"
spend_mode: "實體咭"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-07-12
new_balance: 0
foreign_transaction_fee: 1.95

cashback:
  local_dining: 33.3
  local_retail: 33.3
  local_online: 0
  overseas_online: 0
  overseas_pos: 10.0
  cn_pos: 0
  travel: 0

merchant_specific:
  - store: "OK Store"
    rate: 33.3
    condition: "消費滿 $30"
    expiry: 2026-12-31
  - store: "指定 AEON / AEON STYLE 分店（日本）"
    rate: 10.0
    condition: "實體咭"
    expiry: 2026-07-31

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
    rate: 33.3
    cap: 0
    spend_min: 30
    note: "OK Store 專用"
  - spend_mode: overseas_pos
    pay_method: [physical_card]
    rate: 8.0
    cap: 2000
    spend_min: 0
    note: "日本當地商戶（首 $6,000 豁免 FCC）"
  - spend_mode: overseas_pos
    pay_method: [physical_card]
    rate: 10.0
    cap: 2632
    spend_min: 0
    note: "指定 AEON/AEON STYLE 日本分店"

spend_min: 0
spend_cap_monthly: 2632

special_rules:
  - "OK Store 33.3% 回贈（消費滿 $30）"
  - "日本簽帳首 HK$6,000 豁免 FCC"
  - "指定 AEON 日本分店 10%，至 2026-07-31"

tags: [japan, local_pos, aeon, jcb]
best_for: ["OK Store", "日本簽帳", "AEON日本"]
---

# AEON JCB

| 場景 | 回贈率 | 月上限 | 消費下限 |
|------|--------|--------|----------|
| OK Store | **33.3%** 🔥 | 無 | $30 |
| 日本 AEON/AEON STYLE | **10%** | $2,632 | $0 |
| 日本當地商戶 | 8% | $2,000 | $0 |

- **支付**: 實體咭
- **FCC**: 1.95%（首 $6,000 豁免）
- **截數日**: 每月 12 日
