# 待辦事項總覽 (2026-07-04)

> 由 Hermes Agent 自動掃描 vault 生成

## ⚡ 自動化
**自動化/2026-06-28 自動化-Hermes Agent 驅動的 Telegram Bot：整合 Google MCP 生態與 Obsidian 知識庫架構指南.md**
  - 📌 *   **視覺與排程協作**：（傳送一張手寫會議紀錄的照片給 Bot）「使用 Qwen-VL 解析這張圖片中的待辦事項，幫我在 Google Calendar 建立對應的行程，並將完整的文字紀錄存入 Obsidian 的 `Journal/today.md` 中。」

## 💡 提示詞
**提示詞/2026-06-07-提示詞-香港小學擬題專家提示詞-Google-Gemini.md**
  - 📌 以下為您設計了一套高度專業、結構嚴謹的提示詞模板，您可以直接複製並根據需要修改括號 [ ] 內 的內容。

## 📝 模板
**Templates/通用筆記.md**
  - 📌 ## 待辦事項
  - [ ]

**Templates/AI對話記錄.md**
  - [ ]

**Templates/工作日誌.md**
  - 📌 ## 🔜 待辦事項
  - [ ]
  - [ ]
  - [ ]

## 🤖 Agent 記錄
**Agent/2026-06-07-Agent-Zo-Computer-評價-豆包.md**
  - 📌 手機發指令生成待辦清單，自動存於Zo；
  - 📌 檔案操作：在notes資料夾新建todo.txt，寫入今日待辦清單

**Agent/2026-06-07-Agent-Microsoft-Copilon-實際應用.md**
  - 📌 Outlook 郵件管理：自動摘要郵件、提取待辦事項、撰寫回覆。
  - 📌 郵件往來	Outlook 自動摘要與回覆	提取待辦事項並生成專業回覆

## 🚧 開發中
**開發區/規劃-三大實戰場景.md**
  - [ ] Hermes cron job 定時爬取/監控
  - [ ] Hermes curl → Obsidian proxy → 寫入 01-Inbox/
  - [ ] Proma 讀取 03-Tasks/Pending/ 自動執行
  - [ ] Notification 機制
  - [ ] Hermes 讀取 Obsidian 03-Tasks/Pending/（已通）
  - [ ] Hermes 深度搜索（deep research MCP / web search）
  - [ ] Hermes 寫入 02-Wiki/（curl → proxy 已通）
  - [ ] 學習循環轉化為 Skills（Hermes 原生功能）
  - [ ] Proma MCP 搜尋 Obsidian（proma-mcp + Obsidian REST API 已通）
  - [ ] 02-Wiki/ 目錄結構化積累
  - [ ] 跨 session 記憶查詢

**開發區/Hermes Agent/規劃-Hermes 作為 MCP Server 暴露俾 Proma.md**
  - [ ] Hermes 啟動 MCP server 模式（原生功能）
  - [ ] Tailscale 開 port（VPS [VPS_IP]:8767）
  - [ ] Windows Proma mcp.json 加入 Hermes 端點
  - [ ] 測試：Proma function call Hermes 搜索網絡

**開發區/MQTT Bridge/成功-MQTT Bridge-docker-compose+subscriber script.md**
  - 📌 - 訂閱 `proma/inbox` → 收到任務寫入 `tasks/inbox/`
  - 📌 - 監控 `tasks/hermes-outbox/` → 自動 publish 回 `proma/outbox`

**開發區/MQTT Bridge/成功-MQTT Bridge-設計架構.md**
  - 📌         Obsidian Vault tasks/inbox/

**開發區/MQTT Bridge/有待跟進-MQTT Bridge-落地部署.md**
  - [ ] SSH / Browser Console 入 VPS
  - [ ] `cd ~/mqtt-bridge && docker compose up -d`
  - [ ] 設 MQTT 密碼：`docker compose exec mosquitto mosquitto_passwd -b /mosquitto/config/passwd proma <password>`
  - [ ] `docker compose restart`
  - [ ] 測試連線
  - [ ] Install Python 套件：`pip install paho-mqtt watchdog plyer`
  - [ ] Edit `mqtt-subscriber.py`：
  - [ ] 啟動：`python mqtt-subscriber.py`
  - 📌 Inbox 應該自動出現喺 `開發區/tasks/inbox/`

