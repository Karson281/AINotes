---
type: deployment-guide
title: Telegram Bot v2 部署指南 (Stock-Task-List + Google)
created: 2026-06-23
status: pending
---

# Telegram Bot v2 部署指南

## 檔案清單

所有檔案在 Windows 嘅 `workspace-files/hermes-mqtt-bridge/` 目錄：

| 檔案                        | 部署到                            | 用途                   |
| ------------------------- | ------------------------------ | -------------------- |
| `proma-bot-v2.py`         | VPS `/root/proma-bot.py`       | 主 Bot（replace 舊檔）    |
| `google_services.py`      | VPS `/root/google_services.py` | Google API 模組（新加）    |
| `obsidian-write-proxy.py` | Windows 原位 replace             | Proxy v2（加咗 GET）     |
| `google-oauth-setup.py`   | Windows 執行一次                   | 拎 Google OAuth token |

---

## Part A：基本更新（唔使 Google）

### Step A1：Windows — 更新 Proxy

**如果用緊舊版 proxy：**
1. 停咗而家行緊嘅 proxy（Ctrl+C 或 Task Manager kill）
2. Replace `obsidian-write-proxy.py` 用新版
3. 重啟：
```bash
cd 去到個 file 嘅目錄
python obsidian-write-proxy.py
```
4. 確認行到：
```
Obsidian Write Proxy v2 running on http://0.0.0.0:8766
```

### Step A2：VPS — Upload 新 Bot

**一鍵部署（推薦）**
喺 Git Bash 或 PowerShell 執行：

```bash
# Git Bash
bash deploy-vps.sh

# 或 PowerShell
.\deploy-vps.ps1
```

佢會自動：
1. SCP upload 兩個 file 去 VPS
2. SSH restart bot service
3. Show status

**手動方法（如果 script 唔 work）：**

**方法 1：SCP（如果你 Windows 開緊機，Tailscale 通）**
```bash
# 喺 Windows PowerShell 或 Git Bash 執行
scp "C:\Users\kaisu\.proma\agent-workspaces\default\workspace-files\hermes-mqtt-bridge\proma-bot-v2.py" root@187.127.96.73:/root/proma-bot.py
scp "C:\Users\kaisu\.proma\agent-workspaces\default\workspace-files\hermes-mqtt-bridge\google_services.py" root@187.127.96.73:/root/google_services.py
```

**方法 2：手動 SSH + Paste**
```bash
ssh root@187.127.96.73
```
然後逐個 `cat > /root/proma-bot.py` 貼入去（內容太長可以分幾次）

**方法 3：用 VS Code Remote SSH**
直接 drag & drop upload

### Step A3：VPS — Restart Bot Service

```bash
ssh root@187.127.96.73
systemctl restart proma-bot
systemctl status proma-bot  # 確認綠色 running
```

如果 systemd service 叫其他名，改返：
```bash
systemctl list-units | grep -i promabot
# 或者
systemctl list-units | grep -i telegram
```

### Step A4：Test

Telegram 同 Bot 講：
```
/start
/stocks
/stocks add TSLA
/stocks remove TSLA
```

應該見到正常回應，包括「每日 18:00 自動分析」提示。

每日 18:00 HKT（UTC+8），Bot 會自動分析 watchlist 全部股票，send 結果去你 Telegram。**你只需改 Stock-Task-List.md 嘅股票清單，Bot 會 auto-sync 或者直接讀 VPS watchlist。**

---

## Part B：Google 整合

### Step B1：Google Cloud Console（約 10 分鐘）

**1. 開 Google Cloud 主頁**
- 瀏覽器去 https://console.cloud.google.com/
- 用你嘅 Google Account 登入

**2. 開新 Project（或揀現有）**
- 頂部選 Project → 「新增專案」
- 名：例如 `proma-stock-bot` 或任何名
- 按「建立」

**3. Enable APIs（一個一個開）**
- 左上 Menu → 「API 和服務」→ 「程式庫」
- 搜尋並 ENABLE 以下 APIs（逐個 enable，每個等幾秒）：

