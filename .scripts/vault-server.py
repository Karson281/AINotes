#!/usr/bin/env python3
"""Vault Server — Windows 版，自動分類 + git push"""
import sys, json, subprocess, re
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

VAULT = Path("D:/kaisu/Google Drive/AINotes")
PORT = 18765
TOKEN = "kn-save-token-2026"
DEFAULT = "1-AI-Conversations"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/save": self._json(404); return
        try: b = json.loads(self.rfile.read(int(self.headers["Content-Length"])).decode())
        except: self._json(400,{"error":"invalid json"}); return
        if b.get("token") != TOKEN: self._json(403,{"error":"bad token"}); return
        t = b.get("title","") or ""; c = b.get("content","") or ""
        if not c.strip(): self._json(400,{"error":"empty content"}); return
        p = t.split("-",1)[0].strip() if "-" in t else ""
        D = {d.name for d in VAULT.iterdir() if d.is_dir() and not d.name.startswith(".")}
        f = DEFAULT
        for d in D:
            if d == p: f = d; break
        s = t.strip()[:60].replace("/","-").replace("\\","-").replace(":","-")
        if not s: s = "note"
        fp = VAULT / f / f"{s}.md"
        fp.parent.mkdir(parents=True, exist_ok=True)
        tg = "\n".join(f"  - {x}" for x in b.get("tags",[])) or "  - topic/untagged"
        fp.write_text(f"---\ncreation_date: {datetime.now():%Y-%m-%d}\nsource: \"{b.get('source','?')}\"\ntags:\n{tg}\nstatus: inbox\n---\n\n# {t}\n\n**Date:** {datetime.now():%Y-%m-%d %H:%M}\n\n---\n\n{c}\n", encoding="utf-8")
        try:
            subprocess.run(["git","-C",str(VAULT),"add","."],capture_output=True,timeout=30)
            subprocess.run(["git","-C",str(VAULT),"commit","-m",f"vault:{s}.md"],capture_output=True,timeout=30)
            subprocess.run(["git","-C",str(VAULT),"push"],capture_output=True,timeout=60)
        except: pass
        self._json(200,{"status":"ok","path":f"{f}/{s}.md"})
    def do_GET(self):
        self._json(200,{"status":"running"} if self.path=="/api/status" else {"error":"not found"},404)
    def _json(self,c,d=None,s=200):
        self.send_response(s if s else c); self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
        self.wfile.write(json.dumps(d or {}).encode())
    def log_message(self,*a): pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
