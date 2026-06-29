---
creation_date: 2026-06-29
source: "manus"
tags:
  - topic/untagged
status: inbox
---

# 自動化-Google MCP生態自動化實用例子列表 - Manus

**Date:** 2026-06-29 01:41

---

# 建立並設定 Google 專屬 Agent
hermes profile create google-ops --description "負責 Google 生態系操作與排程"
# 在 ~/.hermes/profiles/google-ops/.env 中填入新 Bot Token 與 Google OAuth 憑證

# 建立並設定一般任務 Agent (使用舊 Bot Token)
hermes profile create general-ops --description "負責網頁研究、程式碼編寫與 Obsidian 筆記"
# 在 ~/.hermes/profiles/general-ops/.env 中填入舊 Bot Token

