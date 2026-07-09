# Proma-Hermes 協作協議

**日期：2026-07-09** | **版本：v1.0**

---

## 分工原則

| 角色 | Agent | 模型 | 負責 |
|:---|:---|:---|:---|
| **策劃者** | Proma | DeepSeek Pro | 分解任務、預判風險、釐清依賴、輸出結構化執行指令 |
| **執行者** | Hermes | DeepSeek Flash | 按步驟執行、回報技術困難（附 context）、不自行猜意圖 |

> Hermes 不應同時承擔「想清楚做什麼」與「怎麼做」兩種認知負擔。

---

## Proma 執行指令模板

每一步必須包含以下五個欄位：

| 欄位 | 說明 |
|:---|:---|
| **目標** | 本步驟要達成的具體可驗證結果 |
| **前置條件** | 執行前需確認的狀態（例如：服務已停止、檔案已備份） |
| **指令** | 精確的命令或操作步驟 |
| **驗證方法** | 如何確認步驟成功（預期輸出） |
| **失敗回退** | 若失敗，應執行的回滾操作 |

---

## 範例

### Step 1: 加入 Cloudflare Tunnel service

**目標**：n8n.tatyan.com 可經 HTTPS 從公網存取

**前置條件**：
- Docker 及 docker-compose 已安裝
- Cloudflare 帳戶已登入 one.dash.cloudflare.com
- n8n container 已在 docker-compose.yml 中定義（service name: `n8n`）

**指令**：
1. Cloudflare Dashboard → Zero Trust → Networks → Tunnels → Create Tunnel
2. 命名 `n8n-tatyan`，選擇 Docker 安裝方式
3. 複製 token（格式：`eyJ...`）
4. 在 docker-compose.yml 加入以下 service：
```yaml
  cloudflared:
    image: cloudflare/cloudflared:latest
    command: tunnel run --token <貼上token>
    restart: unless-stopped
    depends_on:
      - n8n
```
5. Cloudflare Tunnel → Public Hostname：
   - Subdomain: `n8n`
   - Domain: `tatyan.com`
   - Service: `http://n8n:5678`
6. `docker compose up -d cloudflared`

**驗證方法**：
```bash
curl -s -o /dev/null -w "%{http_code}" https://n8n.tatyan.com
```
預期輸出：`200`

**失敗回退**：
- 若 `cloudflared` container 無法啟動：`docker compose logs cloudflared` 查看錯誤
- 常見錯誤：token 格式不正確、Cloudflare 帳戶未驗證域名
- 回滾：`docker compose stop cloudflared && docker compose rm cloudflared`
- 若域名未驗證：在 Cloudflare Dashboard 確認 tatyan.com 已加入並啟動 DNS

---

*此協議由 Proma Agent 制定，存放於 Obsidian Vault Agent-架構/ 供雙方參閱。*
*最後更新：2026-07-09*
