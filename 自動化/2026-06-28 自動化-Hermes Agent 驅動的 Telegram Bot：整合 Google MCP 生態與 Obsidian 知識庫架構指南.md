# Hermes Agent 驅動的 Telegram Bot：整合 Google MCP 生態與 Obsidian 知識庫架構指南

本指南專為已具備 VPS 伺服器、Hermes Agent（配置 DeepSeek V4 及 Qwen-VL-Plus）、Obsidian Vault（透過 GitHub Private Repo 同步）以及本地端 Proma Agent 的進階使用者設計。目標是建立一個安全、可控且能透過自然語言極大化調動 Google 生態系統（Workspace、BigQuery、GCP 等）的 Telegram Bot 系統。

## 1. 系統架構設計

本系統採用「端到端」的跨設備 AI 自動化管線，核心理念為：「Hermes 負責思考與記憶，Proma 負責執行，Obsidian 負責記錄與傳遞」[1]。

### 架構元件與資料流

*   **Telegram Bot 介面 (Gateway)**：作為使用者的自然語言入口。Hermes Agent 內建的 Gateway 模組透過 Webhook 或長輪詢連接 Telegram API，接收指令並回傳執行結果 [2]。
*   **Hermes Agent (VPS 端)**：
    *   **大腦與視覺**：使用 DeepSeek V4 進行複雜推理與規劃，並透過 Qwen-VL-Plus 處理 Telegram 傳入的圖片或文件截圖。
    *   **Google MCP Server**：透過整合 Google 官方的 `gws-mcp-server` 或 `@taylorwilsdon/google-workspace-mcp`，將 Google Workspace (Gmail, Drive, Calendar, Sheets) 與 GCP 服務轉化為標準化的工具呼叫 (Tool Calling) [3]。
    *   **Filesystem MCP**：授權 Hermes 讀寫位於 `/root/vault/` 的 Obsidian 知識庫。
*   **Obsidian Vault (中樞神經與記憶)**：
    *   **三層記憶架構**：分為 Session Logs (短期)、`MEMORY.md` (長期精煉)、與 Knowledge Base (永久)。Hermes 透過 Filesystem MCP 讀寫這些 Markdown 檔案 [4]。
    *   **GitHub Sync**：透過 Cron Job 或 Obsidian Git 外掛，將 `/root/vault/` 定期推送 (Push) 至 GitHub Private Repo，實現雲端與本地端的資料同步。
*   **Proma Agent (本地端)**：在本地端讀取同步下來的 Obsidian Vault，負責執行需要在本地環境完成的具體任務（例如本地程式碼編譯、本地軟體操作），並將結果寫回 Vault。

## 2. 實作與設定步驟

### 2.1 Telegram Bot 建立與 Gateway 設定
1. 在 Telegram 向 `@BotFather` 申請新的 Bot Token。
2. 透過 `@userinfobot` 獲取您的專屬數字 User ID。
3. 在 VPS 的 `~/.hermes/.env` 中設定：
   ```env
   TELEGRAM_BOT_TOKEN=您的_BOT_TOKEN
   TELEGRAM_ALLOWED_USERS=您的_USER_ID
   ```
   設定 `TELEGRAM_ALLOWED_USERS` 是第一道安全防線，確保只有您能調動此 Agent [2]。

### 2.2 Google MCP Server 整合 (Headless OAuth)
Google Workspace 的 MCP 整合需要進行 OAuth 授權。由於 VPS 是無頭 (Headless) 環境，我們採用 SSH Port Forwarding 或 Paste-back 方式完成授權 [5]。

1. 在 Google Cloud Console 建立專案，啟用所需的 API (Gmail, Drive, Calendar 等)，並建立「Desktop App」類型的 OAuth 2.0 憑證。
2. 在 `~/.hermes/config.yaml` 中設定 MCP 伺服器：
   ```yaml
   mcp_servers:
     google-workspace:
       command: "npx"
       args: ["gws-mcp-server", "--services", "drive,gmail,calendar,sheets"]
       env:
         GOOGLE_CLIENT_ID: "您的_CLIENT_ID"
         GOOGLE_CLIENT_SECRET: "您的_CLIENT_SECRET"
   ```
