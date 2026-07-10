---
tags: [dashboard]
---

# 💳 信用咭消費回贈查詢

> 輸入消費資料 → 自動推薦最佳信用卡

---

## 📥 輸入

```dataviewjs
const dv = app.plugins.plugins.dataview.api;

// === 用戶輸入（修改呢度） ===
const amount = 200;              // 消費金額 HKD
const spendMode = "本地簽帳";     // 本地簽帳 | 外地簽帳 | 內地簽帳 | 台灣簽帳 | 本地網購 | 外幣網購
const location = "香港";          // 香港 | 中國 | 澳門 | 台灣 | 日本 | 其他外地
const merchant = "";             // 商戶名（可選，留空 = 唔指定）
const payMethod = "";            // GPay | BOC Pay | 雲閃付 | 手機二維碼 | 實咭（可選）
// =========================

// 消費模式 → cashback field mapping
const modeMap = {
  "本地簽帳": ["local_dining", "local_retail"],
  "外地簽帳": ["overseas_pos"],
  "內地簽帳": ["cn_pos"],
  "台灣簽帳": ["overseas_pos"],
  "本地網購": ["local_online"],
  "外幣網購": ["overseas_online"]
};

// 地區 → FCC 判斷
const isOverseas = !["香港"].includes(location);
const isCN = ["中國", "澳門"].includes(location);

const cashbackFields = modeMap[spendMode] || [];

// 讀取所有活躍信用卡
const cards = dv.pages('"信用咭知識庫"')
  .where(p => p.active === "Y" && p.file.name !== "README" && p.file.name !== "信用咭消費Dashboard");

const results = [];

for (const card of cards) {
  // 跳過沒有 cashback 的
  if (!card.cashback) continue;
  
  // 計算基礎回贈率：取該消費模式最高者
  let bestRate = 0;
  for (const field of cashbackFields) {
    const r = card.cashback[field] || 0;
    if (r > bestRate) bestRate = r;
  }
  
  // 檢查 scenarios（如有，覆蓋基礎 rate）
  if (card.scenarios && card.scenarios.length > 0) {
    for (const s of card.scenarios) {
      const sFields = modeMap[s.spend_mode] || [s.spend_mode];
      const matched = cashbackFields.some(f => sFields.includes(f));
      if (!matched) continue;
      
      // 支付方式過濾
      if (payMethod && s.pay_method && !s.pay_method.includes(payMethod.toLowerCase())) continue;
      
      // 消費下限檢查
      if (s.spend_min && amount < s.spend_min) continue;
      
      if (s.rate > bestRate) bestRate = s.rate;
    }
  }
  
  if (bestRate === 0) continue;
  
  // 消費下限檢查
  if (card.spend_min && amount < card.spend_min) continue;
  
  // 支付方式過濾
  if (payMethod) {
    const pmLower = payMethod.toLowerCase().replace(/\s/g, "");
    const methods = card.payment_methods;
    if (methods) {
      // map common names
      const pmKey = pmLower === "gpay" ? "gpay" :
                    pmLower === "bocpay" ? "bocpay" :
                    pmLower === "雲閃付" ? "unionpay" :
                    pmLower === "手機二維碼" ? "qrcode" :
                    pmLower === "實咭" ? "physical_card" : "";
      if (pmKey && methods[pmKey] !== "Y" && methods[pmKey] !== true) continue;
    }
  }
  
  // 商戶特定優惠覆蓋
  let merchantRate = 0;
  let merchantNote = "";
  if (merchant && card.merchant_specific && card.merchant_specific.length > 0) {
    for (const m of card.merchant_specific) {
      if (m.store && m.store.includes(merchant)) {
        if (m.rate > merchantRate) {
          merchantRate = m.rate;
          merchantNote = m.condition || "";
        }
      }
    }
  }
  
  const finalRate = merchantRate > bestRate ? merchantRate : bestRate;
  
  // 計算淨回贈
  const grossRebate = amount * (finalRate / 100);
  
  // FCC
  let fee = 0;
  if (isOverseas || isCN) {
    const fcc = card.foreign_transaction_fee;
    if (fcc && fcc > 0) {
      fee = amount * (fcc / 100);
    }
  }
  
  const netRebate = grossRebate - fee;
  
  // 月上限檢查
  let cappedRebate = netRebate;
  if (card.spend_cap_monthly && card.spend_cap_monthly > 0) {
    const currentBalance = card.new_balance || 0;
    const remaining = card.spend_cap_monthly - currentBalance;
    if (cappedRebate > remaining && remaining > 0) cappedRebate = remaining;
    if (remaining <= 0) continue; // 已爆 cap
  }
  
  // 支付方式列表
  let payMethods = [];
  if (card.payment_methods) {
    const m = card.payment_methods;
    if (m.physical_card === "Y" || m.physical_card === true) payMethods.push("實咭");
    if (m.gpay === "Y" || m.gpay === true) payMethods.push("GPay");
    if (m.bocpay === "Y" || m.bocpay === true) payMethods.push("BOC Pay");
    if (m.unionpay === "Y" || m.unionpay === true) payMethods.push("雲閃付");
    if (m.qrcode === "Y" || m.qrcode === true) payMethods.push("手機二維碼");
    if (m.alipayhk === "Y" || m.alipayhk === true) payMethods.push("AlipayHK");
    if (m.wechatpay === "Y" || m.wechatpay === true) payMethods.push("WeChat Pay");
    if (m.linepay === "Y" || m.linepay === true) payMethods.push("Line Pay");
  }
  
  results.push({
    name: card.card_name,
    bank: card.bank,
    rate: finalRate,
    netRebate: cappedRebate,
    payMethods: payMethods,
    spendMode: card.spend_mode,
    note: merchantNote,
    balance: card.new_balance || 0,
    cap: card.spend_cap_monthly || 0
  });
}

// 排名
results.sort((a, b) => b.netRebate - a.netRebate);

// === 輸出 ===
dv.paragraph(`## 📊 消費 $${amount} · ${spendMode} · ${location}${merchant ? " · " + merchant : ""}${payMethod ? " · " + payMethod : ""}`);
dv.paragraph("");

