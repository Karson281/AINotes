---
creation_date: 2026-06-07
source: "Gemini"
tags:
  - topic/untagged
status: inbox
---

# 知識庫-Gemini 與豆包同步 Obsidian 差異 - Google Gemini

**Date:** 2026-06-07 02:13
**Source:** Gemini

---

Gemini
新對話
搜尋對話
媒體庫
Gems
最近
自駕遊：OAK 機場附近 Costco 油站防盗指引
旅行：美國搭飛機行李打包指南
知識庫：Gemini 與豆包同步 Obsidian 差異
消費：網購信用卡套利方案
提示詞：香港自駕遊專家-朗晴居出發
旅行：旅行達人-加州旅遊小費與安全指南
Apps: 網頁製作即時匯率轉換器
提示詞：回贈管理 pdf 更新
提示詞：AI 賀咭達人系統提示詞設計
提示詞：简易信用卡回贈計算器
提示詞：簡易信用卡回贈篩選服務
提示詞：簡易信用卡回贈消費篩選
提示詞：简易信用咭回贈篩選助手
提示詞：香港自駕遊專家-提示詞設定
提示詞：香港小學擬題專家提示詞
提示詞：旅行社顧問-行程搜尋與篩選
保險：消費達人-藍十字智在遊尊尚計劃 諮詢
自駕遊：LAX Alamo Skip the Counter 取車指南
提示詞：旅行達人-回贈管理資料庫與旅遊建議
Karson Yeung
Plus
與 Gemini 對話
你話

開網頁gemini 右下角出現sync to Obsidian button, 但豆包沒有？

Gemini 話

這是非常正常的現象！之所以會出現這個差異，是因為這兩個 AI 網頁背後的 「瀏覽器擴充功能（Extension / Plugin）」支援度 不同。

簡單來說，你目前使用的 Obsidian 同步套件（例如 Gemini to Obsidian 或 Obsidian Web 等）只針對了 Gemini 的網頁網址與結構進行了開發，而沒有寫入支援豆包（Doubao）的程式碼。

以下為你詳細拆解為什麼會這樣，以及該怎麼解決：

為什麼 Gemini 有，而豆包沒有？
1. 擴充功能是「認網址和網頁結構」的

瀏覽器擴充功能在運作時，必須先識別特定的網址（例如 gemini.google.com），並在網頁的特定位置（如右下角）強行插入一個「Sync to Obsidian」的按鈕。

2. 開發者尚未適配豆包

Gemini 作為全球主流的 AI 工具，國際開發者為它製作配套工具的意願非常高。而豆包（Doubao）是火山引擎（字節跳動）推出的產品，兩者的網頁原始碼結構（HTML 標籤、CSS 樣式）完全不同。如果擴充功能的開發者沒有特別為 doubao.com 寫一套適配代碼，按鈕就不可能會出現在豆包的網頁上。

💡 解決方案：如何在豆包也實現「一鍵同步到 Obsidian」？

如果你希望把豆包的對話也快速傳送到 Obsidian，可以嘗試以下幾個替代方案：

方案 A：更換支援「全網頁」或「多 AI 平台」的 Obsidian 擴充功能

有些外掛不是專為單一 AI 設計的，而是允許你選取網頁任何文字，或支援自定義網址。

推薦外掛： Obsidian Web Clipper (官方近期推出的瀏覽器剪藏插件) 或 MarkDownload。

使用方式： 安裝後，在豆包的網頁上直接點擊瀏覽器右上角的擴充功能圖示，就能把整篇對話或選取的文字直接剪藏進 Obsidian。

方案 B：使用專門的「AI 對話匯出」擴充功能

有些瀏覽器外掛專門用來備份各種 AI 的對話紀錄（例如支援 ChatGPT, Claude, Gemini 等），你可以留意它們最近是否有更新支援豆包。

這類外掛通常會提供「匯出為 Markdown (.md)」的功能，下載後直接丟進你的 Obsidian 庫（Vault）即可。

方案 C：到原擴充功能的 GitHub 頁面提需求 (Issue)

如果你非常喜歡現在用來同步 Gemini 的這個按鈕功能，可以去瀏覽器擴充功能商店看它的開發者是誰，通常會連結到他們的 GitHub 頁面。

你可以在那裡提交一個 Issue (Feature Request)，標題寫：「Hope to support Doubao (doubao.com)」，如果需求的人多，開發者可能就會在下一次更新時把豆包也加進去！

目前最快的方法，還是先用 網頁剪藏外掛 (Web Clipper) 來處理豆包的對話喔！你目前在 Gemini 上是用哪一款擴充功能來同步的呢？




Flash

Gemini 是 AI，可能會出錯。
