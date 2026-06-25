#!/usr/bin/env python3
"""
Watch Downloads + inbox for .md files, auto-classify into vault folders.
Reads H1 title prefix to determine target folder.
用法：python3 watch-downloads.py
用 Ctrl+C 停止。
"""
import os, time, shutil, re
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
VAULT = Path("C:/Users/kaisu/OneDrive/AINotes")
INBOX = VAULT / "0-Inbox"
POLL_SECS = 3

FOLDERS = [
    "模型", "NAS", "建站", "文件", "Plugin", "提示詞", "Agent",
    "知識庫", "投資", "系統", "VPS", "保險", "Proma", "Apps",
    "編程", "旅行", "ESTA", "自駕遊", "自動化", "醫療", "試題", "通訊", "消費",
]

def detect_folder(content, stem):
    """Read H1 title prefix -> folder name. Fallback to filename prefix."""
    m = re.search(r'^#\s+(.+?)(?:[：:\-_\s]|$)', content, re.MULTILINE)
    prefix = m.group(1).strip() if m else stem
    for folder in FOLDERS:
        if prefix.startswith(folder):
            return folder
    _clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', stem)
    for folder in FOLDERS:
        if stem.startswith(folder) or _clean.startswith(folder):
            return folder
    return None

def process_file(f):
    content = f.read_text(encoding="utf-8", errors="replace")
    folder = detect_folder(content, f.stem)
    target_dir = (VAULT / folder) if folder else INBOX
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f.name
    shutil.move(str(f), str(target))
    rel = str(target.relative_to(VAULT))
    print(f"Moved: {f.name} -> {rel}")

# Pre-seed
seen = set()
for d in [DOWNLOADS, INBOX]:
    for f in d.glob("*.md"):
        seen.add(f.name)

print("Watcher started (auto-classify mode)")
print(f"  Downloads -> {DOWNLOADS}")
print(f"  Watching -> inbox, downloads")
print(f"  Folders: {len(FOLDERS)}")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        for src_dir in [DOWNLOADS, INBOX]:
            for f in list(src_dir.glob("*.md")):
                if f.name in seen:
                    continue
                seen.add(f.name)
                time.sleep(1)
                try:
                    s1 = f.stat().st_size
                    time.sleep(0.5)
                    if f.stat().st_size != s1:
                        continue
                    process_file(f)
                except Exception as e:
                    print(f"Error: {f.name} -> {e}")
        time.sleep(POLL_SECS)
except KeyboardInterrupt:
    print("\nStopped.")
