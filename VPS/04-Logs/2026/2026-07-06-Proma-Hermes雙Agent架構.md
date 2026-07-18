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

---

## 傍晚 Session（18:53 - 19:30）：架構轉向與信用咭達人設計

### 關鍵決策：放棄 Hermes→Proma delegation
- 早上建立的 `delegate-to-proma` shell script + HTTP bridge 方向被否定
- 原因：迫 Hermes (Flash) 做 router 係「削足就履，事倍功半」
- Hermes 本身設計理念係自己處理問題，非做 delegation router
- 保留基建作為備用方案（有備無患）

### 新架構：三層分工
- **Proma (Pro) = CEO / 策略顧問**：架構評鑑、危機處理、深度分析
- **Hermes (Flash) = Manager / 前線經理**：Telegram 24/7、Web Search 格價、快速查詢
- **n8n = Secretary / 營運中樞**：路由分發、定時任務、數據管道
- 今日證明：Hermes Web Search 格價快而準；Proma 成功診斷並修復 Tailscale DNS 危機

### 信用咭達人設計
- 核心機制：自然語言 → AI 摘取關鍵欄位 → 結構化查詢咭片庫 → 自然語言回答
- 五大消費模式：本地簽帳、外地簽帳、內地簽帳、本地網購、外地網購
- 七大支付方式：GPay、BOC Pay、雲閃付、AlipayHK、Wechat、實咭、實咭咭號
- Active flag 過濾過期卡片，節省 AI scan token
- 指定商店欄位（萬寧、麥當勞、ESSO）+ 特殊回贈條件
- 消費下限/上限自動計入回贈計算

### 產出文件
| 文件 | 位置 |
|:---|:---|
| 信用咭達人可行產報告 | `.context/credit-card-expert-blueprint.md` |
| Dashboard Demo（5 場景對話） | `.context/dashboard-demo.md` |
| 咭片 Frontmatter v2 模板 | 同上，附完整 YAML schema |
| Dashboard 主頁設計 | 同上，Dataview queries + 精選表 |

### 明日待辦
- Hermes 建立 n8n + Telegram Bot
- 按模板填寫 5 張主力信用卡 frontmatter
- 建立 Obsidian Dataview Dashboard
- 測試自然語言查詢流程
