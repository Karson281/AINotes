# 📐 Proma Worker 架構審查報告
Date: 2026-07-04
Status: ✅ 所有元件正常運作

## 審查摘要

全系統架構審查，包括：Kanban Bridge、Proma Worker、系統服務、定時任務。

## 架構總覽

```
Telegram → Hermes (You) → Kanban (dispatcher) → Proma Worker (systemd)
                              ↕ HTTP API
                         Kanban Bridge (port 8765)
```

## 腳本狀況

| Script | Path | Size | Permissions | Status |
|--------|------|------|-------------|--------|
| kanban-bridge.py | ~/.hermes/scripts/kanban-bridge.py | 5.7KB | 755 | ✅ v2, patched |
| proma-dispatch.sh | ~/.hermes/scripts/proma-dispatch.sh | 1.2KB | 600 | ✅ |
| proma-monitor.sh | ~/.hermes/scripts/proma-monitor.sh | 1.3KB | 600 | ✅ (cron) |
| proma-worker.py | ~/.hermes/scripts/proma-worker.py | 11.2KB | 755 | ✅ systemd |

## 系統服務

| Service | Status | PID | Port | Restart |
|---------|--------|-----|------|---------|
| kanban-bridge.service | ✅ active | 3565554 | 8765 | always/5s |
| proma-worker.service | ✅ active | 3538479 | — | always/10s |

## 橋接 API 端點驗證

| Endpoint | Method | Status | Note |
|----------|--------|--------|------|
| / | GET | ✅ | Endpoint documentation |
| /kanban/list | GET | ✅ | Returns task list |
| /kanban/stats | GET | ✅ | Board statistics |
| /kanban/create | POST | ✅ | Created test task |
| /kanban/claim | POST | ✅ | (verified in previous run) |
| /kanban/comment | POST | ✅ | **Bug fixed** |
| /kanban/complete | POST | ✅ | (verified via proma-worker) |

## 🔧 Bug Fixed: kanban-bridge.py comment endpoint

**問題**: POST `/kanban/comment` 用了不存在的 `--message` flag，導致所有經 HTTP API 的留言失敗。

**根源**: Line 124: `self._run_hermes("comment", task_id, "--message", message)`

**修復**: 改為 `self._run_hermes("comment", task_id, message)`

⚠️ **影響**: proma-worker.py 本身直接用 CLI（不是經 HTTP API），所以不受影響。個 bug 只影響外部 caller 用 HTTP POST 留言。

## 定時任務 (Cron Jobs)

| Job | Schedule | Type | Status |
|-----|----------|------|--------|
| hermes-update-check | Mon 19:00 UTC | agent | ✅ scheduled |
| Stock-Analysis-Dispatch | Mon-Fri 10:00 UTC | no_agent (script) | ✅ scheduled |
| Morning-Kanban-Check | Mon-Fri 01:00 UTC | agent | ✅ scheduled |
| EndOfDay-Summary | Mon-Fri 12:00 UTC | agent | ✅ scheduled |
| proma-monitor | every 5 min | no_agent (script) | ✅ scheduled |

**注意**: Cron schedules 係 UTC。轉 HKT (+8):
- Morning: 01:00 UTC = 09:00 HKT ✅
- Stock: 10:00 UTC = 18:00 HKT ✅
- EndOfDay: 12:00 UTC = 20:00 HKT ✅
- Update: 19:00 UTC Mon = 03:00 HKT Tue

## Proma Worker 處理記錄

已完成 6 個任務 (proma-worker assignee):
- 🧪 Test: Proma Worker Integration (t_028e349b)
- test msg (t_aa03025b)
- 🧪 Integration Test: 1+1=? (t_61549729)
- What is 2+2? Answer briefly (t_7e6e1cea)
- Calculate 5+3 and reply only the number (t_0b8a0225)
- 🧪 Post-bridge-fix test (t_892fe606)

## 板面狀態 (審查時)

- triage: 0, todo: 0, scheduled: 0, ready: 0, running: 1, blocked: 0, done: 14
- default: 5 done + 1 running (this task)
- proma-worker: 6 done
- stock-worker: 3 done

## 健康檢查清單

- [x] 所有 4 個腳本存在，權限正確
- [x] 兩個 systemd 服務正在運行
- [x] Kanban Bridge API 可存取 (port 8765)
- [x] proma-worker 能正常輪詢和執行任務
- [x] proma-monitor watchdog 定時運作 (每 5 分鐘)
- [x] proma-dispatch.sh 能正確 dispatch 任務
- [x] 無 pending task backlog
- [x] Bridge comment bug 已修復並驗證

## 下次 SOP 整合

依個架構文件可直接俾「每日例行 SOP」參考，確認所有服務正常後就可以跳過逐項檢查。
