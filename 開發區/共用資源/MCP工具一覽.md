---
created: 2026-06-20
---

# MCP 工具一覽

## Proma Agent MCP Config
位置：`C:\Users\kaisu\.proma\agent-workspaces\default\mcp.json`

| 工具 | Type | URL | Status | 用途 |
|------|------|-----|--------|------|
| google | SSE | `localhost:3100/sse` | ✅ Enabled | Google MCP |
| zapier | SSE | `localhost:3100/sse` | ❌ Disabled | Zapier Bridge（開機自啟已停） |
| qwen-vision | SSE | `localhost:8766/mcp` | ✅ Enabled | qwen-vl-plus 圖片分析 |

## Hermes Agent (VPS)
| 工具                 | 位置                      | 狀態                 |
| ------------------ | ----------------------- | ------------------ |
| deepseek-chat      | `~/.hermes/config.yaml` | ✅ 主模型              |
| qwen-vl-plus (aux) | `~/.hermes/config.yaml` | ✅ Vision auxiliary |
| MQTT cron job      | Hermes cron system      | ✅ 每2分鐘             |
