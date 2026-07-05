---
created: 2026-07-04
source: vault-wide scan for "跟進" / "待辦"
---

# 📋 Pending — 所有待跟進／待辦事項總匯

> 自動掃瞄自 Obsidian Vault，按分類排列。來源：所有含「跟進」或「待辦」之 .md 檔案。
> 最後更新：2026-07-04

---

## 🧰 開發區 — 有待跟進項目

### [[有待跟進-MQTT Bridge-落地部署.md]]
> 路徑：`開發區/MQTT Bridge/`
- [ ] ~~SSH / Browser Console 入 VPS~~
- [ ] ~~`cd ~/mqtt-bridge && docker compose up -d`~~
- [ ] ~~設 MQTT 密碼~~
- [ ] ~~`docker compose restart`~~
- [ ] 測試連線
- [ ] Windows：安裝 paho-mqtt watchdog plyer
- [ ] Edit `mqtt-subscriber.py`（填 VPS IP + 密碼）
- [ ] 啟動 subscriber
- **背景**：Code 已寫好，只差執行部署

### [[有待跟進-Hermes Agent-VPS重啟model名]]
> 路徑：`開發區/Hermes Agent/`（引用自成功筆記）
- [ ] 跟進 VPS 重啟後 model name 設定

### [[有待跟進-模板.md]]
> 路徑：`開發區/_模板/`
- 通用待跟進模板，可複製使用

---

## 🛒 PriceCheck — 格價跟進

### [[2026-07-04-可摺式購物車-淘寶攻略.md]]
> 路徑：`02-Wiki/PriceCheck/`
- 🔴 **淘寶買一定得，仲平 50-60%**
- ⏳ 但 Hermes 過唔到淘寶 CAPTCHA，**需要人手俾條 link 跟進**
- 淘寶攻略已整理，只差用戶俾 link 做比價

---

## 📅 工作日誌 — 待跟進／待辦

### 2026-07-03 — 股票分析框架優化
> 路徑：`04-Logs/2026/2026-07-03 -股票分析框架優化.md`
- [ ] 北水數據 source 探索（East Money API 從 VPS 被 geo-blocked）
- [ ] Telegram trigger 直接分析功能
- [ ] 考慮加入其他免費 fundamental data source（港股 PE 問題）

### 2026-07-04 工作日誌
> 路徑：`04-Logs/2026/2026-07-04 工作日誌.md`
- [ ] Telegram /proma handler 待辦

### 2026-07-03 工作日誌
> 路徑：`04-Logs/2026/2026-07-03 工作日誌.md`
- 🔜 下次跟進（未列具體項目）

### 2026-07-02 工作日誌
> 路徑：`04-Logs/2026/2026-07-02 工作日誌.md`
- 🔜 下次跟進（未列具體項目）

### 2026-07-01 工作日誌
> 路徑：`04-Logs/2026/2026-07-01 工作日誌.md`
- ⏳ 本機 reboot 後刪 `6ddcba1b...` 空殼目錄（由得佢都得）

### 2026-06-30 工作日誌
> 路徑：`04-Logs/2026/2026-06-30 工作日誌.md`
- 🔴 **待你跟進 Revoke**：GitHub Token（GitHub Settings → Personal access tokens）
- 🔜 下次跟進（2026-07-01）

### 2026-06-29 工作日誌
> 路徑：`04-Logs/2026/2026-06-29 工作日誌.md`
- [ ] ⏳ Windows 開機自動啟動 vault-server（startup folder / task scheduler）

### 2026-06-28 工作日誌
> 路徑：`04-Logs/2026/2026-06-28 工作日誌.md`
- [ ] ⏳ 研究點樣係 VPS 24/7 環境用 **systemd** 代替 screen

### 2026-06-27 工作日誌
> 路徑：`04-Logs/2026/2026-06-27 工作日誌.md`
- [ ] ⏳ CSS Snippets 啟用（Obsidian Settings → Appearance）

### 2026-06-26 工作日誌
> 路徑：`04-Logs/2026/2026-06-26 工作日誌.md`
- ✅ ~~Revoke exposed API key~~（已 revoke，已更換新 key）

### 2026-06-25 工作日誌
> 路徑：`04-Logs/2026/2026-06-25 工作日誌.md`
- **P1: VPS Git Auto-Push**

---

## 📄 Templates — 模板參考

### [[通用筆記.md]]
> 路徑：`Templates/`
- 含 `## 待辦事項` section

### [[工作日誌.md]]
> 路徑：`Templates/`
- 含 `## 🔜 待辦事項` section

---

## 📚 研究筆記 — 提及待辦概念

### Agent - Zo Computer 評價
> 路徑：`Agent/2026-06-07-Agent-Zo-Computer-評價-豆包.md`
- 📌 手機發指令生成待辦清單，自動存於 Zo
- 📌 檔案操作：在 notes 資料夾新建 todo.txt，寫入今日待辦清單
- 自動清理緩存

### Agent - Microsoft Copilot 實際應用
> 路徑：`Agent/2026-06-07-Agent-Microsoft-Copilon-實際應用.md`
- 📌 Outlook 郵件管理：自動摘要郵件、提取待辦事項、撰寫回覆
- 產品簡報、郵件往來、專案會議等自動化場景

### 自動化 - TG 調動全生態 Google MCP
> 路徑：`自動化/2026-06-28 自動化-TG 調動全生態 Google MCP.md`
- 📌 Contacts/Tasks：查聯絡人、建待辦

### 自動化 - Hermes Agent + Google MCP 生態
> 路徑：`自動化/2026-06-28 自動化-Hermes Agent 驅動的 Telegram Bot：整合 Google MCP 生態與 Obsidian 知識庫架構指南.md`
- 📌 視覺與排程協作：Qwen-VL 解析圖片 → Google Calendar + Obsidian
- 📌 跨 Agent 協作：Obsidian Tasks/proma_queue.md 傳送任務

---

## 📊 統計

| 分類 | 項目數 |
|------|--------|
| 🧰 開發區有待跟進 | 3 |
| 🛒 PriceCheck 格價 | 1 |
| 📅 工作日誌待辦 | 12 |
| 📄 Templates 參考 | 2 |
| 📚 研究筆記參考 | 4 |
| **總計** | **22** |
