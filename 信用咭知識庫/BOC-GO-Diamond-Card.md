---
card_name: "BOC GO Diamond Card"
bank: "BOC"
spend_mode: "多模式（網上理財/BOC Pay/雲閃付/實體咭）"
expiry_date: 2026-09-30
active: Y
closing_date: 2026-07-19
new_balance: 0
foreign_transaction_fee: 0

cashback:
  local_dining: 0
  local_retail: 5.0
  local_online: 5.0
  overseas_online: 0
  overseas_pos: 0
  cn_pos: 8.0
  travel: 0

merchant_specific:
  - store: "內地及澳門銀聯商店"
    rate: 8.0
    condition: "實體咭"
    expiry: 2026-12-31
  - store: "內地美團/大眾點評/滴滴出行"
    rate: 5.0
    condition: "實體卡/雲閃付"
    expiry: 2026-09-30
  - store: "Keeta/惠康/Market Place"
    rate: 5.0
    condition: "實體卡/雲閃付"
    expiry: 2026-09-30

payment_methods:
  physical_card: Y
  card_number: N
  gpay: N
  gpay_bonus: 0
  bocpay: Y
  unionpay: Y
  alipayhk: N
  wechatpay: N

scenarios:
  - spend_mode: local_pos
    pay_method: [bocpay]
    rate: 1.4
    cap: 20000
    spend_min: 10000
    note: "網上理財/BOC Pay：繳費（管理費/保險/水電煤/差餉地租）"
  - spend_mode: cn_pos
    pay_method: [unionpay, bocpay]
    rate: 8.0
    cap: 1250
    spend_min: 0
    note: "雲閃付/BOC Pay：內地實體店"
  - spend_mode: local_pos
    pay_method: [physical_card, unionpay]
    rate: 5.0
    cap: 2000
    spend_min: 1500
    note: "實體卡/雲閃付：內地美團等 + 本地 Keeta/惠康/Market Place"
  - spend_mode: local_pos
    pay_method: [unionpay, bocpay]
    rate: 4.0
    cap: 2500
    spend_min: 0
    note: "雲閃付/BOC Pay：本地銀聯商店"
  - spend_mode: cn_pos
    pay_method: [physical_card]
    rate: 8.0
    cap: 5000
    spend_min: 0
    note: "實體咭：內地及澳門銀聯商店（退稅另回 10%）"

spend_min: 0
spend_cap_monthly: 5000

special_rules:
  - "多場景多回贈率，視支付方式及地區"
  - "雲閃付/BOC Pay 內地簽帳 8% 最強"
  - "部分場景 FCC 豁免，部分不適用"

tags: [cn_pos, local_pos, unionpay, bocpay, multi_mode]
best_for: ["內地簽帳", "銀聯商店", "繳費"]
---

# BOC GO Diamond Card

| 場景 | 回贈率 | 支付方式 | 月上限 | 消費下限 |
|------|--------|----------|--------|----------|
| 內地實體店 | **8%** | 雲閃付/BOC Pay | $1,250 | $0 |
| 內地及澳門銀聯 | **8%** | 實體咭 | $5,000 | $0 |
| 內地美團/Keeta/惠康 | 5% | 實體卡/雲閃付 | $2,000 | $1,500 |
| 本地銀聯商店 | 4% | 雲閃付/BOC Pay | $2,500 | $0 |
| 繳費 | 1.4% | 網上理財/BOC Pay | $20,000 | $10,000 |

- **FCC**: 大部分豁免/不適用
- **截數日**: 每月 19 日
- ⚠️ 部分場景回贈至 2026-09-30
