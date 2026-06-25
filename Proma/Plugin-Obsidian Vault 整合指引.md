# Proma Agent ↔ Obsidian Vault 整合指引

## Vault 資訊

- **路徑：** `D:\ObsidianVault\AINotes`
- **Local REST API：** HTTPS `localhost:27124`（已啟用 SSL）
- **API Key：** 見 `.obsidian/plugins/obsidian-local-rest-api/data.json`

---

## 目錄結構

```
0-Inbox/                  臨時收件箱
1-AI-Conversations/       所有 AI 對話（按話題分類，平台記錄喺 frontmatter）
2-Project-Management/     項目管理
   Projects/ Meetings/ Weekly-Reviews/ Tasks/
3-Knowledge-Base/         知識庫
   Concepts/ Summaries/ References/
4-Daily-Notes/            每日筆記
Templates/                筆記模板
Attachments/              附件
.scripts/                 自動化腳本同 CLI 工具
```

---

## Proma Agent 操作規範

### 讀取 vault
- 用 Glob / Read / Grep 直接操作 `D:\ObsidianVault\AINotes\`
- 路徑要用絕對路徑引用

### 寫入 vault
- 用 Write / Edit 直接建立同修改 .md 文件
- 所有新 Note 預設放 `0-Inbox/`，由用戶手動歸檔
- AI 對話放 `1-AI-Conversations/YYYY-MM-DD-主題.md`（**不按平台分目錄**，平台資訊放 frontmatter `source` 欄位）

### 常用 Workflow

1. **記錄對話：** 用 AI-Conversation 模板 → 填內容 → 放 `1-AI-Conversations/` → frontmatter 記錄 source + tags
2. **整理收件箱：** 讀取 `0-Inbox/` → 分類 → 移去對應目錄 → 加標籤同連結
3. **每週回顧：** 用 Weekly-Review 模板 → 掃描本週所有新 Note → 生成摘要
4. **搜尋知識：** 用 Grep 搜 tag 同 keyword → 匯總結果 → 生成洞察 Note

### 快速整理（一鍵自動化）

用 Python 自動化工具：
```
python .scripts/vault-tool.py status      # vault 狀態
python .scripts/vault-tool.py inbox       # 自動分類收件箱
python .scripts/vault-tool.py weekly      # 生成週報
python .scripts/vault-tool.py import x.md # 匯入對話
python .scripts/vault-tool.py tag x.md    # 加標籤
python .scripts/vault-tool.py connect x.md # 搵相關筆記
```

### 標籤系統

```
#ai/{platform}     — AI 來源（perplexity/qianwen/doubao/copilot/manus/gemini/proma-agent）
#topic/{topic}     — 主題分類
#daily             — 每日筆記
#meeting           — 會議記錄
#project           — 項目文件
#weekly-review     — 每週回顧
#status/inbox      — 未處理
#status/archived   — 已歸檔
```

---

## 整合要點（俾 LLM 記住）

1. 永遠用絕對路徑 `D:\ObsidianVault\AINotes\` 存取
2. 新 Note 預設放 `0-Inbox/`
3. 文件名格式：`YYYY-MM-DD-英文或中文簡述.md`
4. 善用 YAML frontmatter 嘅 `tags` 同 `status`
5. 用 `[[wikilink]]` 建立 Note 之間嘅關聯
