---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-Proma Agent-Qwen-vision MCP tool

## 功能描述
透過 MCP (Model Context Protocol) tool，令 Proma Agent（deepseek-v4-flash）可以 function call 去 qwen-vl-plus 做圖片分析。

## 架構
```
你問 Proma "分析呢張圖"
    → deepseek 收到
    → call MCP tool "vision_analyze"
    → Windows 本地 qwen-vision MCP server
    → download 圖片 → base64 → qwen-vl-plus (新加坡)
    → 返回分析結果
```

## 設定位置
- **MCP Server Script：** `workspace-files/hermes-mqtt-bridge/qwen-vision-mcp.py`
- **MCP Config：** `C:\Users\kaisu\.proma\agent-workspaces\default\mcp.json`
- **Server Port：** `http://localhost:8766`

## MCP Config (`mcp.json`)
```json
"qwen-vision": {
  "type": "sse",
  "url": "http://localhost:8766/mcp",
  "enabled": true
}
```

## 使用方法
### 1. 啟動 Server（keep 住 PowerShell 開住）
```powershell
$env:PORT=8766; python "C:/Users/kaisu/.proma/agent-workspaces/default/workspace-files/hermes-mqtt-bridge/qwen-vision-mcp.py"
```

### 2. 喺 Proma 問
```
用 vision_analyze 分析呢張圖：https://example.com/image.jpg
```

## 語法要點
- 圖片必須係公開 URL（local file 唔得）
- 唔支援 Wikimedia / imgur 等有限制嘅圖片源（server 會自行 download 再 base64）
- Server 用 MCP over SSE protocol，JSON-RPC 格式

## 實例
```
你 → 用 vision_analyze 分析呢張圖：https://httpbin.org/image/jpeg
Proma → [call vision_analyze]
       → 這張圖片展示了一隻豺狼（亞洲胡狼）...
```

## 相關檔案
- [[成功-Proma Agent-Deepseek主模型]]
- [[有待跟進-Proma Agent-vision MCP自啟服務]]
