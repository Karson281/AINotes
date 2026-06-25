---
prefix: 成功
status: completed
created: 2026-06-21
---

# 成功-Hermes Agent-Telegram Bot + Tasks Automation

## 功能描述
手機 Telegram 可以直接同 Hermes Agent 對話，查股票、分析、問問題。同時 VPS crontab 每 10 分鐘自動檢查 Obsidian 03-Tasks/Pending/ 有新任務時通知用家。

## Telegram 設定
Bot Token：由 @BotFather 建立，已寫入 config.yaml

```yaml
telegram:
  enabled: true
  bot_token: "8644362320:AAF_YYR8NmT44HXPyKmzOu-lWrWkpDEtOR0"
  allowed_user_ids: []
```

## Tasks Monitoring Crontab
檔案：`~/scripts/check-tasks.sh`
排程：每 10 分鐘執行
功能：scan Pending/ 有新 file → Telegram 通知用家

```bash
*/10 * * * * /bin/bash ~/scripts/check-tasks.sh
```

## 每日股票分析 Cron Job
```bash
# 港股 18:00 HKT
hermes cron create "0 10 * * 1-5" --prompt "$(cat ~/.hermes/prompts/stock-analysis-prompt.md)" --name "Daily-HK-US-Stock-Analysis" --skill "finance-stocks"
```

## 使用方式
📱 手機 Telegram → Bot → 直接問：「分析 0941.HK」
💻 電腦 Proma → 深度分析
📝 Obsidian 03-Tasks/ → Agent 之間任務傳遞

## 相關檔案
- [[成功-Hermes Agent-Tailscale+Obsidian proxy 打通]]
- [[成功-整合哲學-Hermes+Proma+Obsidian 協作架構]]
