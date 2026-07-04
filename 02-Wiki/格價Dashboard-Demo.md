---
cssclasses:
  - dashboard
---

# 🛒 格價 Dashboard（Demo）

> 呢個係概念展示 — Hermes 可以自動爬格價、寫入 frontmatter，DataviewJS 動態 render

```button
name  新增產品
type link
action 02-Wiki/PriceCheck/
color blue
```

---

## 📊 價格概覽

```dataviewjs
const pages = dv.pages('"02-Wiki/PriceCheck"').where(p => p.type === 'price-check');
const total = pages.length;
const avgPrice = pages.length > 0 
  ? (pages.values.reduce((a, p) => a + (p.price || 0), 0) / pages.length).toFixed(0)
  : 0;
const cheapest = pages.length > 0
  ? pages.sort(p => p.price || 999999)[0]
  : null;
const up = pages.where(p => p.trend === 'up').length;
const down = pages.where(p => p.trend === 'down').length;

dv.container.innerHTML = `
<div class="stats-grid">
  <div class="stat-card"><div class="stat-value">${total}</div><div class="stat-label">追蹤貨品</div></div>
  <div class="stat-card"><div class="stat-value">$${avgPrice}</div><div class="stat-label">平均價格</div></div>
  <div class="stat-card stat-buy"><div class="stat-value">${down}</div><div class="stat-label">📉 跌價</div></div>
  <div class="stat-card stat-sell"><div class="stat-value">${up}</div><div class="stat-label">📈 升價</div></div>
</div>`;
```

---

## 🏷️ 按類別分類

```dataviewjs
const pages = dv.pages('"02-Wiki/PriceCheck"').where(p => p.type === 'price-check');
const categories = {};
pages.forEach(p => {
  const cat = p.category || '其他';
  if (!categories[cat]) categories[cat] = [];
  categories[cat].push(p);
});

dv.container.innerHTML = Object.entries(categories).map(([cat, items]) => {
  const best = items.sort((a, b) => (a.price||0) - (b.price||0))[0];
  return `<details open>
    <summary><strong>${cat}</strong>（${items.length} 件）最平 $${best.price} @ ${best.retailer}</summary>
    <table class="stock-table">
      <thead><tr><th>產品</th><th>零售商</th><th>💰 價格</th><th>📊 走勢</th><th>更新</th></tr></thead>
      <tbody>${items.sort((a,b) => (a.price||0)-(b.price||0)).map(p => {
        const trendIcon = p.trend === 'up' ? '🟢 升' : (p.trend === 'down' ? '🔴 跌' : '⚪ 平');
        return `<tr>
          <td><strong>${p.product}</strong></td>
          <td>${p.retailer}</td>
          <td style="font-weight:bold; color:${p.price === best.price ? 'var(--color-green)' : 'inherit'}">
            ${p.price === best.price ? '🏆 ' : ''}$${p.price}
          </td>
          <td>${trendIcon}</td>
          <td>${p.last_check || '-'}</td>
        </tr>`;
      }).join('')}</tbody>
    </table>
  </details>`;
}).join('');
```

---

## 🔍 最抵買推薦

```dataviewjs
const pages = dv.pages('"02-Wiki/PriceCheck"').where(p => p.type === 'price-check');
const bestDeals = {};
pages.forEach(p => {
  const key = p.product;
  if (!bestDeals[key] || (p.price||0) < (bestDeals[key].price||999999)) {
    bestDeals[key] = p;
  }
});

dv.container.innerHTML = '<div class="cards-grid">' + Object.values(bestDeals).sort((a,b) => (a.price||0)-(b.price||0)).map(p => `
  <div class="rating-card" style="border-left: 4px solid var(--color-green);">
    <div class="card-header"><strong>${p.product}</strong><span class="rating-badge badge-buy">最抵</span></div>
    <div class="card-body">
      <div style="font-size:1.5em; font-weight:bold; color:var(--color-green);">$${p.price}</div>
      <div>@ ${p.retailer}</div>
      <div style="color:var(--text-muted); font-size:0.85em;">🔄 ${p.last_check}</div>
    </div>
  </div>
`).join('') + '</div>';
```

---

## 📦 Demo 數據架構

每件產品係一個 `.md` file，frontmatter 係咁：

```yaml
---
type: price-check
product: PlayStation 5 Slim
category: 遊戲機
retailer: 豐澤
price: 3980
trend: down
last_check: 2026-07-04
url: https://...
---
```
