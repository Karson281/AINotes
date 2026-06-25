# AI 對話匯入指南（俾人類同 Agent 用）

## 通用流程

1. 喺對應 AI 工具複製對話內容
2. 用 AI-Conversation 模板建立新 Note
3. 填寫來源、主題、關鍵要點
4. 加上適當標籤
5. 連接相關筆記（[[wikilink]]）

---

## 各平台匯出方式

### Perplexity
- **方法：** 分享對話 → 複製連結 / 直接複製內容
- **建議標籤：** `#ai/perplexity`

### 千問
- **方法：** 複製對話內容 / 截圖 + OCR
- **建議標籤：** `#ai/qianwen`

### 豆包
- **方法：** 複製對話內容
- **建議標籤：** `#ai/doubao`

### Copilot
- **方法：** 複製對話內容
- **建議標籤：** `#ai/copilot`

### Manus
- **方法：** 複製對話內容
- **建議標籤：** `#ai/manus`

### Gemini
- **方法：** Gemini 有匯出功能 / 複製連結
- **建議標籤：** `#ai/gemini`

### Proma Agent
- **方法：** 直接由 Proma Agent 寫入 vault
- **建議標籤：** `#ai/proma-agent`
- **自動化：** Agent 直接 Read/Write，唔使手動

---

## 批量匯入建議

一次過匯入大量對話時：
1. 每條對話一個 .md 文件
2. 文件名格式：`YYYY-MM-DD-主題簡述.md`
3. 文件放 `1-AI-Conversations/` 目錄
4. 批量處理可用 .scripts/ 入面嘅工具
