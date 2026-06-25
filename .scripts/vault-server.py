#!/usr/bin/env python3
"""
Obsidian Vault HTTP Server
接收 browser bookmarklet 嘅 POST 請求 → 自動寫入 vault

用法：
  python vault-server.py start     (啟動 server，背景執行)
  python vault-server.py stop      (停止 server)
  python vault-server.py status    (睇狀態)

Server 只 bind 127.0.0.1，唔會暴露俾外界。
"""

import sys, os, json, signal, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path
import re
import subprocess

VAULT = Path("C:/Users/kaisu/OneDrive/AINotes")
PORT = 18765
PID_FILE = VAULT / ".scripts" / ".server.pid"

# 簡單 token，防止其他 local process 亂寫
TOKEN = "kn-save-token-2026"

class SaveHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/save":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                body = json.loads(raw.decode("utf-8", errors="replace"))
            except Exception as e:
                import sys as _sys
                print("JSON ERROR:", repr(e), file=_sys.stderr)
                self._json(400, {"error": "invalid json", "detail": repr(e)})
                return

            # Token check
            if body.get("token") != TOKEN:
                self._json(403, {"error": "bad token"})
                return

            source = body.get("source", "Unknown")
            title = body.get("title", "untitled")
            content = body.get("content", "")
            tags = body.get("tags", [])

            if not content.strip():
                self._json(400, {"error": "empty content"})
                return

            # Build note
            today = datetime.now()
            tag_yaml = "\n".join(f"  - {t}" for t in tags) if tags else "  - topic/untagged"
            slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
            slug = re.sub(r'[-\s]+', '-', slug)[:40]

            note = f"""---
creation_date: {today.strftime('%Y-%m-%d')}
source: "{source}"
tags:
{tag_yaml}
status: inbox
---

# {title}

**Date:** {today.strftime('%Y-%m-%d %H:%M')}
**Source:** {source}

---

{content}
"""

            filename = f"{today.strftime('%Y-%m-%d')}-{slug}.md"
            filepath = VAULT / "1-AI-Conversations" / filename

            # Write file
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(note, encoding="utf-8")

            self._json(200, {
                "status": "ok",
                "path": str(filepath.relative_to(VAULT)),
                "tags": tags,
            })
            print(f"[SAVED] {filename} ({len(tags)} tags)")
        else:
            self._json(404, {"error": "not found"})

    def do_GET(self):
        if self.path == "/api/status":
            self._json(200, {"status": "running", "vault": str(VAULT)})
        else:
            self._json(404, {"error": "not found"})

    def _json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, fmt, *args):
        pass  # silent


def find_process():
    """搵返已經跑緊嘅 server process"""
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)  # signal 0 = just check existence
            return pid
        except (ValueError, ProcessLookupError, PermissionError):
            PID_FILE.unlink(missing_ok=True)
    return None


def cmd_start():
    pid = find_process()
    if pid:
        print(f"Server already running (PID {pid})")
        return

    # Fork to background (Windows compatible)
    if sys.platform == "win32":
        # Use START /B on Windows
        script = Path(__file__).resolve()
        subprocess.Popen(
            [sys.executable, str(script), "_serve"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        print(f"Server started on http://127.0.0.1:{PORT}")
    else:
        pid = os.fork()
        if pid > 0:
            print(f"Server started (PID {pid}) on http://127.0.0.1:{PORT}")
            PID_FILE.write_text(str(pid))
        else:
            _serve()

    cmd_status()


def cmd_stop():
    pid = find_process()
    if pid:
        os.kill(pid, signal.SIGTERM)
        PID_FILE.unlink(missing_ok=True)
        print("Server stopped")
    else:
        print("Server not running")


def cmd_status():
    pid = find_process()
    if pid:
        print(f"Server is RUNNING (PID {pid})")
        print(f"  http://127.0.0.1:{PORT}")
        print(f"  Vault: {VAULT}")
    else:
        print("Server is STOPPED")


def _serve():
    """Actually run the server"""
    server = HTTPServer(("127.0.0.1", PORT), SaveHandler)
    server.serve_forever()


if __name__ == "__main__":
    # Write PID when running as background
    if len(sys.argv) > 1 and sys.argv[1] == "_serve":
        pid = os.getpid()
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(pid))
        _serve()

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "start":
        cmd_start()
    elif cmd == "stop":
        cmd_stop()
    elif cmd == "status":
        cmd_status()
    else:
        print(f"Usage: {sys.argv[0]} {{start|stop|status}}")
