---
type: system-audit
date: 2026-07-09
status: completed
component: stock-worker-workflow
---

# 🔧 Stock-Worker Workflow Fix — 2026-07-09

## Problem
Stock-worker Kanban cards were being marked `blocked` even when analysis reports existed on disk. This created false alarms.

**Root causes:**
1. **API key mismatch** (original 401 error, ending `0320` — fixed earlier)
2. **No auto-completion safety net** — when the LLM agent session ended without calling `kanban_complete`, the card stayed `running` → timed out → marked `blocked` (after 14400s = 4hr default)
3. **Dispatch instructions vague** — said "call kanban_complete" but no fallback if agent forgot

## Changes Made

### 1. `daily-stock-dispatch.sh` — 監察系統 phase added
**File:** `/root/.hermes/scripts/daily-stock-dispatch.sh`

New **Phase 1**: Before creating today's card, scans all non-done stock-worker cards:
- Extracts date from card title
- Checks if reports exist on disk (`02-Wiki/Stocks/{date}-*.md`)
- If ≥15 reports found → auto-completes the stuck card
- This prevents the false alarm cycle

Also added **Phase 3 pre-check**: Skip card creation entirely if today's reports already exist.

### 2. `stock_daily_v2.py` — Self-healing auto-complete
**File:** `/root/vault/stock_daily_v2.py`

At the end of `analyze_all()`, after successful analysis + git push:
- Runs `hermes kanban list --json`
- Finds any `stock-worker` card in `running`/`blocked` state for today
- Auto-completes it via `hermes kanban complete <id>`
- This is the **last line of defense** — the script itself ensures cleanup

### 3. Agent instructions clearer
Dispatch script's ANALYSIS_BODY now says:
- **CRITICAL**: After analysis, `IMMEDIATELY call \`kanban_complete\``
- Explicitly: "Do NOT let the session end without calling kanban_complete"

## Architecture — 三層安全網

```
Layer 1: Dispatch pre-check
  └─ Before creating card → check stuck cards + rescue them
Layer 2: LLM agent instructions
  └─ "Call kanban_complete before session ends"
Layer 3: Script auto-complete (last resort)
  └─ stock_daily_v2.py completes any stuck card for today
```

This ensures reports-on-disk = card-complete, regardless of agent behavior.

## Verification
- `bash -n daily-stock-dispatch.sh` ✅ Syntax OK
- `python3 -c "ast.parse(...)"` ✅ Python syntax OK
- Current Kanban: all stock-worker cards ✅ done/no blocked cards
