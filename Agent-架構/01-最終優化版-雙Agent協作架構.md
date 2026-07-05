# 技術可行性研究報告：基於雙 Agent 協作的自動化架構設計（最終優化版）

**作者：Manus AI** | **日期：2026 年 7 月** | **最終修正：Karson**

---

## 摘要

本報告基於「Hermes Agent（DeepSeek Flash）+ Proma Agent（DeepSeek Pro）+ n8n + Obsidian Vault + Telegram Bot」五元件整合架構，旨在打造涵蓋「信用卡達人」、「旅行顧問」及「格價專家」的個人 AI 助理。

核心設計哲學：**Proma 負責深度推理，Hermes 負責通訊閘道與第一線路由**，兩者並列協作而非從屬關係。

---

## 1. 架構核心與角色重塑

### 1.1 模型配置決定角色分配

| Agent | 模型 | 定位 |
|:---|:---|:---|
| **Proma Agent** | **DeepSeek Pro**（強推理） | 中央推理引擎，負責複雜分析與多步規劃 |
| **Hermes Agent** | **DeepSeek Flash**（輕量快速） | 通訊閘道，負責 24/7 在線、意圖路由、數據聚合 |
| **n8n** | — | 確定性自動化與資料處理 |
| **Obsidian Vault** | — | 共享知識庫，永久記憶 |

### 1.2 Proma Agent：深度推理與複雜規劃

Proma Agent 搭載 DeepSeek Pro，是系統真正的「思考中樞」。

- **深度分析**：處理信用卡回贈分析、個人化推薦等複雜場景
- **多步任務**：執行需要跨多個數據源、進行多重條件過濾的旅行規劃
- **背景 Worker**：在不阻礙使用者對話的情況下，於背景處理耗時的分析任務

### 1.3 Hermes Agent：通訊閘道與輕量路由

Hermes Agent 在此架構中的核心價值在於其強大的基礎設施能力，而非深度推理。

- **24/7 在線介面**：透過原生 Telegram Gateway 接收使用者訊息
- **第一線路由**：進行意圖分類，簡單查詢直接回覆，複雜任務轉交 Proma
- **排程觸發**：利用內建 Cron 執行定時任務
- **數據聚合**：執行格價等不需深度推理的數據收集工作

### 1.4 n8n：確定性自動化與資料處理

- **資料管道**：將外部資料（如 PDF）轉換為 Markdown 格式寫入 Obsidian
- **API 串接**：連接外部服務，執行具體操作
- **資源**：建議使用 SQLite 資料庫以節省 KVM2 (2GB RAM) 的記憶體開銷

### 1.5 Obsidian Vault：共享知識庫

- 儲存信用咭回贈.md、USER.md 使用者偏好
- 存放 Proma 的推理結果與 Agent 輸出存檔
- 所有資料為純文字 Markdown，人類可讀、Agent 可解析

---

## 2. 三大應用場景的能力分層

| 場景 | 核心能力需求 | 負責 Agent | 理由 |
|:---|:---|:---|:---|
| **格價達人** | 數據聚合、比對、呈現 | **Hermes（Flash）** | 整據數據行事，不需深度推理；Flash 速度優勢匹配 |
| **旅行顧問** | 偏好匹配 + 條件過濾 | **Hermes + Proma 協作** | 日常查詢 Hermes 足夠；複雜規劃由 Proma 處理 |
| **信用卡達人** | 消費模式分析、策略推薦 | **Proma（Pro）** | 需要深度推理與個人化計算 |

### 2.1 信用卡達人：已優化數據管道

**舊設計（過時）**：依賴 n8n 爬蟲抓取信用卡網站。

**新設計（優化）**：利用既有可靠數據源（信用咭回贈.pdf），移除反爬蟲維護成本。

**實作路徑**：
1. n8n 負責將信用咭回贈.pdf 結構化轉換為 Markdown（信用咭回贈.md）
2. n8n 將轉換後的檔案寫入 Obsidian Vault 的 信用咭知識庫/
3. Proma（Pro）讀取 Vault 中的結構化數據，結合使用者消費紀錄進行分析與推薦

### 2.2 格價達人：三層 Filter Logic

為避免每次查詢消耗大量 Token：

1. **關聯過濾（n8n，0 token）**：判斷訊息是否包含格價關鍵字（平、抵、比較），若無則不處理
2. **快取過濾（n8n，0 token）**：檢查產品是否有 cached data，有則直接回覆
3. **內容過濾（Hermes，低 token）**：確認訊息符合 scope 後，才啟動 Web Search 或調用工具

日常使用中，95% 的簡單對話或已知查詢均為 0 token 消耗。

---

## 3. 通訊架構

### 3.1 主要路線：HTTP over Tailscale（即時）

VPS 與 Windows 之間透過 Tailscale 互聯，Hermes 與 Proma 直接 HTTP 通訊：

```
Hermes (VPS) ── POST /task ──► Proma (Windows, port 8767)
Proma (Windows) ── POST /result ──► Hermes (VPS)
```

### 3.2 備用路線：Agent-Inbox/ + Agent-Outputs/（非同步）

當 Proma 離線或 HTTP 失敗時，自動降級到 Obsidian 檔案佇列模式。

### 3.3 不使用 MQTT

MQTT 因一直運作不順、經常 down 機，不採用。

---

## 4. 安全設計：分散式憑證管理

| 元件 | 憑證存放方式 |
|:---|:---|
| **Hermes** | DeepSeek Flash Key + Telegram Bot Token（~/.hermes/config.yaml 或 .env，權限 0600） |
| **Proma** | DeepSeek Pro Key（.env 環境變數） |
| **n8n** | 僅儲存工作流所需的外部服務 Key（內建加密憑證庫） |

真正的安全來自：VPS 防火牆 + fail2ban、內部通訊走 Tailscale（不對公網暴露）、每個 Key 賦予最小權限、敏感設定檔不進入版本控制系統。

---

## 5. 部署建議

- VPS（KVM2+）：運行 Hermes Gateway + n8n（SQLite）+ Obsidian 副本
- 強烈建議配置 2GB Swap 確保 KVM2 穩定運行
- Windows 本地：運行 Proma Agent（DeepSeek Pro）+ Obsidian 主庫
- 同步機制：VPS 只寫 Agent-Inbox/ + Agent-Outputs/ 目錄，避開本地編輯區

---

## 6. 分階段實施

1. **Phase 1**：建立 HTTP over Tailscale 通訊，驗證 Hermes ↔ Proma 基礎迴路
2. **Phase 2**：設定路由規則，優化分流準確率
3. **Phase 3**：場景落地（格價達人 → 信用卡達人 → 旅行顧問）
4. **Phase 4**：升級 MCP 直連（可選）
