---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-Hermes Agent-deepseek+vl-plus 設定

## 功能描述
Hermes Agent (VPS) 使用 deepseek-chat 做主模型（文本推理），qwen-vl-plus 做 auxiliary vision model（圖片分析）。主模型 + vision 分離，各取所長。

## 設定位置
- **VPS Config：** `~/.hermes/config.yaml`
- **API Keys：** `~/.hermes/.env`

## Config 內容
```yaml
model:
  default: deepseek-chat
  provider: custom
  base_url: https://api.deepseek.com/v1
  api_key: $DEEPSEEK_API_KEY

auxiliary:
  vision:
    provider: custom
    model: qwen-vl-plus
    base_url: https://ws-08jd1r0pnb7v5sgv.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    api_key: $QWEN_VL_API_KEY
    max_tokens: 32768
```

## .env 檔案
```bash
# ~/.hermes/.env
DEEPSEEK_API_KEY=sk-xxx
QWEN_VL_API_KEY=sk-ws-xxx
chmod 600 ~/.hermes/.env
```

## 使用方法
```bash
# 一般對話（用 deepseek）
hermes chat

# 叫佢分析圖片（自動 call qwen-vl-plus）
hermes chat
# 然後輸入：幫我分析呢張圖：https://...
```

## 語法要點
- `auxiliary.vision` 定義 vision 專用模型
- API key 用環境變數 `$DEEPSEEK_API_KEY` 引用 .env，避免寫死喺 config
- `max_tokens: 32768` 避免 qwen-vl-plus 嘅 token 超出限制

## 實例
```
你 → 幫我分析呢張圖：https://upload.wikimedia.org/wikipedia/commons/3/3b/Dog_Breeds.jpg
Hermes → [vision] 這是黃金獵犬幼犬的可愛照片...
```

## 相關檔案
- [[成功-Hermes Agent-vision功能測試]]
- [[有待跟進-Hermes Agent-VPS重啟model名]]
