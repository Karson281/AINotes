## 💳 信用咭消費回贈查詢

> 輸入消費資料 → 自動推薦最佳信用卡
---
📥 輸入
```dataviewjs
// 先在 IIFE 外捕獲 Obsidian 注入的 container
const _container = dv.container;

(() => {
// === 用戶輸入（修改呢度） ===
const amount    = 5000;
const spendMode = "本地簽帳";   // 本地簽帳 | 外地簽帳 | 內地簽帳 | 台灣簽帳 | 本地網購 | 外幣網購
const location  = "香港";       // 香港 | 中國 | 澳門 | 台灣 | 日本 | 其他外地
const merchant  = "";           // 商戶名（可選，留空 = 唔指定）
const payMethod = "";           // GPay | BOC Pay | 雲閃付 | 手機二維碼 | 實咭（可選）
// =========================

const modeMap = {
  "本地簽帳": ["local_dining", "local_retail"],
  "外地簽帳": ["overseas_pos"],
  "內地簽帳": ["cn_pos"],
  "台灣簽帳": ["overseas_pos"],
  "本地網購": ["local_online"],
  "外幣網購": ["overseas_online"]
};

const isOverseas = !["香港"].includes(location);
const isCN = ["中國", "澳門"].includes(location);
const cashbackFields = modeMap[spendMode] || [];

// ── 今日日期，匹配 merchant_specific 嘅日期條件 ──
const today   = new Date();
const dayNum  = today.getDate();
const weekDay = today.getDay();
const weekDayMap = {0:"日",1:"一",2:"二",3:"三",4:"四",5:"五",6:"六"};
const todayStr = weekDayMap[weekDay];

function dateMatches(cond) {
  if (!cond) return false;
  const s = cond.replace(/\s/g, "");
  const dayMatch = s.match(/每月([\d\/]+)日/);
  if (dayMatch) {
    const days = dayMatch[1].split("/").map(Number);
    return days.includes(dayNum);
  }
  const wkMatch = s.match(/星期([一二三四五六日])/);
  if (wkMatch) return wkMatch[1] === todayStr;
  return false;
}

const cards = dv.pages('"信用咭知識庫"')
  .where(p => p.active === "Y"
           && p.file.name !== "README"
           && p.file.name !== "信用咭消費Dashboard");

const results = [];
const hasMerchantInput = merchant.trim().length > 0;

for (const card of cards) {
  if (!card.cashback) continue;

  // ── 1. 基礎回贈率 ──
  let bestRate = 0;
  for (const field of cashbackFields) {
    const r = card.cashback[field] || 0;
    if (r > bestRate) bestRate = r;
  }

  // ── 2. Scenarios 覆蓋 ──
  if (card.scenarios && card.scenarios.length > 0) {
    for (const s of card.scenarios) {
      const sFields = modeMap[s.spend_mode] || [s.spend_mode];
      const matched = cashbackFields.some(f => sFields.includes(f));
      if (!matched) continue;
      // 有商戶輸入時，scenarios 的支付方式篩選也忽略
      if (!hasMerchantInput && payMethod && s.pay_method && !s.pay_method.includes(payMethod.toLowerCase())) continue;
      if (s.spend_min && amount < s.spend_min) continue;
      if (s.rate > bestRate) bestRate = s.rate;
    }
  }

  if (bestRate === 0 && !hasMerchantInput) continue;

  // ── 3. 消費下限篩選（必須達到才顯示）──
  if (card.spend_min && amount < card.spend_min) continue;

  // ── 4. 支付方式篩選（有商戶輸入時忽略）──
  if (!hasMerchantInput && payMethod) {
    const pmLower = payMethod.toLowerCase().replace(/\s/g, "");
    const methods = card.payment_methods;
    if (methods) {
      const pmKey = pmLower === "gpay"       ? "gpay"          :
                    pmLower === "bocpay"     ? "bocpay"        :
                    pmLower === "雲閃付"     ? "unionpay"      :
                    pmLower === "手機二維碼" ? "qrcode"        :
                    pmLower === "實咭"       ? "physical_card" : "";
      if (pmKey && methods[pmKey] !== "Y" && methods[pmKey] !== true) continue;
    }
  }

  // ── 5. 商戶特定優惠 ──
  let merchantRate = 0;
  let merchantNote = "";
  let dateAutoMatch = false;

  if (card.merchant_specific && card.merchant_specific.length > 0) {
    for (const m of card.merchant_specific) {
      if (hasMerchantInput && m.store && m.store.includes(merchant)) {
        if (m.rate > merchantRate) {
          merchantRate = m.rate;
          merchantNote = m.condition || "";
        }
      }
      if (!hasMerchantInput && dateMatches(m.condition)) {
        if (m.rate > merchantRate) {
          merchantRate = m.rate;
          merchantNote = `📅 ${m.store}（${m.condition}）`;
          dateAutoMatch = true;
        }
      }
    }
  }

  // 有商戶輸入但此卡無匹配商戶回贈，跳過
  if (hasMerchantInput && merchantRate === 0 && bestRate === 0) continue;

  const finalRate   = merchantRate > bestRate ? merchantRate : bestRate;
  if (finalRate === 0) continue;

  const grossRebate = amount * (finalRate / 100);

  let fee = 0;
  if (isOverseas || isCN) {
    const fcc = card.foreign_transaction_fee;
    if (fcc && fcc > 0) fee = amount * (fcc / 100);
  }

  const netRebate  = grossRebate - fee;
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
    if (m.gpay      === "Y" || m.gpay      === true) payMethods.push("GPay");
    if (m.bocpay    === "Y" || m.bocpay    === true) payMethods.push("BOC Pay");
    if (m.unionpay  === "Y" || m.unionpay  === true) payMethods.push("雲閃付");
    if (m.qrcode    === "Y" || m.qrcode    === true) payMethods.push("手機二維碼");
    if (m.alipayhk  === "Y" || m.alipayhk  === true) payMethods.push("AlipayHK");
    if (m.wechatpay === "Y" || m.wechatpay === true) payMethods.push("WeChat Pay");
    if (m.linepay   === "Y" || m.linepay   === true) payMethods.push("Line Pay");
  }

  // ── 消費下限/上限 ──
  const spendMin = card.spend_min || 0;
  const spendCap = card.spend_cap_monthly || 0;
  let limitStr = "";
  if (spendMin > 0) limitStr += `下限 $${spendMin.toLocaleString()}`;
  if (spendMin > 0 && spendCap > 0) limitStr += " · ";
  if (spendCap > 0) limitStr += `上限 $${spendCap.toLocaleString()}`;

  results.push({
    name:        card.card_name,
    bank:        card.bank,
    rate:        finalRate,
    netRebate:   cappedRebate,
    payMethods:  payMethods,
    note:        merchantNote,
    limitStr:    limitStr,
    conditional: (merchantRate > 0 && bestRate === 0) || dateAutoMatch
  });
}

// 排序：無條件優先 → 同等下條件卡排後
results.sort((a, b) => {
  if (a.conditional !== b.conditional) return a.conditional ? 1 : -1;
  return b.netRebate - a.netRebate;
});

const unconditional = results.filter(r => !r.conditional);
const conditional   = results.filter(r =>  r.conditional);

// ── 輸出標題 ──
const header = document.createElement("div");
header.innerHTML = `<p style="font-size:1.1em;font-weight:bold;margin:8px 0 4px;">
  📊 消費 $${amount} · ${spendMode} · ${location}${merchant ? " · " + merchant : ""}${payMethod ? " · " + payMethod : ""}
