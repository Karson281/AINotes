---
card_name: "BOC Chill World Mastercard"
bank: "BOC"
spend_mode: "GPay"
expiry_date: 2026-12-31
active: Y
closing_date: 2026-07-21
new_balance: 0
foreign_transaction_fee: 1.95

cashback:
  local_dining: 0
  local_retail: 0
  local_online: 0
  overseas_online: 10.0
  overseas_pos: 10.0
  cn_pos: 0
  travel: 0

merchant_specific:
  - store: "McDonald's, Pacific Coffee, Starbucks, UNIQLO, GU, IKEA, Dyson, Samsung, Sony, LOG-ON, NOC, %ARABICA, FINEPRINT, Logitech, Razer, 全港戲院, Apple Store, Netflix, Spotify, YouTube 等"
    rate: 10.0
    condition: "消費滿 $1,500 + GPay"
    expiry: 2026-12-31

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
  - spend_mode: overseas_pos
    pay_method: [gpay]
    rate: 10.0
    cap: 1562
    spend_min: 1500
    note: "指定商戶滿 $1,500"
  - spend_mode: overseas_pos
    pay_method: [gpay]
    rate: 5.0
    cap: 3260
    spend_min: 0
    note: "非指定商戶（無消費下限）"

spend_min: 1500
spend_cap_monthly: 1562

special_rules:
  - "必須 GPay 支付"
  - "10% 指定商戶需消費滿 $1,500（McDonald's, UNIQLO, IKEA, Apple Store, Netflix 等 30+ 商戶）"
  - "5% 非指定商戶無消費下限"

tags: [gpay, overseas_pos, overseas_online]
best_for: ["外地簽帳", "指定國際品牌", "GPay"]
---

# BOC Chill World Mastercard

| 場景 | 回贈率 | 消費下限 | 月上限 |
|------|--------|----------|--------|
| 外地/外幣 — 指定商戶 | **10%** | $1,500 | $1,562 |
| 外地/外幣 — 一般 | 5% | $0 | $3,260 |

**指定商戶**: McDonald's, Pacific Coffee, Starbucks, UNIQLO, GU, IKEA, Dyson, Samsung, Sony, LOG-ON, NOC, %ARABICA, FINEPRINT, Logitech, Razer, 全港戲院, Apple Store/TV/Music, App Store, Disney+, Google Play, JOOX, KK Box, MOOV, Netflix, Nintendo, PlayStation, Spotify, YouTube

- **支付**: 必須 GPay
- **FCC**: 1.95%
- **截數日**: 每月 21 日
