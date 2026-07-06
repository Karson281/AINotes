# 工作日誌：雙 Agent 協作架構設計與實施

**日期：2026-07-06** | **時長：約 3.5 小時**

---

## 背景

收到 Manus AI 撰寫的「n8n + Proma + Obsidian + Telegram + Hermes 整合架構」技術可行性報告，需客觀評價及優化。

## 主要工作

### 1. 原報告評價（07:27 - 08:45）
- 驗證 Hermes Agent 真實存在（NousResearch/hermes-agent，GitHub 207k+ stars）
- 發現報告核心問題：架構權力倒置——以 DeepSeek Flash（Hermes）為中心、DeepSeek Pro（Proma）為下屬，違反能力匹配原則
- 指出爬蟲假設過時、路由設計完全缺失、Proma 定位薄弱
- 修正評分：原報告概念有價值但執行不可照搬

### 2. 架構修正（08:45 - 10:19）
- 確立雙 Agent 並列協作模式：
  - **Proma (DeepSeek Pro)**：中央推理引擎，負責複雜分析與多步規劃
  - **Hermes (DeepSeek Flash)**：通訊閘道、第一線路由、24/7 Telegram 在線、格價聚合
  - **n8n**：確定性自動化（PDF→Markdown、排程、通知）
  - **Obsidian**：共享知識庫
- DeepSeek V4 Flash vs Pro 價格對比：Flash 輸出 ¥2/百萬token，Pro 輸出 ¥6/百萬token（非高峰），成本非主要考量
- MQTT 因不穩定已棄用，改用 HTTP over Tailscale + Obsidian 檔案佇列備用
- API Key 分散管理（各元件管自己），不集中放 n8n

### 3. 路由邏輯設計（09:00 - 10:00）
- 三層分流規則：
  - 簡單查詢 → Hermes 直接回覆
  - 中等查詢 → Hermes 查 Obsidian 回覆
  - 複雜分析 → Hermes 轉交 Proma（觸發關鍵詞：分析、比較、推薦、策略、組合、優化、計劃）
- 主路線：HTTP POST over Tailscale（即時）
- 備用路線：Agent-Inbox/ + Agent-Outputs/ 檔案佇列（非同步）

### 4. Hermes 環境修復（08:00 - 08:58）
- 發現 Tailscale exit node 搶走 VPS DNS（所有域名無法解析）
- `tailscale set --exit-node=` 釋放 → 網絡恢復
- DeepSeek API Key 更新（因 Bitwarden 未同步，需重新生成）
- Hermes config 修正：`provider: custom, model: deepseek-v4-flash`
- Tailscale 重啟：`tailscale up --accept-routes=false --accept-dns=false`

### 5. Proma HTTP Server 建立（09:04 - 09:37）
- Windows 端建立 Flask HTTP Server (`~/.proma/proma-server/`)
- Bind Tailscale IP（Windows 端，port 8767）
- Endpoints：`GET /health`、`POST /task`（Bearer Token 認證）
- 直接調用 DeepSeek Pro API 進行推理
- 結果存檔至 `logs/result-*.json`

### 6. Hermes↔Proma 橋接（09:37 - 10:58）
- Hermes Plugin 被載入但工具未註冊（plugin loader bug）
- 改為 shell script 方案：`/usr/local/bin/delegate-to-proma`
- Hermes 透過內建 `terminal` tool 調用 script → HTTP → Proma
- 包含自動降級：HTTP 失敗時寫入 Obsidian Agent-Inbox/
- VPS → Tailscale → Proma HTTP 管道測試成功

## 產出文件

| 文件 | 位置 |
|:---|:---|
| 實施藍圖 | workspace `.context/implementation-blueprint.md` |
| 最終優化版架構 | Obsidian `Agent-架構/01-最終優化版-雙Agent協作架構.md` |
| 路由補強版 | Obsidian `Agent-架構/02-路由補強版-路由判斷與通訊協議.md` |
| Hermes Bridge Script | VPS `/usr/local/bin/delegate-to-proma` |
| Proma HTTP Server | Windows `~/.proma/proma-server/` |

## 剩餘待辦

- [ ] Telegram 指示 Hermes 使用 `delegate-to-proma` script（已準備好 prompt）
- [ ] End-to-end 測試：信用卡分析問題
- [ ] n8n 部署（SQLite、PDF→Markdown 數據管道）
- [ ] Hermes 長期 System Prompt 寫入 config（路由規則持久化）
- [ ] Obsidian 雙向同步策略確認（VPS 只寫 Agent-Inbox/ + Agent-Outputs/）

## 關鍵決策紀錄

1. **去 MQTT**：因長期不穩定，改用 HTTP over Tailscale（主要）+ Obsidian 檔案佇列（備用）
2. **provider: custom**：繞過 Hermes model ID 自動轉換 bug
3. **不用 OpenRouter**：直接 DeepSeek API 即可
4. **Shell script 取代 Plugin**：Hermes plugin loader 有 bug，改用 terminal + shell script 更可靠
5. **分散式 Key 管理**：各 Agent 管自己的 Key，不集中放 n8n
