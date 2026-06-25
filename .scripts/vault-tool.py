#!/usr/bin/env python3
"""
Obsidian Vault Automation Tool
用法: python vault-tool.py <command> [options]

Commands:
  status             Show vault stats
  list [path]        List notes
  import <file>      Import conversation as formatted note
  tag <file>         Auto-suggest tags for a note
  connect <file>     Find related notes
  inbox              Process inbox (auto-categorize)
  weekly             Generate weekly summary
"""

import os, sys, json, urllib.request, urllib.error, ssl, re
from datetime import datetime, timedelta
from pathlib import Path

VAULT_PATH = Path("C:/Users/kaisu/OneDrive/AINotes")
API_PORT = 27124
API_KEY_FILE = VAULT_PATH / ".obsidian" / "plugins" / "obsidian-local-rest-api" / "data.json"

TAG_KEYWORDS = {
    "ai/perplexity":    ["perplexity", "pplx"],
    "ai/qianwen":       ["千問", "qwen", "通義"],
    "ai/doubao":        ["豆包", "doubao"],
    "ai/copilot":       ["copilot", "github"],
    "ai/manus":         ["manus"],
    "ai/gemini":        ["gemini", "bard"],
    "ai/proma-agent":   ["proma", "claude code"],
    "topic/python":     ["python", "django", "flask", "fastapi"],
    "topic/javascript": ["javascript", "typescript", "react", "vue", "node"],
    "topic/database":   ["sql", "nosql", "postgresql", "mysql", "mongodb", "redis"],
    "topic/devops":     ["docker", "kubernetes", "k8s", "ci/cd", "github action"],
    "topic/ai-ml":      ["machine learning", "deep learning", "llm", "transformer"],
    "topic/design":     ["ui", "ux", "design", "figma"],
    "topic/project-mgmt": ["agile", "scrum", "sprint", "milestone"],
    "topic/security":   ["security", "encrypt", "auth", "oauth", "jwt"],
    "topic/architecture": ["microservice", "monolith", "event-driven", "architecture"],
}

# ==============================================================
# Obsidian REST API
# ==============================================================
class ObsidianAPI:
    def __init__(self):
        self.api_key = self._load_api_key()
        self.base_url = f"https://localhost:{API_PORT}"
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def _load_api_key(self):
        try:
            return json.loads(API_KEY_FILE.read_text()).get("apiKey", "")
        except Exception as e:
            print(f"[WARN] Cannot read API Key: {e}")
            return ""

    def _request(self, method, path, data=None):
        url = f"{self.base_url}{path}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if data is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(data).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, context=self.ctx, timeout=10) as resp:
                return resp.read().decode()
        except urllib.error.HTTPError as e:
            print(f"[ERR] HTTP {e.code}: {e.reason}")
        except Exception as e:
            print(f"[ERR] API failed: {e}")
        return None

    def ping(self):
        return self._request("GET", "/")

# ==============================================================
# Filesystem access
# ==============================================================
class VaultFS:
    @staticmethod
    def list_md_files(subdir=None):
        base = VAULT_PATH / subdir if subdir else VAULT_PATH
        if not base.exists():
            return []
        files = sorted(base.rglob("*.md"))
        return [f for f in files if ".obsidian" not in str(f)]

    @staticmethod
    def read(rel_path):
        f = VAULT_PATH / rel_path
        return f.read_text(encoding="utf-8") if f.exists() else None

    @staticmethod
    def write(rel_path, content):
        f = VAULT_PATH / rel_path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
        return f

    @staticmethod
    def move(src_rel, dst_rel):
        src = VAULT_PATH / src_rel
        dst = VAULT_PATH / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        return dst

