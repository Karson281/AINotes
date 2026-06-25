---
source: proma-agent
tags:
  - ai/proma-agent
  - topic/google
  - topic/mcp
  - reference
  - automation
created: 2026-06-06
---

# Google MCP 自動化工具參考手冊

> Google Workspace MCP Server — 53 個工具，涵蓋 Gmail、Calendar、Drive、Docs、Sheets、Slides

## 快速開始

直接對 Proma Agent 講 natural language 就得：
- 「今日有咩 email？」
- 「聽日有咩行程？」
- 「幫我搵份 Budget file」
- 「幫我開個新 Doc 叫週會記錄」

---

## Gmail（3）

| 你想做咩 | 點樣問 | 底層工具 |
|---------|--------|---------|
| 睇今日 email | 「今日有咩新 email？」 | `gmail_messages_list` |
| 搜尋特定 email | 「搵 Amy 寄俾我啲 email」 | `gmail_messages_list` |
| 睇 email 詳細內容 | 「睇下呢封講咩」 | `gmail_message_get` |
| 跨帳戶 | 「check 晒全部 account」 | `gmail_messages_list_all_accounts` |

搜尋語法：`from:xxx` `subject:xxx` `after:2026/01/01` `is:unread`

---

## Calendar（4）

| 你想做咩 | 點樣問 | 底層工具 |
|---------|--------|---------|
| 睇行程 | 「今日有咩 meeting？」 | `calendar_events_list` |
| 建立活動 | 「聽日下晝 3 點加牙醫 appointment」 | `calendar_event_create` |
| 列出日曆 | 「我嘅行事曆列表」 | `calendar_list` |
| 跨帳戶 | 「check 晒全部 account 行程」 | `calendar_events_list_all_accounts` |

---

## Drive（16）

| 你想做咩 | 點樣問 | 底層工具 |
|---------|--------|---------|
| 列出檔案 | 「最近改過咩 file？」 | `drive_files_list` |
| 搜尋檔案 | 「搵 Budget 2026」 | `drive_files_search` |
| Download | 「Download 份 report 俾我」 | `drive_file_download` |
| Upload | 「Upload 呢個 file 上 Drive」 | `drive_file_upload` |
| Markdown → Doc | 「將呢段 Markdown 上傳做 Doc」 | `drive_markdown_upload` |
| 更新 Doc | 「更新份 Doc 嘅內容」 | `drive_markdown_replace` |
| 開 Folder | 「開個新 folder 叫 Project Alpha」 | `drive_folder_create` |
| 搬/複製/刪除 | 「搬去第二個 folder / copy / delete」 | `drive_file_move/copy/delete` |
| 垃圾桶 | 「丟入垃圾桶 / 還原」 | `drive_file_trash/restore` |
| 分享 | 「整條分享 link」 | `drive_shared_link_create` |
| 權限 | 「加俾阿 May 可以睇」 | `drive_permissions_create` |
| 跨帳戶 | 「search 晒全部 account」 | `drive_files_list_all_accounts` |

---

## Docs（3）

| 你想做咩 | 點樣問 | 底層工具 |
|---------|--------|---------|
| 建立新文檔 | 「開個新 Doc 叫『週會記錄』」 | `docs_document_create` |
| 睇文檔內容 | 「幫我睇份 meeting notes」 | `docs_document_get` |
| 更新文檔 | 「幫我喺份 Doc 加新內容」 | `docs_document_update` |

---

## Sheets（3）🔥 新加入

| 你想做咩 | 點樣問 | 底層工具 |
|---------|--------|---------|
| 讀取試算表 | 「幫我睇份報價表嘅內容」 | `sheets_spreadsheet_get` |
| 讀取儲存格 | 「拎 A1:B10 嘅資料出嚟」 | `sheets_values_get` |
| 更新儲存格 | 「將 B2 格改做 100」 | `sheets_values_update` |

**應用實例：**
- 「幫我讀取 Budget 試算表嘅 A 欄」
- 「將 inventory sheet 嘅 C5 格更新為『已出貨』」
- 「睇下份 sales report 嘅總計係咩」

> 建立新 Sheet 可用 web UI 開，或者用 `drive_markdown_upload` 將 Markdown 表格上傳做 Sheets

---

## Slides（17）

| 你想做咩 | 點樣問 | 底層工具 |
|---------|--------|---------|
| 建立簡報 | 「開個新簡報叫 Q3 Review」 | `slides_presentation_create` |
| **Markdown → Slides** 🔥 | 「將呢段 Markdown 變成 Slides」 | `slides_markdown_create` |
| 更新簡報（MD） | 「更新呢份簡報」 | `slides_markdown_update` |
| 加 Slide | 「加多張 slide」 | `slides_slide_create` |
| 刪除 Slide | 「刪咗第三張」 | `slides_slide_delete` |
| 複製 Slide | 「複製第一張」 | `slides_slide_duplicate` |
| Export PDF | 「幫我 export 做 PDF」 | `slides_export_pdf` |
| 分享 | 「分享俾同事 edit」 | `slides_share` |
| 跨帳戶 | 「search 全部 account 嘅簡報」 | `slides_presentations_list_all_accounts` |

---

## 帳戶管理（5）

| 工具 | 用途 |
|------|------|
| `accounts_list` | 列出已連接嘅 Google 帳戶 |
| `accounts_details` | 睇帳戶詳細資料 |
| `accounts_add` | 加新 Google 帳戶 |
| `accounts_remove` | 移除帳戶 |
| `accounts_refresh` | 刷新 token |

---

## 注意事項

- Bridge 需要長開先用到（已設開機自動啟動）
- Token 自動 refresh，唔使手動更新
- 所有 Google API 都係免費配額，唔會額外收費
- Google Cloud 免費試用到 2026-09-05，$300 額度
