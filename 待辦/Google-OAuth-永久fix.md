# 待辦：Google OAuth 永久 fix 🎯

## 步骤
1. Google Cloud Console → **Credentials** → **+ 建立憑證** → **OAuth 2.0 用戶端 ID**
2. 類型：**網頁應用程式**
3. 名稱：`Hermes Agent Web`
4. 已授權的重新導向 URI：`https://developers.google.com/oauthplayground`
5. 建立後 copy **client_id + client_secret**
6. OAuth Playground → ⚙️ → **Use your own OAuth credentials** ✅
7. 貼 client_id + client_secret → Close
8. Scope: `https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/documents.readonly`
9. Authorize APIs → Exchange → 俾我 Refresh token + Access token