3. 執行 `hermes mcp login google-workspace`。系統會給出一串授權 URL。
4. 在本地瀏覽器打開該 URL，完成 Google 登入後，將重新導向的 URL (即使顯示無法連線) 複製，貼回 VPS 的終端機中，完成 Token 交換 [5]。

### 2.3 Obsidian Vault 與 Filesystem MCP 設定
為了讓 Hermes 能夠讀寫知識庫，並與本地的 Proma Agent 協作：

1. 確保 VPS 上的 `/root/vault/` 已經與 GitHub Private Repo 建立連結。
2. 在 `~/.hermes/config.yaml` 啟用 Filesystem MCP：
   ```yaml
   mcp_servers:
     obsidian-vault:
       command: "npx"
       args: ["-y", "@modelcontextprotocol/server-filesystem", "/root/vault/"]
   ```
3. **自動同步設定**：在 Hermes 中設定自然語言 Cron Job，例如在 Telegram 輸入：「每天凌晨 2 點，執行 `cd /root/vault && git add . && git commit -m "Auto sync" && git push`」。

## 3. 安全可控策略 (Security & IAM)

全面調動 Google 生態伴隨著極高的風險（例如誤刪重要郵件或雲端資源）。必須實施多層次的安全控制 [6] [7]。

1. **最小權限原則 (Least Privilege)**：
   * 在 `config.yaml` 的 `args` 中，嚴格限制 MCP Server 載入的服務（例如只載入 `drive,gmail`，不載入 `admin`）。
   * 在 Google Cloud IAM 中，為該 OAuth Client ID 設定 Deny Policies。例如，禁止呼叫任何非唯讀 (Read-only) 的工具：
     ```json
     "expression": "api.getAttribute('mcp.googleapis.com/tool.isReadOnly', false) == false"
     ```
2. **危險指令攔截 (Dangerous Command Approval)**：
   * 確保 `~/.hermes/config.yaml` 中的 `approvals.mode` 設為 `manual` 或 `smart`。
   * 當 Hermes 試圖執行如 `rm -rf` 或大量刪除資料庫的指令時，會透過 Telegram 傳送確認訊息，必須回覆 `yes` 或 `approve` 才會執行 [7]。
3. **目錄隔離**：Filesystem MCP 的路徑嚴格限制在 `/root/vault/`，防止 Agent 讀取或修改 VPS 上的系統設定檔（如 `/etc/` 或 `~/.ssh/`）。

## 4. 自然語言指令範例

設定完成後，您可以透過 Telegram 發送以下自然語言指令，極大化調動生態系：

*   **跨服務資訊整合**：「幫我讀取 Gmail 中標題包含 'Q3 財報' 的最新郵件，提取其中的營收數據，並將結果更新到 Google Drive 中名為 '2026_Revenue' 的 Sheets 試算表中。」
*   **視覺與排程協作**：（傳送一張手寫會議紀錄的照片給 Bot）「使用 Qwen-VL 解析這張圖片中的待辦事項，幫我在 Google Calendar 建立對應的行程，並將完整的文字紀錄存入 Obsidian 的 `Journal/today.md` 中。」
*   **跨 Agent 協作 (透過 Obsidian)**：「在 Obsidian 的 `Tasks/proma_queue.md` 中新增一項任務：『請 Proma Agent 在本地端編譯最新的 React 專案並回報錯誤』。」（本地端的 Proma Agent 偵測到 Vault 更新後，便會接手執行）。

---

### 參考資料
[1] [Hermes Agent 官方文件與設計理念](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
[2] [Telegram Setup - hermes-agent](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/telegram.md)
[3] [gws CLI: Wire Google Workspace Into Claude Code](https://www.grizzlypeaksoftware.com/articles/p/gws-cli-wire-google-workspace-into-claude-code-the-honest-setup-guide-nocnz7tj)
[4] [I Gave My AI Agent a Three-Layer Memory. Here’s How It Thinks Now.](https://pub.towardsai.net/i-gave-my-ai-agent-a-three-layer-memory-obsidian-heres-how-it-thinks-now-0aaa0fdbdbbd)
[5] [OAuth over SSH / Remote Hosts - Hermes Agent](https://hermes-agent.nousresearch.com/docs/guides/oauth-over-ssh)
[6] [Control MCP use with Identity and Access Management | Google Cloud](https://docs.cloud.google.com/mcp/control-mcp-use-iam)
[7] [Security | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/security)
