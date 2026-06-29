
### Hermes MCP 相容性測試 & VPS 安全補強
## 目標
1. 驗證 Hermes Agent (v0.16.0) + DeepSeek V4 Flash 的 MCP Tool Calling 相容性
2. VPS 安全漏洞盤點與修復

## 環境
- VPS: Ubuntu (root), Hermes v0.16.0
- LLM: DeepSeek V4 Flash (官方 API `api.deepseek.com/v1`)
- Vision: Qwen-VL-Plus (阿里雲)
- Telegram Bot: Proma Stock Bot (systemd service)
- Google MCP: 在本機 Proma Desktop App，VPS 未掛載
## 進行事項
### 1. MCP 相容性測試
| 項目                                | 結果    | 備註                            |
| --------------------------------- | ----- | ----------------------------- |
| `read_file`                       | ✅ 通過  | 0.1s 回應                       |
| `search_files` / `list_directory` | ✅ 通過  | 0.0s 回應                       |
| `write_file`                      | ✅ 通過  | 0.1s 回應，未觸發 approval          |
| 壓力測試（12 項連續 MCP 呼叫）               | ✅ 通過  | 混合多步驟任務亦正常（#11 讀取 5 檔案→摘要→寫入） |
| 上下文累積後的工具選擇退化                     | ✅ 無退化 | 始終保持正確工具選擇                    |
**結論：🟢 DeepSeek V4 Flash 與 Hermes MCP 完全相容**

### 2. 安全漏洞盤點與修復
#### 發現的問題
- **`/root/.hermes/google_token.json` 權限不正確**：`644` → 任何使用者可讀 → 已修復為 `600`
- **DeepSeek API Key 已泄露**：早前 replaced，已在 Hermes config.yaml 更新
- **Telegram Bot Token 在對話中暴露** → 已在 BotFather 撤銷並重發，更新了 `.env`

#### 已完成修復
- ✅ `google_token.json` → `chmod 600`
- ✅ `google_client_secret.json` → `chmod 600`
- ✅ `auth.json` → `chmod 600`
- ✅ `.env` → 已是 `600`
- ✅ `config.yaml` → 已是 `600`
- ✅ Telegram Bot Token 撤銷重發

### 3. Obsidian Vault
在 CLAUDE.md 記錄了 Vault 路徑，新 Agent 自動知道。
## 備註
- Hermes 更新落後 13381 commits（v0.16.0 vs upstream），需注意已知漏洞
- VPS 提示需重啟（核心更新 pending）
- Filesystem MCP 測試正常，但 `approvals.mode: manual` 未正確觸發審批，需要進一步配置