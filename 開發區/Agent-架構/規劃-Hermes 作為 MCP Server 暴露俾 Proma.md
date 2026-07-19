---
created: 2026-06-20
status: planning
---

# 規劃-Hermes 作為 MCP Server 暴露俾 Proma

## 目標
將 VPS 上嘅 Hermes Agent 暴露為 MCP Server，等本地 Proma 可以經過 Tailscale 直接 function call Hermes 做 VPS 任務（深度搜索、爬資料、長期記憶查詢）。

## 架構
```
Proma (Windows) ──MCP──► Hermes MCP Server (VPS port 8767)
                             │
                             ├── deepseek-chat 推理
                             ├── qwen-vl-plus vision
                             ├── 長期記憶查詢
                             └── 網絡爬蟲 / 搜索
```

## 所需實行
- [ ] Hermes 啟動 MCP server 模式（原生功能）
- [ ] Tailscale 開 port（VPS [VPS_IP]:8767）
- [ ] Windows Proma mcp.json 加入 Hermes 端點
- [ ] 測試：Proma function call Hermes 搜索網絡

## 指令參考
```bash
# VPS 啟動 Hermes MCP server（可能需要：
hermes mcp server --port 8767

# 或者 config.yaml 入面設定
```

## 前置條件
- ✅ Tailscale VPN 已打通
- ✅ Hermes deepseek-chat 已設定
- ⏳ 需確認 Hermes 嘅 MCP server 指令

## 相關檔案
- [[規劃-三大實戰場景]]
- [[成功-Hermes Agent-Tailscale+Obsidian proxy 打通]]