**開發區/完整任務地圖-優先次序總覽.md**
  - [x] Proma Telegram Bot（python-telegram-bot + DeepSeek API）
  - [x] Bot 回短訊 + 完整報告寫入 02-Wiki/Stocks/
  - [x] systemd 開機自動 restart
  - [x] qwen-vision proxy write fix（filesystem 直接寫入）
  - [x] 01-Inbox/
  - [x] 02-Wiki/（含投資組合參考.md + Stocks/ 目錄）
  - [x] 03-Tasks/Pending/、In-Progress/、Completed/
  - [x] 04-Logs/
  - [x] Bases（核心插件）
  - [x] Templater + Linter
  - [x] SOUL.md（全局人格）
  - [x] stock-analysis-prompt.md（每日分析 prompt）
  - [x] finance-stocks skill installed
  - [x] Daily Cron Job（18:00 HKT，聽日首 run）
  - [x] Tailscale VPN + Obsidian proxy
  - [x] Google Drive sync（手機 Obsidian）
  - [x] Stock Dashboard HTML tool
  - [x] qwen-vision server + Task Scheduler
  - [x] UFW active（只開必要 ports）
  - [x] Obsidian Git（每30分鐘 auto commit）
  - [x] Git Bash installed
  - [x] Tailscale ACL（default allow all）
  - [x] Obsidian Git
  - [x] Bases / Templater / Linter
  - [ ] Non-root user for Hermes
  - [ ] Immutable Inbox 原則
  - [x] Google MCP 激活（Hermes 原生支援 Google 生態）— ✅ 已授權
  - [ ] Telegram Bot 整合 Google 功能（Gmail/Sheets/Drive/Calendar/Docs/Keep/Tasks/Maps）
  - [ ] 美股 Cron Job
  - [x] 熄咗 qwen-vision server + 移除 MCP tool（Proma 0.13.0 已原生支援 qwen-vl-plus）
  - [ ] 美股 Cron Job
  - [ ] 生活三達人（格價/信用卡/旅行）
  - [ ] Obsidian Hybrid Search MCP
  - [ ] Obsidian CLI（Proma 端）
  - [x] Google MCP → ✅ 已激活授權（2026-06-22）
  - [x] Google Sheets → Skip（Markdown Table + Bases 取代）
  - [x] Dataview → Skip（Bases 取代）
  - [x] Obsidian Tasks → Skip（唔需要）
  - [x] Obsidian Sync $10/月 → 擱置
  - [x] MQTT Bridge → 已取代
  - [x] rclone → Skip（Google Drive Desktop sync 已夠）

**開發區/成功-Hermes Agent-Telegram Bot + Tasks Automation.md**
  - 📌 檔案：`~/scripts/check-tasks.sh`
  - 📌 */10 * * * * /bin/bash ~/scripts/check-tasks.sh

**開發區/成功-整合哲學-Hermes+Proma+Obsidian 協作架構.md**
  - 📌     → 寫入 Obsidian tasks/inbox/（MQTT / Obsidian MCP）
  - 📌     → 結果寫回 tasks/done/ 或 tasks/hermes-outbox/

**開發區/stock-dashboard-技術方案.md**
  - [x] Stock analysis reports 已標準化 YAML frontmatter
  - [x] Bot /analyze 已有完整資料
  - [ ] 開 Stock-Dashboard.md（等你用 Bases set up）
  - [ ] Bot 自動 append summary table（你要我改 code 就出聲）

**開發區/Proma Agent/成功-Proma Agent-vision MCP自啟服務.md**
  - 📌 用 Windows Task Scheduler 註冊啟動 task。

**開發區/_模板/有待跟進-模板.md**
  - [ ] 步驟一
  - [ ] 步驟二
  - [ ] 步驟三

## 📄 其他
**tasks/tasks-test-en.md**
  - 📌 # tasks-test-en

**tasks/tasks-test-routing.md**
  - 📌 # tasks-test-routing

**tasks/done/20260609-response-polling-v2.md**
  - 📌 original_task: 請幫我構思如何將 Obsidian 分發 (improved)

**tasks/done/20260609-response-empty-task.md**
  - 📌 original_task: task-20260609-092350

**tasks/done/20260609-response-polling方案.md**
  - 📌 original_task: 請幫我構思如何將 Obsidian 分發

**tasks/done/20260609-response-test-task-1.md**
  - 📌 original_task: 20260609-這是一條全新的測試任務_看看_Obsid
