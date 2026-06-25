---
created: 2026-06-09T19:51:00
original_task: 請幫我構思如何將 Obsidian 分發
status: completed
source: proma-agent
---

# 回報：Watcher 改 Polling 方案

## 分析

現有 `watch-downloads.py` 其實已經係 polling（每 3 秒掃描一次），但有以下問題：
1. 冇自動重啟機制 — 死咗就停
2. 用 `os.kill` 做 PID check，Windows 下唔穩定
3. 冇 log 記錄，死咗唔知

## 建議方案：一個 batch + polling loop

分兩個檔案：

### 1. 啟動器（vault-polling.bat）

放喺 `.scripts/` 或 startup folder，簡單可靠：

```batch
@echo off
:restart
title Vault Polling Agent
python3 "C:\Users\kaisu\OneDrive\AINotes\.scripts\vault-polling.py"
echo %date% %time% - Watcher crashed, restarting... >> "C:\Users\kaisu\OneDrive\AINotes\.scripts\polling.log"
timeout /t 5 /nobreak >nul
goto restart
```

特性：crash 後 5 秒自動重啟，無限 loop。

### 2. Polling 主程式（vault-polling.py）

```python
#!/usr/bin/env python3
"""Polling-based vault classifier. Watches Downloads + inbox."""
import re, shutil, time, sys, logging
from pathlib import Path

VAULT = Path("C:/Users/kaisu/OneDrive/AINotes")
DOWNLOADS = Path.home() / "Downloads"
INBOX = VAULT / "0-Inbox"
LOG = VAULT / ".scripts" / "polling.log"
POLL_SECS = 5

FOLDERS = ["模型","NAS","建站","文件","Plugin","提示詞","Agent","知識庫","投資",
           "系統","VPS","保險","Proma","Apps","編程","旅行","ESTA","自駕遊",
           "自動化","醫療","試題","通訊","消費"]

logging.basicConfig(filename=LOG, level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("polling")

def classify(content, stem):
    m = re.search(r'^#\s+(.+?)(?:[：:\-_\s]|$)', content, re.MULTILINE)
    prefix = m.group(1).strip() if m else stem
    for f in FOLDERS:
        if prefix.startswith(f): return f
    clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', stem)
    for f in FOLDERS:
        if stem.startswith(f) or clean.startswith(f): return f
    return None

def scan(src_dir):
    for f in list(src_dir.glob("*.md")):
        time.sleep(0.5)
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            folder = classify(content, f.stem)
            dst = (VAULT / folder / f.name) if folder else (INBOX / f.name)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(dst))
            log.info(f"Moved: {f.name} -> /{folder or 'inbox'}/")
        except Exception as e:
            log.error(f"Error: {f.name} -> {e}")

if __name__ == "__main__":
    log.info("=" * 40)
    log.info("Polling agent started (PID %d)", __import__("os").getpid())
    while True:
        try:
            scan(DOWNLOADS)
            scan(INBOX)
        except Exception as e:
            log.error("Scan error: %s", e)
        time.sleep(POLL_SECS)
```

## 優點
- .bat 自動重啟，死咗即刻 rebirth
- 有 log 可以追蹤問題
- 比 watchdog 更簡單，唔使裝額外套件
- CPU 用量 ~0%

## 安裝
1. 將 `vault-polling.py` 放入 `.scripts/`
2. 將 `vault-polling.bat` 放入 Startup folder
3. 雙擊 .bat 啟動（或 reboot）
