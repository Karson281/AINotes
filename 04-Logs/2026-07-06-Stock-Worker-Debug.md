---
tags:
  - log
  - stock-analysis
  - hermes
  - kanban
  - debug
date: 2026-07-06
---

# Stock Worker Debug & Fix — 2026-07-06

## 問題
18:00 股票分析 blocked，stock-worker 掛咗，冇出報告。

## Root Cause
VPS 上 `DEEPSEEK_KEY` 環境變數過期（今早 regenerate 咗新 key，Bitwarden 未同步），`stock_daily_v2.py` call DeepSeek API 全部 401 → Hermes mark task blocked。

## 修復過程

### 1. 更新 DEEPSEEK_KEY
- VPS 上 `nano ~/.bashrc` 更新 `export DEEPSEEK_KEY`
- `source ~/.bashrc` 生效

### 2. stock_daily_v2.py crontab（舊方案）
- 加入 crontab：`0 18 * * 1-5 source ~/.bashrc && cd /root/vault && python3 stock_daily_v2.py`
- 手動測試：全部 19 隻完成，但分析質素不及 Hermes（yfinance 數據舊、全部出「密切觀察」）

### 3. Hermes Kanban Dispatch（✅ 最佳方案）
- 透過 kanban API create task → Hermes 直接做分析（web search + DeepSeek）
- 測試成功：19 份個股報告 + 1 份摘要，質素遠超 stock_daily_v2.py
- Crontab 格式：
```
0 18 * * 1-5 curl -s -X POST http://localhost:8765/kanban/create -H "Content-Type: application/json" -d '{"title":"📊 Daily Stock Analysis","body":"Analyze all 19 stocks in /root/vault/stock-watchlist.json. Use web search for real-time prices. Apply stock analysis parameters. Write reports to /root/vault/02-Wiki/Stocks/. Git push.","assignee":"default","priority":1}'
```

## 關鍵發現
- Hermes ≠ stock-worker（stock-worker 係獨立 process，已死）
- Kanban dispatch → Hermes 直接分析 係最穩定方案（唔經 stock-worker）
- Kanban task body 要簡短（太長會 502），keyword "stock analysis" + "web search" 即可觸發 Hermes

## 待辦
- [ ] 🔴 **將 VPS crontab 換成 kanban dispatch**（目前仲係 stock_daily_v2.py）
- [ ] Fix VPS SSH（port 22 拒絕連線）
- [ ] Proma 19:00 Git Pull 股票分析報告 繼續 keep（sync VPS 其他改動）
