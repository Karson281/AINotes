---
created: 2026-07-02T13:15:00+08:00
type: ops
---

# Google OAuth Token Refresh

## 事件
- **日期**: 2026-07-02
- **動作**: Re-authenticate Google OAuth token
- **原因**: Token expired，refresh 失敗 (`invalid_grant`)
- **方式**: 經 `/root/setup.py --auth` 行 OAuth flow（console mode + PKCE）

## 結果
- ✅ Token 有效，有 refresh_token
- Google Services (Gmail, Calendar, Sheets, Docs, Drive) 可正常使用

## 下次
- 正常情況下 token 會自動 refresh，唔需要人手介入
- 如果再有 `invalid_grant`，行 `python /root/setup.py --auth` 即可