| API | 搜尋關鍵字 | 用途 |
|-----|-----------|------|
| Gmail API | gmail | 睇/寄 Email |
| Google Calendar API | calendar | 睇行程 |
| Google Sheets API | sheets | 讀取試算表 |
| Google Docs API | google docs | 讀取文件 |
| Places API | places | 地圖搜尋 |

**4. 建立 OAuth 2.0 Client ID（最關鍵一步）**
- 左 Menu → 「API 和服務」→ 「憑證」
- 按上方面板，佢可能叫你「設定 OAuth 同意畫面」

**OAuth 同意畫面設定：**
- User Type：揀 **「外部」**
- App name：`Proma Stock Bot`
- User support email：揀你嘅 email
- Developer contact：你嘅 email
- 按「儲存並繼續」
- Scopes：直接按「儲存並繼續」（唔使加任何 scope）
- Test users：按「ADD USERS」+ 加你自己個 Gmail
- 按「返回資訊主頁」

**建立 Client ID：**
- 按「建立憑證」→ 「OAuth 用戶端 ID」
- 應用程式類型：**「電腦版應用程式」**
- 名稱：`Proma Desktop Auth`
- 按「建立」
- 會彈出一個視窗，按 **「下載 JSON」** → 儲存為 `credentials.json`

**5. 建立 API Key（for Maps）**
- 仍然喺「憑證」頁面
- 按「建立憑證」→ 「API 金鑰」
- 複製彈出嘅金鑰（一串字母數字）
- 可以限制「應用程式限制」→ 「IP 位址」→ 輸入你 VPS IP：`187.127.96.73/32`
- 按「儲存」

### Step B2：Windows — 執行 OAuth Setup（一次過）

**1. 安裝 Python dependencies：**
```bash
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

**2. 準備檔案：**
- 將下載嘅 `credentials.json` 放入 `google-oauth-setup.py` 同一個 folder
- 開一個新檔案 `api-key.txt`，paste 你 Step B1.5 嘅 API Key

**3. Run Setup Script：**
```bash
python google-oauth-setup.py
```

**4. 瀏覽器會彈出：**
- 揀你嘅 Google Account
- 會見到安全性警告（因為係未驗證 app）
- 按「進階」→ 「前往 Proma Stock Bot（不安全）」→ 「繼續」
- 授權 Gmail、Calendar、Sheets、Docs 權限
- 授權完成後，browser 顯示「驗證流程已完成，可關閉此視窗」

**5. 確認生成咗：**
- `google-token.json` — 呢個係 refresh token，VPS Bot 就係用呢個自動 refresh
- `api-key.txt` — Maps API key

### Step B3：Upload Token 去 VPS

```bash
scp google-token.json root@187.127.96.73:/root/google-token.json
scp api-key.txt root@187.127.96.73:/root/api-key.txt
```

### Step B4：VPS — 安裝 Google Dependencies

```bash
ssh root@187.127.96.73
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### Step B5：Restart Bot

```bash
systemctl restart proma-bot
```

### Step B6：Test Google 功能

Telegram 同 Bot 講：
```
/mystatus
```
應該見到：
```
✅ Google 已授權
📍 Maps API 已設定
```

然後試：
```
/gmail               # 睇未讀郵件
/calendar            # 今日行程
/docs                # 最近 Docs
/maps 中環咖啡       # 地圖搜尋
```

---

## 假如出問題

### Bot 行唔到／起唔到
```bash
# VPS 睇 log
journalctl -u proma-bot -n 50 --no-pager
# 或者
systemctl status proma-bot
```

### Google token 過期
重新喺 Windows 行一次 `python google-oauth-setup.py`，會自動 refresh，然後再 upload 個 `google-token.json` 去 VPS。

### OAuth 授權時 browser 話「已封鎖」
睇下有無開 ad blocker／popup blocker。關咗佢再試。

### SSL 問題（Windows 用 HTTPS 但 proxy 係 HTTP）
新版 bot code + proxy 已經全部用 **HTTP**（因為 Tailscale VPN 本身就加密咗隧道），唔會有 SSL 問題。

### Windows 熄機時 Google 功能
**照用到。** Bot 喺 VPS direct call Google API，完全唔需要 Windows。
只有 sync 去 Obsidian（寫 Stock-Task-List.md）先需要 Windows 開機。
