#!/usr/bin/env python3
"""
vault-polling.py — 定時掃描 Downloads + inbox，自動分類至對應 folder。
改善：
  1. 重複檔名自動加 timestamp
  2. utf-8-sig 編碼，避免亂碼
  3. POLL_SECS = 10，更慳資源
  4. 完善 logging
用法：python3 vault-polling.py
建議用 Task Scheduler 背景執行，隱藏視窗。
"""
import re, shutil, time, logging
from pathlib import Path

VAULT = Path("C:/Users/kaisu/OneDrive/AINotes")
DOWNLOADS = Path.home() / "Downloads"
INBOX = VAULT / "0-Inbox"
LOG_FILE = VAULT / ".scripts" / "polling.log"
POLL_SECS = 10

FOLDERS = [
    "模型", "NAS", "建站", "文件", "Plugin", "提示詞", "Agent",
    "知識庫", "投資", "系統", "VPS", "保險", "Proma", "Apps",
    "編程", "旅行", "ESTA", "自駕遊", "自動化", "醫療", "試題", "通訊", "消費",
]

logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)
log = logging.getLogger("polling")

def classify(content, stem):
    """Detect target folder from H1 title or filename stem."""
    m = re.search(r'^#\s+(.+?)(?:[：:\-_\s]|$)', content, re.MULTILINE)
    prefix = m.group(1).strip() if m else stem
    for f in FOLDERS:
        if prefix.startswith(f):
            return f
    clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', stem)
    for f in FOLDERS:
        if stem.startswith(f) or clean.startswith(f):
            return f
    return None

def safe_move(src, dst):
    """Move file, auto-rename if destination exists."""
    if dst.exists():
        stem = dst.stem + f"_{int(time.time())}"
        dst = dst.with_stem(stem)
    shutil.move(str(src), str(dst))
    return dst

def scan(src_dir):
    """Scan a directory and classify all .md files."""
    for f in list(src_dir.glob("*.md")):
        time.sleep(0.3)
        try:
            content = f.read_text(encoding="utf-8-sig", errors="replace")
            folder = classify(content, f.stem)
            dst_dir = (VAULT / folder) if folder else INBOX
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst = safe_move(f, dst_dir / f.name)
            loc = str(dst.relative_to(VAULT))
            log.info("Moved: %s -> %s", f.name, loc)
        except Exception as e:
            log.error("Failed: %s -> %s", f.name, e)

if __name__ == "__main__":
    log.info("=" * 50)
    log.info("Polling agent started (PID %d)", __import__("os").getpid())
    log.info("POLL_SECS=%d, FOLDERS=%d", POLL_SECS, len(FOLDERS))
    log.info("=" * 50)
    while True:
        try:
            scan(DOWNLOADS)
            scan(INBOX)
        except Exception as e:
            log.error("Scan error: %s", e)
        time.sleep(POLL_SECS)
