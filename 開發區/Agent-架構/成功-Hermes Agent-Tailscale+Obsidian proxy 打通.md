---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-Hermes Agent-Tailscale + Obsidian proxy 打通

## 功能描述
VPS (Hermes) 同 Windows (Obsidian) 之間透過 Tailscale VPN + qwen-vision proxy，成功實現跨網絡讀寫 Obsidian Vault。

## 網絡拓樸
```
VPS (srv1740946)          Windows (ideapad-slim3i)
[VPS_IP] ◄───────► 100.98.113.30
    │                          │
    │    Tailscale VPN          │ qwen-vision server:8766
    │                          │ (含 Obsidian proxy)
    ▼                          ▼
curl → :8766/obsidian/ → → → → 127.0.0.1:27124 (Obsidian REST API)
```

## 設定詳情

### Tailscale IP
| 裝置 | Tailscale IP | 名稱 |
|------|-------------|------|
| Windows | 100.98.113.30 | ideapad |
| VPS | [VPS_IP] | srv1740946 |
| iPad | 100.118.52.119 | ipad-gen-6（offline） |
| NAS | 100.79.213.2 | nas |

### Obsidian Proxy（經 qwen-vision server）
qwen-vision MCP server port 8766 已整合 Obsidian proxy endpoints：

| Endpoint | 功能 |
|----------|------|
| `/obsidian/` | API 狀態 |
| `/obsidian/vault/` | 列出 vault 目錄 |
| `/obsidian/vault/{path}` | 讀取/寫入檔案 |
| `/obsidian/search/` | 搜尋 vault |

測試指令（VPS 執行）：
```bash
# 列出 vault
curl -s http://100.98.113.30:8766/obsidian/vault/

# 讀取檔案
curl -s http://100.98.113.30:8766/obsidian/vault/開發區/成功-整合哲學.md
```

## 安全考慮
- Tailscale WireGuard 加密，唔暴露 port 出公網
- Port 8766 只限 tailnet 內存取
- Obsidian API key 已設 Bearer token
- 建議定期 audit tailnet 內嘅裝置權限

## 相關檔案
- [[成功-四步配置-Tailscale+Obsidian MCP Server 整合方案]]
- [[成功-整合哲學-Hermes+Proma+Obsidian 協作架構]]
