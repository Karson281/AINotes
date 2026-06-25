# 終極 Agent 協同架構：以 Obsidian 為中樞的 Hermes 與 Proma 整合方案

## 一、 架構設計與核心理念

### 1. 角色定位：各司其職

| 組件                          | 角色        | 職責                             |
| --------------------------- | --------- | ------------------------------ |
| **Hermes Agent (KVM2 VPS)** | 24/7 常駐大腦 | 背景監控、網絡爬蟲、API 輪詢、學習循環、持久化記憶    |
| **Proma Agent (本機)**        | 本地執行雙手    | 工作區管理、本地檔案操作、腳本執行、桌面自動化        |
| **Obsidian (本機)**           | 中樞神經與共享狀態 | 結構化知識庫、非同步消息隊列 (Message Queue) |

### 2. 核心連線架構：MCP 協議 + Tailscale

採用**以 Obsidian MCP Server 為中介的星型拓樸**，兩個 Agent 無需直接連線，而是共同對 Obsidian Vault 讀寫。

1. 本機安裝 obsidian-mcp-tools 插件，啟動 MCP Server
2. 透過 Tailscale 建立 VPN，將本機 Obsidian MCP Server 暴露俾 VPS
3. Hermes (VPS) 與 Proma (本機) 皆透過標準 MCP 協議操作 Obsidian

```
┌──────────┐     MCP     ┌──────────┐     MCP     ┌──────────┐
│ Hermes   │◄───────────►│ Obsidian │◄───────────►│ Proma    │
│ Agent    │  Tailscale  │ Vault    │  localhost  │ Agent    │
│ (VPS)    │             │ (本機)   │             │ (本機)   │
└──────────┘             └──────────┘             └──────────┘
```

## 二、 實戰配置指南

### 步驟 1：建立基礎網路連線 (Tailscale)
- 本機與 KVM2 VPS 安裝 Tailscale，登入同一帳號
- 取得本機 Tailscale 虛擬 IP（100.x.x.x）

### 步驟 2：配置 Obsidian 中樞與 MCP Server
建立目錄結構：
```
Vault/
├── 01-Inbox/       # Raw data (Hermes 爬取的原始資料)
├── 02-Wiki/        # Structured knowledge (結構化知識庫)
├── 03-Tasks/       # Message Queue (任務隊列)
│   ├── Pending/    # 待處理任務
│   ├── In-Progress/# 執行中
│   └── Completed/  # 已完成
├── 04-Logs/        # Execution logs (系統日誌)
└── 開發區/          # Agent 開發紀錄
```

安裝 Obsidian 插件 `obsidian-mcp-tools`，啟動 MCP Server，綁定 0.0.0.0 或 Tailscale IP。

### 步驟 3：配置 Hermes Agent (VPS)
```yaml
# ~/.hermes/config.yaml
mcp_servers:
  obsidian_vault:
    url: "http://<本機_TAILSCALE_IP>:<PORT>/mcp"
    transport: "sse"
    headers:
      Authorization: "Bearer <YOUR_OBSIDIAN_API_KEY>"
    allowed_tools:
      - "read_file"
      - "write_file"
      - "search_files"
```

### 步驟 4：配置 Proma Agent (本機)
```json
// mcp.json
"obsidian": {
  "type": "sse",
  "url": "http://localhost:<PORT>/mcp",
  "enabled": true
}
```

## 三、 協作流程

```
Hermes 收到手機任務
  → MCP write 到 03-Tasks/Pending/
  → Proma 本地 MCP read 到任務
  → 分析決策 → write 到 03-Tasks/Completed/
  → 同時更新 02-Wiki/ 做長期記憶
  → Hermes read 到結果 → 通知用戶
```

## 四、 技術棧總結

| 層面      | 技術                                          |
| ------- | ------------------------------------------- |
| 網絡層     | Tailscale (VPN)                             |
| 協議層     | MCP (Model Context Protocol)                |
| 存儲層     | Obsidian Vault (Markdown)                   |
| 同步層     | Google Drive                                |
| Agent 1 | Hermes Agent (deepseek-chat + qwen-vl-plus) |
| Agent 2 | Proma Agent (deepseek-v4-flash + MCP tools) |
