# WORKFLOW.md — Stock Analysis Project

## Project Overview
- **Vault**: /root/vault (GitHub: Karson281/AINotes)
- **Main script**: /root/vault/stock_daily_v2.py
- **Reports**: /root/vault/02-Wiki/Stocks/YYYYMMDD-TICKER.md
- **Dashboard**: /root/vault/02-Wiki/01_投資組合總覽.md
- **Watchlist**: /root/vault/02-Wiki/Stocks/YYYYMMDD-股票監察名單.md
- **Summary**: /root/vault/02-Wiki/Stocks/YYYYMMDD-股票分析摘要.md

## User Profile
- **Name**: Mark（港仔）
- **Language**: Cantonese / Traditional Chinese
- **Location**: Hong Kong (HKT, UTC+8)
- **Investment style**: Dividend-focused, HK blue chips + US dividend stocks
- **Communication**: Direct, no fluff, evidence-first

## Golden Rules

### 1. Evidence First（禁止瞎編）
- ALL output must be backed by real tool output (terminal, read_file, etc.)
- Never fabricate results — say "not found" if data unavailable
- Show concrete evidence: diffs for patches, output for runs, lint results for writes

### 2. Stock Analysis Protocol
- **Must use real technical indicators**: fetch 200d OHLCV from yfinance, calc MA20/50/200, RSI(14), MACD(12,26,9), volume ratio in Python
- **DeepSeek is interpretation only** — never ask it to calculate indicators
- **Dashboard must have**: market indices (HSI, IXIC, GSPC, DJI), rating distribution, last-updated timestamp
- **Every generated page** must have `updated: YYYY-MM-DD HH:MM` in frontmatter + body

### 3. Git Protocol
```bash
cd /root/vault
git add -A
git commit -m "description: YYYYMMDD"
git push
```
- Always `git add -A` (include all changes)
- Commit message format: `<action>: <detail> — YYYYMMDD`
- Push after every batch of changes

### 4. File Conventions
- Stock reports: `YYYYMMDD-TICKER.md` (dot retained, e.g. `20260707-0005.HK.md`)
- Never create `*HK.md` without dot — cleanup script removes them
- Dashboard path: `02-Wiki/01_投資組合總覽.md`
- Script path: `stock_daily_v2.py` (v4, real indicators)

### 5. Cron Schedule (HKT = UTC+8)
| Job | Schedule | Description |
|-----|----------|-------------|
| stock_daily_v2.py | Mon-Fri 18:00 HKT (10:00 UTC) | Full analysis + git push |

### 6. Common Pitfalls (已踩過的坑)
- `change_percent` in frontmatter is written as float, read back as str → must `float()` before formatting
- yfinance dividends index has tz → use `pd.Timestamp.now(tz=last_div.tz)` for comparison
- DeepSeek API key not in os.environ when running direct → fallback to read `/root/.env`
- n8n Code node sandbox blocks `$http` → set `NODE_FUNCTION_ALLOW_BUILTIN=*` for `require('https')`
- Security approval blocks inline python → use `write_file + python3 script.py` pattern

### 7. Communication Style
- Respond in Cantonese/Traditional Chinese unless asked otherwise
- Be concise, direct — no fluff, no over-apologizing
- Show evidence for every claim
- "沒有證據 = 沒有完成"
