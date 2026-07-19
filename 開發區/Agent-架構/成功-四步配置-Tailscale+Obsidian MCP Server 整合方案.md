---
prefix: 成功
status: pending
created: 2026-06-20
---

# 成功-四步配置-Tailscale + Obsidian MCP Server 整合方案

## 核心概念
用 Obsidian MCP Server plugin 取代 MQTT Bridge，配合 Tailscale 安全內網，令 Hermes (VPS) 可以直接 MCP 讀寫本地 Obsidian Vault。

## 優點
- 唔需要 Mosquitto Docker + subscriber script（簡化架構）
- 統一 MCP 協議，Agent 唔需要知檔案路徑
- Tailscale 點對點加密，唔使開 firewall port
- Obsidian plugin 原生支援，即裝即用

---

## 步驟 1 — 建立安全內網 (Tailscale)

VPS 同本機都安裝 Tailscale，加入同一 Tailnet。

```bash
# VPS (KVM2) 安裝
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# 本機 Windows 安裝
# 去 https://tailscale.com/download 下載 Windows client
# 登入同一個 Google/Microsoft 帳號
```

完成後兩邊會有 `100.x.x.x` 嘅 Tailscale IP。

---

## 步驟 2 — 配置 Obsidian 中樞

安裝 `obsidian-mcp-tools` 插件：
- Obsidian → 設定 → 第三方插件 → 社群插件市場
- 搜尋 "MCP" 或 "obsidian-mcp-tools"
- 安裝並啟用

重組 Vault 目錄結構：

```
Vault/
├── 01-Inbox/          # Hermes 寫入的原始情報（Immutable）
├── 02-Wiki/           # 結構化知識庫（Agent 整理後的長期記憶）
├── 03-Tasks/          # 消息隊列
│   ├── Pending/       # 待處理任務
│   ├── In-Progress/   # 執行中
│   └── Completed/     # 已完成
├── 04-Logs/           # 系統執行日誌
└── 開發區/            # 原有開發區保持不變
```

---

## 步驟 3 — 配置 Hermes (VPS)

喺 `~/.hermes/config.yaml` 加入遠端 Obsidian MCP Server：

```yaml
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

---

## 步驟 4 — 配置 Proma (本機)

喺 Proma MCP config (`mcp.json`) 加入本地 Obsidian MCP Server：

```json
"obsidian": {
  "type": "sse",
  "url": "http://localhost:<PORT>/mcp",
  "enabled": true
}
```

---

## 協作流程（更新版）

```
Hermes 收到手機任務
    → MCP read/write Obsidian Vault（經 Tailscale）
    → 寫入 03-Tasks/Pending/
    → Proma 透過本地 MCP 讀取到任務
    → 分析 → 寫回 03-Tasks/Completed/
    → Hermes 可以讀到結果 → 通知用戶
```

## 關聯檔案
- [[成功-整合哲學-Hermes+Proma+Obsidian 協作架構]]
- [[有待跟進-MQTT Bridge-落地部署]]（可能被取代）
