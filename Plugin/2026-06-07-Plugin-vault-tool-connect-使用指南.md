# vault-tool.py connect 使用指南

## 用途
搵出同指定筆記相關嘅其他 Note（關鍵字匹配），列出 [[wikilink]]。

## 用法

```bash
cd /c/Users/kaisu/OneDrive/AINotes
python3 .scripts/vault-tool.py connect "資料夾/檔案名.md"
```

## 範例

```bash
python3 .scripts/vault-tool.py connect "旅行/2026-06-07-美國搭飛機行李打包指南-Google-Gemini.md"
```

輸出：

```
Related notes found (3):
  [[2026-06-07-加州旅遊小費與安全指南]]  (match: 旅行)
  [[2026-06-07-OAK-機場附近-Costco-油站防盗指引]]  (match: 美國)
  [[2026-06-07-消費-網購信用卡套利方案]]  (match: 行李)
```

## 注意
- 結果只顯示喺 Terminal，唔會寫入檔案
- Keyword 係自動抽嘅（中文詞 + 英文專有名詞）
- 唔需要 API Key，100% 本地
