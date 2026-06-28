# Polling Agent — Task Scheduler 設定

## 目標
背景執行 `vault-polling.py`，開機自動啟動，唔顯示 CMD 視窗。

## 步驟

### 1. 開 Task Scheduler
- Windows 鍵 → 打 `Task Scheduler` → Enter

### 2. 建立基本任務
- 右邊 **「Create Basic Task」**
- **Name:** `Vault Polling Agent`
- **Trigger:** 揀 **「When the computer starts」**
- **Action:** 揀 **「Start a program」**

### 3. 設定程式
- **Program/script:** `python3`
- **Arguments:** `"C:\Users\kaisu\OneDrive\AINotes\.scripts\vault-polling.py"`
- **Start in:** `C:\Users\kaisu\OneDrive\AINotes`

### 4. 完成後，改進階設定
- 喺 Task Library 揀返 `Vault Polling Agent` → 右鍵 **Properties**
- **General tab:**
  - ☑ **Run whether user is logged on or not**（隱藏視窗）
  - ☑ **Run with highest privileges**
- **Settings tab:**
  - ☑ **Allow task to be run on demand**
  - ☑ **If the task fails, restart every 5 minutes**
  - ☑ **Stop the task if it runs longer than: 3 days**

### 5. 測試
- 右鍵 Task → **Run**
- Check log:
```
notepad C:\Users\kaisu\OneDrive\AINotes\.scripts\polling.log
```

## 停用
- Task Scheduler → 右鍵 **Disable** 或 **Delete**

## 手動啟動（唔用 Task Scheduler）
想即時行：
```bash
python3 C:/Users/kaisu/OneDrive/AINotes/.scripts/vault-polling.py
```