</p>`;
_container.appendChild(header);

if (results.length === 0) {
  const noResult = document.createElement("p");
  noResult.textContent = "❌ 冇匹配嘅信用卡";
  _container.appendChild(noResult);
} else {

  // ── 🏆 Top 2：無條件常用卡 ──
  if (unconditional.length > 0) {
    dv.table(
      ["🏆 常用推薦", "信用咭", "支付模式", "回贈率", "淨回贈", "消費限制"],
      unconditional.slice(0, 2).map((r, i) => [
        i === 0 ? "🥇" : "🥈",
        `**${r.name}** (${r.bank})`,
        r.payMethods.join(" / "),
        `${r.rate}%`,
        `HK$${r.netRebate.toFixed(1)}`,
        r.limitStr || "無限制"
      ])
    );
  }

  // ── ⚠️ 條件觸發高回贈 ──
  if (conditional.length > 0) {
    const cLabel = document.createElement("p");
    cLabel.innerHTML = `<br><span style="color:#c60;">⚠️ 條件觸發高回贈（有日期/商戶限制，僅供參考）</span>`;
    _container.appendChild(cLabel);

    dv.table(
      ["信用咭", "回贈率", "淨回贈", "支付方式", "觸發條件"],
      conditional.map(r => [
        r.name,
        `${r.rate}%`,
        `HK$${r.netRebate.toFixed(1)}`,
        r.payMethods.join(" / "),
        r.note
      ])
    );
  }

  // ── 📋 全部無條件卡 ──
  if (unconditional.length > 2) {
    const divider = document.createElement("div");
    divider.innerHTML = `<hr style="margin:12px 0;"><p style="font-weight:bold;">📋 全部無條件卡</p>`;
    _container.appendChild(divider);

    dv.table(
      ["信用咭", "回贈率", "淨回贈", "支付方式", "消費限制"],
      unconditional.map(r => [
        r.name,
        `${r.rate}%`,
        `HK$${r.netRebate.toFixed(1)}`,
        r.payMethods.join(" / "),
        r.limitStr || "無限制"
      ])
    );
  }
}
})();
```
---
📝 使用說明
變數	說明	可選值
`amount`	消費金額 (HKD)	數字
`spendMode`	消費模式	本地簽帳 / 外地簽帳 / 內地簽帳 / 台灣簽帳 / 本地網購 / 外幣網購
`location`	消費地區	香港 / 中國 / 澳門 / 台灣 / 日本 / 其他外地

`merchant`	商戶名（可選）	例如 "惠康"、"萬寧"、"百佳"（填入後忽略支付方式篩選）
`payMethod`	支付方式（可選）	GPay / BOC Pay / 雲閃付 / 手機二維碼 / 實咭
