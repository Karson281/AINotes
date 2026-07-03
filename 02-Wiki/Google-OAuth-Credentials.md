---
created: 2026-07-03
tags: [google, oauth, credentials, reference]
---

# Google OAuth 2.0 Credentials Reference

## My Project 68208 (`consummate-rush-500205-r2`)

| Client | Client ID (尾段) | 用途 |
|--------|-----------------|------|
| **Proma Stock Bot** | `...mlc...5u` | 預留 (Proma Stock Bot) |
| **Hermes Agent** ✅ | `...dsv...l3od` | **目前用緊** — Gmail, Calendar, Drive, Sheets, Docs |

## My Project 64869

| Client | Client ID (尾段) | 用途 |
|--------|-----------------|------|
| **Google MCP Client** | `...epe...gm` | Google MCP Client (獨立 project) |

> **Security**: 上述 client secrets 已按 security policy 遮罩處理，實際值只存在於 Google Cloud Console 及 `~/.hermes/google_client_secret.json`。

## Setup Status (Hermes Agent)

- `~/.hermes/google_client_secret.json` ✅ — Client credentials 已配置
- `~/.hermes/google_token.json` ✅ — Token valid，已 re-authenticated
- 啟用 APIs: Gmail API · Google Calendar API · Google Drive API · Google Sheets API · Google Docs API · People API
- Places API (New) ✅ — API key 已更新及驗證

## Token Reset History

| Date | Action | Notes |
|------|--------|-------|
| 2026-06-22 | Initial setup | Client secret + token created |
| 2026-07-03 | Token revoked | `invalid_grant` — 需 re-auth |
| 2026-07-03 | Re-authenticated ✅ | OAuth flow completed via Telegram |
