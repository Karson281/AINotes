# 2026-07-17 n8n 部署、備份驗證與自動化遷移

## 摘要

完成 n8n 在 VPS 上的完整部署、Backup/Restore 隔離驗證、Telegram Bot 整合，並將 3 個 Proma 定時任務遷移至 n8n + cron/Windows Task，實現零 token 日常自動化。

---

## 一、Backup/Restore 隔離驗證（全部通過）

| Step | 工序 | 結果 |
|------|------|------|
| 1 | 手動執行 backup.sh | 348K .dump 成功 |
| 2 | 查看 backup log | 無靜默失敗 |
| 3 | restore-test.sh 隔離還原 | PASSED（獨立 container, --network none） |
| 4 | 測試 container 自動清理 | production 未受影響 |
| 5 | Windows offsite 副本 | D:\n8n-backups\ SCP pull 成功 |
| 6 | 記錄結果 | 已建立恢復基準 |

## 二、n8n Workflow 遷移

### Workflow #1: Stock Alert
- Trigger: VPS cron (Mon-Fri 18:55) → POST n8n webhook
- Logic: IF stock files >= 5 → Telegram OK / ELSE → Telegram Alert
- Webhook: /stock-check | Bot: @Stock_K281_bot

### Workflow #2: Git Sync
- Trigger: Windows Scheduled Task (Mon-Fri 21:00) → POST n8n webhook
- Logic: IF git push success → Telegram OK / ELSE → Telegram Alert
- Webhook: /git-sync

### 已停用的 Proma 自動化
- 監察 Hermes 股市報告 (19:27) → n8n Stock Alert
- Git Pull 股票分析報告 (19:00) → n8n Stock Alert
- Git Sync 工作日誌 (21:00) → n8n Git Sync

**Token 節省：每日 3 次 AI agent run → 0。**

## 三、Hermes 時區修正

- VPS system: HKT +0800
- config.yaml system_prompt: 加入強制時區規則
- Gateway 已重啟

## 四、待辦後續

- [ ] Windows Scheduled Task 自動 pull backup
- [ ] Production restore drill（維護時段）
- [ ] Roadmap ① Hermes ↔ n8n 分工定義
- [ ] Roadmap ② 首批 Automation Flows
