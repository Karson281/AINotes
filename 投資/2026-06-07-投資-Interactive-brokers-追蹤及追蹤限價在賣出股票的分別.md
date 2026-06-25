---
creation_date: 2026-06-07
source: "Perplexity"
tags:
  - ai/perplexity
status: inbox
---

# 投資:Interactive brokers + 追蹤及追蹤限價在賣出股票的分別

**Date:** 2026-06-07 23:09
**Source:** Perplexity

---

回答
連結
圖片
分享
下載 Comet
投資:Interactive brokers + 追蹤及追蹤限價在賣出股票的分別

在 Interactive Brokers（盈透證券，IBKR）賣出股票時，「追蹤單」（Trailing Stop） 與 「追蹤限價單」（Trailing Stop Limit） 的核心區別在於：觸發後下單的類型不同，這直接影響成交確定性與成交價格控制。

關鍵區別對照表
維度	追蹤單（Trailing Stop）	追蹤限價單（Trailing Stop Limit）
觸發後下單類型	市價單（Market Order） 
ibtws
	限價單（Limit Order） 
interactivebrokers
+1

成交確定性	高（幾乎一定會成交） 
ibtws
	較低（可能無法成交，若股價快速下跌） 
interactivebrokers

成交價格控制	無保證（可能滑價） 
stock.yahoo
	有保證（不會低於你設的限價） 
interactivebrokers
+1

適合情境	急跌時必須出場、重視成交優先	想控制最低賣出價、可接受可能沒成交 
stock.yahoo

風險	可能以遠低於預期價成交（跳空時） 
stock.yahoo
	股價暴跌時可能完全沒賣出，損失擴大 
interactivebrokers
運作機制說明（以賣出為例）
1. 追蹤單（Trailing Stop）

設定「追蹤金額」或「追蹤百分比」，例如低於市價 $0.20
ibtws

股價上漲時，止損價同步上移；股價下跌時，止損價不動
ibtws

當股價觸及止損價，系統自動發出市價單賣出
ibtws

優點：確保出場

缺點：若股價跳空下跌（如財報後開盤大跌），可能以遠低於止損價成交

2. 追蹤限價單（Trailing Stop Limit）

設定「追蹤金額」＋「限價偏移（Lmt Offset）」或直接設限價
interactivebrokers
+1

止損價運作與追蹤單相同

當股價觸及止損價，系統發出限價單（價格 = 最後計算的限價）
interactivebrokers

優點：可控制最低賣出價，避免極端滑價
stock.yahoo

缺點：若股價快速跌破限價，訂單可能完全不成交，你仍持有股票
interactivebrokers

舉例說明

假設你持有 XYZ 股票，現價 $62.46，平均成本 $66.34：

設定	追蹤單	追蹤限價單
追蹤金額	$0.20	$0.20
初始止損價	$62.26	$62.26
限價偏移	—	$0.10 → 限價 = $62.16
股價跌至 $62.26 時	發出市價單，可能以 $62.20 或 $61.80 成交	發出限價單 $62.16，只有 ≥$62.16 才成交
股價跳空至 $60	以 $60 左右成交（可能損失大）	不成交，你仍持股，損失持續擴大
使用建議

用追蹤單：當你需要「確保出場」，例如避險、止損优先，能接受輕微滑價
ibtws

用追蹤限價單：當你想「鎖定利潤並控制最低賣價」，例如大額交易、避免極端滑價，且可接受可能沒成交
stock.yahoo

在 IBKR TWS 或行動 App 中，下單時選擇訂單類型為 TRAIL（追蹤單）或 TRAIL LIMIT（追蹤限價單），並填入追蹤額與限價偏移即可 。
interactivebrokers
+1

8 個來源
interactive brokers + trailing及 trailing limit 在賣出股票的分別

在 Interactive Brokers 賣出股票時，「Trailing」即追蹤止損單（Trailing Stop）和「Trailing Limit」即追蹤止損限價單（Trailing Stop Limit）有明確分別，核心在於觸發後的賣出方式不同：

Trailing（追蹤止損單）

設定某個固定金額或百分比距離現價為「追蹤額」。

如果股價上漲，止損價隨之上移；如股價下跌，止損價保持不變。

一旦市價跌至止損價，系統自動以市價單（Market Order）賣出持倉，保證能賣出，但最後成交價可能比止損價差一些
interactivebrokers
+1
。

Trailing Limit（追蹤止損限價單）

同樣設追蹤額，但需再指定一個「限價」或「限價偏離值」。

當市價跌至止損價時，系統送出一張限價單（Limit Order），僅在限價或更好價格成交，若市價未達限價則可能無法成交。

提供更多自主性，你能控制最壞可能成交價，但未必一定能賣出
interactivebrokers
。

主要分別比較
功能	Trailing（追蹤止損單）	Trailing Limit（追蹤止損限價單）
觸發後下單類型	市價單（Market）	限價單（Limit）
保證成交	是，會以當前可得市價成交，但價格未必理想	否，只會在不差於限價才成交
可控最大損失	不完全可控，快市行情時存在滑價	是，損失最大不超過你設定的限價
有機會失敗未成交	否，掛市價單幾乎一定成交	會，市價若低於設定限價時賣不出
適用場景	需確保能賣得掉、不介意可能滑價	希望保證賣價底線、接受可能成交不掉

簡單總結：想要賣股票時「一定賣得出」可用 Trailing；如果追求「有控制最壞成交價」，願意承受未必保證成交，可用 Trailing Limit
interactivebrokers
+2
。

10 個來源
香港股票市場11月份今個月嘅期貨結算日係幾時

香港股票市場11月份的期貨結算日（最後交易日）是2025年11月27日，緊接著的最後結算日是11月28日。

最後交易日是期貨合約可以交易的最後一天，通常是該月的倒數第二個交易日。

最後結算日則是在最後交易日之後的下一個交易工作日，進行合約的最終盈虧結算。

因此，11月份期貨的最後交易日（即結算關鍵日）為11月27日，11月28日為正式的結算日
bowiemoneydiary
+2
。

10 個來源
後續問題
本月恆指最後交易日同最後結算日分別係幾多日
如果未平倉點樣影響我喺結算日嘅保證金要求
點查閱香港交易所或券商公布嘅期貨結算日曆
Pro
免费预览次数已用完。现在使用基础搜索。
升级




詢問後續問題
搜尋
模型
