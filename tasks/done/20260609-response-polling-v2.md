---
created: 2026-06-09T20:52:00
original_task: 請幫我構思如何將 Obsidian 分發 (improved)
status: completed
source: proma-agent
---

# 回報：Polling 方案 v2 — 已實作

## 已建立檔案

### 1. vault-polling.py
位置：`.scripts/vault-polling.py`

改善點：
- 重複檔名自動加 timestamp 避 override
- utf-8-sig 編碼，減少亂碼
- POLL_SECS = 10
- 完善 logging 到 `.scripts/polling.log`

### 2. Task Scheduler 設定指引
位置：`Plugin/Plugin-polling-Task-Scheduler-設定.md`

## 總結
而家有兩個版本可以選擇：
- `vault-polling.py`（新）— 每 10 秒 polling + 自動重命名
- `watch-downloads.py`（舊）— 每 3 秒 polling（keep 住做 backup）

建議改行新版本，用 Task Scheduler 背景執行。