if (results.length === 0) {
  dv.paragraph("❌ 冇匹配嘅信用卡");
} else {
  // Top 2
  const top2 = results.slice(0, 2);
  
  dv.table(
    ["排名", "信用咭", "支付模式", "回贈率", "淨回贈", "月上限餘額"],
    top2.map((r, i) => [
      i === 0 ? "🥇" : "🥈",
      `**${r.name}** (${r.bank})`,
      r.payMethods.join(" / "),
      `${r.rate}%`,
      `HK$${r.netRebate.toFixed(1)}`,
      r.cap > 0 ? `$${(r.cap - r.balance).toFixed(0)} / $${r.cap}` : "無上限"
    ])
  );
  
  // 所有結果
  dv.paragraph("");
  dv.paragraph("---");
  dv.paragraph("### 📋 全部結果");
  
  dv.table(
    ["信用咭", "回贈率", "淨回贈", "支付方式", "備註"],
    results.map(r => [
      `${r.name}`,
      `${r.rate}%`,
      `HK$${r.netRebate.toFixed(1)}`,
      r.payMethods.join(" / "),
      r.note
    ])
  );
}
```

---

## 📝 使用說明

修改上面 `const` 區塊嘅變數即可查詢：

| 變數 | 說明 | 可選值 |
|------|------|--------|
| `amount` | 消費金額 (HKD) | 數字 |
| `spendMode` | 消費模式 | 本地簽帳 / 外地簽帳 / 內地簽帳 / 台灣簽帳 / 本地網購 / 外幣網購 |
| `location` | 消費地區 | 香港 / 中國 / 澳門 / 台灣 / 日本 / 其他外地 |
| `merchant` | 商戶名（可選）| 文字，例如 "惠康"、"萬寧"、"百佳" |
| `payMethod` | 支付方式（可選）| GPay / BOC Pay / 雲閃付 / 手機二維碼 / 實咭 |
