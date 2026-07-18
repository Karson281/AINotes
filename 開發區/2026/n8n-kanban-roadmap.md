# n8n + Kanban Operations Hub — Roadmap 2026

> 建立日期: 2026-07-18
> 核心原則：AI 只用於策略/分析/創作層面；n8n + Kanban 接管所有 rule-based 自動化、監察與路由

---

## 架構理念

```
AI (Hermes/Proma)     策略、分析、創作、決策（燒 token，用得其所）
     │
     ├──→ Kanban ←── 任務路由、狀態追蹤、進度視覺化（零 token）
     │       │
     │       └──→ n8n ←── 自動化、監察、排程、通知（零 token）
     │
     └── AI 只落在 n8n/Kanban 做唔到嘅策略層面
```

---

## Phase 1: Consolidate（鞏固現有）

| # | 項目 | 細節 | 狀態 |
|---|------|------|------|
| 1 | Proma automation → n8n | Stock Alert + Git Sync 遷移完成 | ✅ |
| 2 | Hermes ↔ n8n 分工定義 | 邊啲 task 歸 Hermes，邊啲歸 n8n | ⬜ |
| 3 | Kanban 雙向通訊 | n8n ↔ Kanban API，task 自動建立與狀態更新 | ⬜ |

## Phase 2: n8n Automation Flows

| # | 項目 | 細節 |
|---|------|------|
| 4 | Stock price fetch + Telegram push | n8n 定時 fetch 股價 → Telegram |
| 5 | 其他 rule-based workflow | 按需求逐步建立 |

## Phase 3: n8n as Monitor（監察層）

| # | 項目 | 細節 |
|---|------|------|
| 6 | 監察 Hermes 進度 | Kanban task 逾時 → n8n alert |
| 7 | 監察 backup health | dump size / count / offsite → alert |
| 8 | n8n self-monitor | workflow error → Telegram + Kanban task |

## Phase 4: Resilience & Access

| # | 項目 | 細節 |
|---|------|------|
| 9 | Production restore drill | 維護時段，先做安全 backup + 確認回滾 |
| 10 | 外部 webhook / HTTPS | Coolify / reverse proxy / 證書（需要時才做） |

---

## Token 節省估算

| 已遷移 | 原 Proma automation | 日節省 |
|--------|-------------------|--------|
| Stock Alert + VPS cron | 監察 Hermes 股市報告 + Git Pull | ~3 min AI |
| Git Sync + Windows Task | Git Sync 工作日誌 | ~2 min AI |
| **合計** | **3 個 automation** | **~5 min AI / 日** |

後續 Phase 2-3 將繼續將更多 rule-based 工作從 AI 移至 n8n。
