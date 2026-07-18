# 2026-07-18 n8n Phase 1-4 完成 + Kanban 清理

## 摘要

3 小時內完成 Phase 1-4 roadmap，將 n8n 從零打造成 6 workflow + 7 cron job 嘅 operations hub。

---

## Phase 1: Consolidate
- Proma automation → n8n: ✅ Stock Alert + Git Sync（3 automation 退役）
- Hermes ↔ n8n 分工定義: ✅ Kanban v2 notice published
- Kanban 雙向通訊: ✅ HTTP Request + 5s timeout + Error fallback

## Phase 2: Automation Flows
- Stock Price Push: ✅ Yahoo Finance → n8n → Telegram（27 stocks, rate-limited）
- Backup Health: ✅ Daily 03:15 check dump size + count

## Phase 3: n8n as Monitor
- Kanban Health: ✅ 08:00, 18:00 check task counts
- Backup Health: ✅（Phase 2 完成）
- N8N Self Monitor: ✅ Every 30min health check

## Phase 4: Resilience
- Production Restore Drill: ✅ Script created（/opt/n8n/restore-drill.sh）
- External webhook/HTTPS: ⬜ deferred（no need yet）

## Kanban Cleanup
- 合併 3 張分工 notice → 1 張 v2 comprehensive card
- 刪除過時 SOP notices（t_903f60b3, t_1020910c）
- REF-工作日誌備忘 updated（+n8n sync info）
- 04-Logs reorganized into 2026/ subfolder

## 架構總覽

n8n workflows:
├── Stock Alert (Mon-Fri 18:55) — monitor Hermes reports
├── Git Sync (Mon-Fri 21:00) — sync work logs
├── Stock Price Push (Mon-Fri 16:30) — 27 stocks daily
├── Backup Health (Daily 03:15) — verify dumps
├── N8N Self Monitor (Every 30min) — check n8n alive
└── Kanban Health (Daily 08:00, 18:00) — check task counts

VPS cron:
├── backup.sh (03:00)
├── stock-dispatch.sh (18:55)
├── stock-price-push.py (16:30)
├── backup-health.py (03:15)
├── n8n-self-check.py (*/30)
└── kanban-health.py (08:00, 18:00)

Telegram Bot: @Stock_K281_bot
