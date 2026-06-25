---
status: completed
tags:
  - project/obsidian-integration
  - project/completed
start_date: 2026-05-30
end_date: 2026-05-30
---

# Obsidian × AI 工具整合建置記錄

## 背景
整合 7 個 AI 工具（Perplexity、千問、豆包、Copilot、Manus、Gemini、Proma Agent）嘅對話到 Obsidian vault，統一知識管理。

## 建置內容

### 目錄結構
```
0-Inbox/                  ← 臨時收件箱
1-AI-Conversations/       ← AI 對話紀錄（全部 flat 存放）
2-Project-Management/     ← 項目管理
  Projects/ Meetings/ Weekly-Reviews/ Tasks/
3-Knowledge-Base/         ← 知識庫
  Concepts/ Summaries/ References/
4-Daily-Notes/            ← 每日筆記
Templates/                ← 筆記模板
Attachments/              ← 附件
.scripts/                 ← 自動化 CLI 工具
```

### 特點
- AI 對話**按話題分類**，**不按平台分目錄**
- 平台來源記錄喺 frontmatter `source` 欄位 + `#ai/{platform}` tag

### 模板（5 個）
| 模板                           | 用途      |
| ---------------------------- | ------- |
| Templates/AI-Conversation.md | AI 對話記錄 |
| Templates/Daily-Note.md      | 每日筆記    |
| Templates/Meeting-Note.md    | 會議記錄    |
| Templates/Project-Note.md    | 項目追蹤    |
| Templates/Weekly-Review.md   | 每週回顧    |

### 自動化工具
`.scripts/vault-tool.py` — Python CLI，支援：
- `status` — vault 統計
- `list` — 列出筆記
- `import <file>` — 匯入對話（自動偵測平台 + 自動 tag）
- `tag <file>` — 自動標籤
- `connect <file>` — 搵相關筆記
- `inbox` — 處理收件箱
- `weekly` — 生成週報

### Proma Agent 整合
- Vault 路徑已記錄到 Proma 記憶系統
- CLAUDE.md 已寫入 vault 根目錄，記錄操作規範
- Proma Agent 可直接透過 Read/Write/Edit/Glob/Grep 讀寫 vault

### Obsidian 設定
- Templates 插件指向 Templates/
- Daily Notes 指向 4-Daily-Notes/
- 新檔案預設 0-Inbox/
- 附件去 Attachments/
- Markdown links 啟用

### Local REST API
- Port: 27124 (HTTPS)
- 插件：obsidian-local-rest-api
- 可用於外部程式操作 vault

## 用法速記

### 記錄對話
就咁同 Proma Agent 講：「幫我記低呢段對話」即可，Agent 會自動：
1. 偵測邊個 AI 平台
2. 分析內容關鍵字，自動加 `#topic/xxx` 標籤
3. 格式化寫入 `1-AI-Conversations/YYYY-MM-DD-主題.md`

### 整理收件箱
- 手動：`python .scripts/vault-tool.py inbox`
- 或叫 Proma Agent：「幫我整理收件箱」

### 每週回顧
- 手動：`python .scripts/vault-tool.py weekly`
- 或叫 Proma Agent：「幫我生成週報」

## 標籤系統
- `#ai/perplexity` `#ai/qianwen` `#ai/doubao` `#ai/copilot` `#ai/manus` `#ai/gemini` `#ai/proma-agent`
- `#topic/python` `#topic/javascript` `#topic/database` `#topic/devops` `#topic/ai-ml` 等
- `#daily` `#meeting` `#project` `#weekly-review`
- `status: inbox / reviewed / archived`

## 關鍵決策
- AI 對話**不分平台目錄**，只用 frontmatter 記錄來源（用戶明確要求）
- 雙軌整合：直接檔案存取（主要）+ Local REST API（輔助）
