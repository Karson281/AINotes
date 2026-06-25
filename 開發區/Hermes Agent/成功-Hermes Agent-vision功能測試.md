---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-Hermes Agent-vision 功能測試

## 功能描述
驗證 Hermes Agent 嘅 auxiliary vision (qwen-vl-plus) 可以正確分析圖片內容。

## 測試方法
喺 `hermes chat` 模式輸入：
```
幫我分析呢張圖：https://upload.wikimedia.org/wikipedia/commons/3/3b/Dog_Breeds.jpg
```

## 成功指標
Hermes 會顯示 `👁️ vision` 標籤，代表使用了 auxiliary vision model。然後返回圖片分析內容。

## 實例
```
你 → 幫我分析呢張圖：https://upload.wikimedia.org/wikipedia/commons/3/3b/Dog_Breeds.jpg
Hermes → 👁️ vision  [6.3s]
         這是黃金獵犬（Golden Retriever）幼犬的可愛照片...
         - 品種：黃金獵犬幼犬
         - 構圖：幼犬居中躺臥在草地上
         - 光線：柔和自然光
```

## 注意事項
- Wikimedia 等網站有時會 block curl download，但 Hermes 會自動 fallback 用 browser 攞圖
- Vision 分析需時約 5-10 秒

## 相關檔案
- [[成功-Hermes Agent-deepseek+vl-plus設定]]