# ==============================================================
# Core automation
# ==============================================================
class VaultAutomation:
    def __init__(self):
        self.api = ObsidianAPI()
        self.fs = VaultFS()

    # ----- status -----
    def show_status(self):
        api_ok = self.api.ping() is not None
        files = self.fs.list_md_files()
        total = len(files)
        inbox = len([f for f in files if "0-Inbox" in str(f)])
        ai = len([f for f in files if "0-Inbox" not in str(f) and ".scripts" not in str(f)])
        pm = len([f for f in files if "2-Project-Management" in str(f)])
        kb = len([f for f in files if "3-Knowledge-Base" in str(f)])
        week_ago = datetime.now() - timedelta(days=7)
        recent = sum(1 for f in files if datetime.fromtimestamp(f.stat().st_mtime) > week_ago)

        print("=" * 50)
        print("  Obsidian Vault Status")
        print("=" * 50)
        print(f"  API:        {'OK' if api_ok else 'OFFLINE'}")
        print(f"  Total:      {total}")
        print(f"  Inbox:      {inbox}")
        print(f"  AI Convos:  {ai}")
        print(f"  Project:    {pm}")
        print(f"  Knowledge:  {kb}")
        print(f"  This week:  {recent}")
        print("=" * 50)

    # ----- list -----
    def list_notes(self, subdir=""):
        files = self.fs.list_md_files(subdir) if subdir else self.fs.list_md_files()
        files = [f for f in files if f.name != "README.md" and "Templates" not in str(f)]
        if not files:
            print("  (no notes yet)")
            return
        print(f"\nNotes ({len(files)}):")
        print("-" * 60)
        for f in files:
            rel = str(f.relative_to(VAULT_PATH))
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            print(f"  {mtime.strftime('%m-%d %H:%M')}  {rel}")
        print()

    # ----- import -----
    def import_conversation(self, file_path, platform="Proma-Agent"):
        content_path = Path(file_path)
        if not content_path.exists():
            print(f"[ERR] File not found: {file_path}")
            return

        text = content_path.read_text(encoding="utf-8")
        lines = text.strip().split("\n")
        title = lines[0][:50] if lines else "untitled"
        today = datetime.now()

        source = self._detect_platform(text) or platform
        tags = self._suggest_tags(text)
        tags_str = "\n".join(f"  - {t}" for t in tags)

        note = f"""---
creation_date: {today.strftime('%Y-%m-%d')}
source: "{source}"
tags:
{tags_str}
status: inbox
---

# {title}

**Date:** {today.strftime('%Y-%m-%d %H:%M')}
**Source:** {source}

---

## Content

{text}

---

## Key Points

-

## Related Notes

-

## Action Items

- [ ]
"""

        filename = f"{today.strftime('%Y-%m-%d')}-{self._slugify(title)}.md"
        rel_path = f"0-Inbox/{filename}"
        self.fs.write(rel_path, note)
        print(f"[OK] Imported: {rel_path}")
        print(f"Tags: {', '.join(tags)}")

    # ----- tag -----
    def _suggest_tags(self, text):
        text_lower = text.lower()
        tags = []
        for tag, keywords in TAG_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    tags.append(tag)
                    break
        return tags if tags else ["topic/untagged"]

    def _detect_platform(self, text):
        text_lower = text.lower()
        for platform, keywords in {
            "Perplexity": ["perplexity", "pplx"],
            "Copilot": ["copilot"],
            "Manus": ["manus"],
            "Gemini": ["gemini"],
            "Proma-Agent": ["proma agent", "claude code"],
        }.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    return platform
        if "千問" in text or "qwen" in text_lower:
            return "千問"
        if "豆包" in text:
            return "豆包"
        return None

    def auto_tag_note(self, rel_path):
        content = self.fs.read(rel_path)
        if not content:
            print(f"[ERR] Cannot read: {rel_path}")
            return
        tags = self._suggest_tags(content)
        tags_str = "\n".join(f"  - {t}" for t in tags)

        fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if fm_match:
            fm_text = fm_match.group(1)
            if "tags:" in fm_text:
                new_content = re.sub(r"tags:.*?(?=\n\w)", tags_str, content, flags=re.DOTALL)
            else:
                new_content = content.replace(fm_text, fm_text + "\n" + tags_str)
        else:
            new_content = f"---\ntags:\n{tags_str}\n---\n\n{content}"
        self.fs.write(rel_path, new_content)
        print(f"[OK] Tagged: {rel_path}")
        print(f"Tags: {', '.join(tags)}")

    # ----- connect -----
    def find_connections(self, rel_path):
        content = self.fs.read(rel_path)
        if not content:
            print(f"[ERR] Cannot read: {rel_path}")
            return
        keywords = set()
        for m in re.finditer(r'[一-鿿]{3,5}', content):
            keywords.add(m.group())
        for m in re.finditer(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content):
            if len(m.group()) > 3:
                keywords.add(m.group())

        all_files = self.fs.list_md_files()
        matches = []
        for f in all_files:
            f_rel = str(f.relative_to(VAULT_PATH))
            if f_rel == rel_path:
                continue
            try:
                fc = f.read_text(encoding="utf-8", errors="ignore")
            except:
                continue
            for kw in keywords:
                if kw in fc:
                    matches.append((kw, f_rel))
                    break

        if not matches:
            print("No related notes found")
            return
        print(f"\nRelated notes found ({len(matches)}):")
        print("-" * 60)
        for kw, f_rel in matches[:15]:
            note_name = Path(f_rel).stem
            print(f"  [[{note_name}]]  (match: {kw})")
        print()

    # ----- inbox -----
    def process_inbox(self):
        inbox_dir = VAULT_PATH / "0-Inbox"
        files = [f for f in inbox_dir.glob("*.md") if f.name != "README.md"]
        if not files:
            print("Inbox is empty")
            return
        print(f"\nProcessing inbox ({len(files)} files)...")
        print("-" * 60)
        for f in files:
            content = f.read_text(encoding="utf-8")
            tags = self._suggest_tags(content)
            platform = self._detect_platform(content)

            if platform:
                target_dir = VAULT_PATH / "0-Inbox"
            elif any(t.startswith("topic/") for t in tags):
                topic = [t for t in tags if t.startswith("topic/")][0]
                subdir = topic.replace("topic/", "")
                fd = ["模型","NAS","建站","文件","Plugin","提示詞","Agent","知識庫","投資","系統","VPS","保險","Proma","Apps","編程","旅行","ESTA","自駕遊","自動化","醫療","試題","通訊","消費"]
            target_dir = VAULT_PATH / "0-Inbox"
            for fname in fd:
                if fname in f.stem:
                    target_dir = VAULT_PATH / fname
                    break
            else:
                target_dir = VAULT_PATH / "0-Inbox"

            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / f.name
            f.rename(target)
            rel = str(target.relative_to(VAULT_PATH))
            print(f"  [OK] {f.name} -> {rel}")
            self.auto_tag_note(rel)
        print("[DONE] Inbox processed!")

    # ----- weekly summary -----
    def generate_weekly_summary(self):
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        files = self.fs.list_md_files()
        week_files = []
        for f in files:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if week_start <= mtime <= week_end and f.name != "README.md" and "Templates" not in str(f):
                week_files.append(f)
        if not week_files:
            print("No new notes this week")
            return

        by_cat = {}
        for f in week_files:
            rel = str(f.relative_to(VAULT_PATH))
            cat = rel.split("/")[0] if "/" in rel else "root"
            by_cat.setdefault(cat, []).append(rel)

        all_content = ""
        for f in week_files:
            try:
                all_content += f.read_text(encoding="utf-8", errors="ignore")
            except:
                pass

        topic_counts = {}
        for tag, keywords in TAG_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in all_content.lower():
                    topic_counts[tag] = topic_counts.get(tag, 0) + 1
                    break

        lines = []
        lines.append("---")
        lines.append(f"week: {today.strftime('%Y')}W{today.isocalendar()[1]}")
        lines.append("tags:")
        lines.append("  - weekly-review")
        lines.append("  - auto-generated")
        lines.append("---")
        lines.append("")
        lines.append(f"# Weekly Review - {week_start.strftime('%m/%d')} ~ {week_end.strftime('%m/%d')}")
        lines.append("")
        lines.append(f"Total **{len(week_files)}** notes this week\n")
        for cat, items in sorted(by_cat.items()):
            lines.append(f"### {cat}")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")
        if topic_counts:
            lines.append("### Hot Topics")
            for tag, count in sorted(topic_counts.items(), key=lambda x: -x[1])[:10]:
                lines.append(f"- {tag}: {count}")

        summary = "\n".join(lines)
        filename = f"W{today.isocalendar()[1]}-auto-review.md"
        rel_path = f"2-Project-Management/Weekly-Reviews/{filename}"
        self.fs.write(rel_path, summary)
        print(f"[OK] Weekly report generated: {rel_path}")
        print(f"Covers {len(week_files)} notes")

    @staticmethod
    def _slugify(text):
        text = re.sub(r'[^\w\s-]', '', text.strip().lower())
        return re.sub(r'[-\s]+', '-', text)[:40]

# ==============================================================
# CLI
# ==============================================================
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    auto = VaultAutomation()
    cmds = {
        "status": lambda: auto.show_status(),
        "list": lambda: auto.list_notes(sys.argv[2] if len(sys.argv) > 2 else ""),
        "import": lambda: auto.import_conversation(
            sys.argv[2] if len(sys.argv) > 2 else input("File path: "),
            sys.argv[3] if len(sys.argv) > 3 else "Proma-Agent"
        ),
        "tag": lambda: auto.auto_tag_note(sys.argv[2] if len(sys.argv) > 2 else input("Note path: ")),
        "connect": lambda: auto.find_connections(sys.argv[2] if len(sys.argv) > 2 else input("Note path: ")),
        "inbox": lambda: auto.process_inbox(),
    }
    fn = cmds.get(cmd)
    if fn:
        fn()
    else:
        print(f"[ERR] Unknown command: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
