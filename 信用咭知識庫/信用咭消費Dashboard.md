---
tags: [dashboard]
---

# 💳 信用咭消費回贈查詢

> 輸入消費資料 → 自動推薦最佳信用卡

---

## 📥 輸入
```dataviewjs
// IIFE wrapper — prevents 'dv already declared' error
(() => {
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
  if (!card.cashback) continue;
  
  let bestRate = 0;
  for (const field of cashbackFields) {
    const r = card.cashback[field] || 0;
    if (r > bestRate) bestRate = r;
  }
  
  if (card.scenarios && card.scenarios.length > 0) {
    for (const s of card.scenarios) {
      const sFields = modeMap[s.spend_mode] || [s.spend_mode];
      const matched = cashbackFields.some(f => sFields.includes(f));
      if (!matched) continue;
      if (payMethod && s.pay_method && !s.pay_method.includes(payMethod.toLowerCase())) continue;
      if (s.spend_min && amount < s.spend_min) continue;
      if (s.rate > bestRate) bestRate = s.rate;
    }
  }
  
  if (bestRate === 0) continue;
  if (card.spend_min && amount < card.spend_min) continue;
  
  if (payMethod) {
    const pmLower = payMethod.toLowerCase().replace(/\s/g, "");
    const methods = card.payment_methods;
    if (methods) {
      const pmKey = pmLower === "gpay" ? "gpay" :
                    pmLower === "bocpay" ? "bocpay" :
                    pmLower === "雲閃付" ? "unionpay" :
                    pmLower === "手機二維碼" ? "qrcode" :
                    pmLower === "實咭" ? "physical_card" : "";
      if (pmKey && methods[pmKey] !== "Y" && methods[pmKey] !== true) continue;
    }
  }
  
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
  const grossRebate = amount * (finalRate / 100);
  
  let fee = 0;
  if (isOverseas || isCN) {
    const fcc = card.foreign_transaction_fee;
    if (fcc && fcc > 0) fee = amount * (fcc / 100);
  }
  
  const netRebate = grossRebate - fee;
  let cappedRebate = netRebate;
  if (card.spend_cap_monthly && card.spend_cap_monthly > 0) {
    const currentBalance = card.new_balance || 0;
    const remaining = card.spend_cap_monthly - currentBalance;
    if (cappedRebate > remaining && remaining > 0) cappedRebate = remaining;
    if (remaining <= 0) continue;
  }
  
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
    note: merchantNote,
    balance: card.new_balance || 0,
    cap: card.spend_cap_monthly || 0
  });
}

results.sort((a, b) => b.netRebate - a.netRebate);

// ✅ 修正：用 dv.container.innerHTML 取代所有 dv.el()
const header = document.createElement("div");
header.innerHTML = `
  <p style="font-size:1.1em; font-weight:bold; margin-bottom:4px;">
    📊 消費 $${amount} · ${spendMode} · ${location}${merchant ? " · " + merchant : ""}${payMethod ? " · " + payMethod : ""}
  </p>`;
dv.container.appendChild(header);

if (results.length === 0) {
  const noResult = document.createElement("p");
  noResult.textContent = "❌ 冇匹配嘅信用卡";
  dv.container.appendChild(noResult);
} else {
  // Top 2 表格
  dv.table(
    ["排名", "信用咭", "支付模式", "回贈率", "淨回贈", "月上限餘額"],
    results.slice(0, 2).map((r, i) => [
      i === 0 ? "🥇" : "🥈",
      `**${r.name}** (${r.bank})`,
      r.payMethods.join(" / "),
      `${r.rate}%`,
      `HK$${r.netRebate.toFixed(1)}`,
      r.cap > 0 ? `$${(r.cap - r.balance).toFixed(0)} / $${r.cap}` : "無上限"
    ])
  );

  // 分隔線與全部結果標題
  const divider = document.createElement("div");
  divider.innerHTML = `<hr style="margin:12px 0;"><p style="font-weight:bold;">📋 全部結果</p>`;
  dv.container.appendChild(divider);

  // 全部結果表格
  dv.table(
    ["信用咭", "回贈率", "淨回贈", "支付方式", "備註"],
    results.map(r => [
      r.name,
      `${r.rate}%`,
      `HK$${r.netRebate.toFixed(1)}`,
      r.payMethods.join(" / "),
      r.note
    ])
  );
}
})(); // END IIFE
```dataviewjs


