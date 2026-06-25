---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-Proma Agent-Deepseek 主模型

## 功能描述
Proma Agent 使用 deepseek-v4-flash 做主模型。可透過 Proma UI 下拉選單自由切換到 deepseek-v4-pro / qwen-vl-max / qwen3.5-omni-plus。

## 設定位置
- **Config 檔：** `C:\Users\kaisu\.proma\settings.json`

## Config 內容
```json
"agentModelId": "deepseek-v4-flash"
```

## 使用方法
1. 開 Proma 桌面 App
2. 左下角模型下拉選單 → 直接揀 model
3. 開新 Tab 即刻生效

## 語法要點
- **唔好手動改 settings.json**，官方會重設，改 UI 下拉選單就得
- UI 支援嘅 models：`deepseek-v4-flash`, `deepseek-v4-pro`, `qwen-vl-max`, `qwen3.5-omni-plus`
- 每次切換後開新 Tab 先用新 model

## 相關檔案
- [[成功-Proma Agent-Qwen-vision MCP tool]]
- [[有待跟進-Proma Agent-vision MCP自啟服務]]
