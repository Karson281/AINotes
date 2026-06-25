---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# Apps-DeepSeek debugger-AI 繁體/英文語言強制規則設定 - 豆包

**Date:** 2026-06-07 03:26
**Source:** 豆包

---

Apps: DeepSeek debugger-AI 繁體/英文語言強制規則設定
内容由豆包 AI 生成，请仔细甄别
完整操作清單（放工直接跟住做就得）
 
一、先準備兩個 GitHub 資料（一次搞掂）
 
1. 建立 Gist（用來永久存筆記）
 
登錄 GitHub → 點右上角 + → New gist
 
Filename 一定要寫： notes.json 
 
內容直接貼入：
 
json
  
{"通用": [], "Python": [], "Shell": [], "前端": []}
 
 
點 Create public gist
 
從網址提取 GIST_ID
範例網址：
 https://gist.github.com/xxx/  abc123def456 
 abc123def456  呢串就係 GIST_ID
 
2. 申請 GitHub Token（只開 Gist 權限，最安全）
 
GitHub 進入：Settings → Developer settings → Personal access tokens → Tokens (classic)
 
Generate new token (classic)
 
備註隨便寫，Expiration 選 No expiration（永久有效）
 
Scope 只勾選：gist（淨係勾呢一個就得）
 
生成後 馬上複製 Token，只會顯示一次
 
二、Vercel 環境變量 3 個（必須填）
 
進入你 Vercel 專案 → Settings → Environment Variables，新增 3 項：
 
 DEEPSEEK_API_KEY  = 你原本嘅 DeepSeek 密鑰
 
 GIST_ID  = 剛才 Gist 嘅 ID
 
 GITHUB_TOKEN  = 剛才生成嘅 GitHub Token
 
三、3 個部署文件內容（直接複製）
 
1. requirements.txt
 
txt
  
gradio
openai
requests
python-dotenv
 
 
2. vercel.json
 
json
  
{
  "build": {
    "env": {
      "PYTHON_VERSION": "3.11"
    }
  },
  "rewrites": [
    { "source": "/(.*)", "destination": "/api/index" }
  ]
}
 
 
3. api/index.py（最終穩固完整版）
 
python
  
import os
import json
import requests
import gradio as gr
from openai import OpenAI

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GIST_ID = os.getenv("GIST_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
你是 DeepSeek‑Coder 專業程式助手。
專長 Python、Shell、網頁、後端、腳本、Debug、代碼優化、邏輯解釋。
回答簡潔專業，程式碼使用 Markdown 區塊呈現。
"""

GIST_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def load_notes_from_gist():
    try:
        res = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=GIST_HEADERS)
        data = res.json()
        content = data["files"]["notes.json"]["content"]
        return json.loads(content)
    except:
        return {"通用": [], "Python": [], "Shell": [], "前端": []}

def save_notes_to_gist(notes_data):
    payload = {
        "files": {
            "notes.json": {"content": json.dumps(notes_data, ensure_ascii=False, indent=2)}
        }
    }
    requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=GIST_HEADERS, json=payload)

def chat_response(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for u, a in history[-6:]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": message})
    try:
        resp = client.chat.completions.create(
            model="deepseek-coder",
            messages=messages,
            timeout=8
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"請求超時或出錯：{str(e)}"

notes_data = load_notes_from_gist()

def get_categories():
    return list(notes_data.keys())

def load_notes(category):
    return "\n\n---\n\n".join(notes_data.get(category, []))

def save_note(category, note_content):
    if not note_content.strip():
        return "內容不能空白"
    if category not in notes_data:
        notes_data[category] = []
    notes_data[category].append(note_content.strip())
    save_notes_to_gist(notes_data)
    return f"✅ 已永久儲存到【{category}】"

CSS = """
:root {
    --bg-0: #0b0b10;
    --bg-1: #16161f;
    --bg-2: #20202c;
    --text: #e5e7eb;
    --primary: #6366f1;
    --primary-light: #818cf8;
    --border: #2d2d3a;
}
body, .gradio-container {background: var(--bg-0) !important;color: var(--text) !important;}
.gradio-chatbot {background: var(--bg-1) !important;border:1px solid var(--border) !important;border-radius:14px !important;}
.gradio-chatbot .user {background: var(--primary) !important;border-radius:12px 12px 4px 12px !important;}
.gradio-chatbot .bot {background: var(--bg-2) !important;border-radius:12px 12px 12px 4px !important;}
textarea, input, select {background: var(--bg-2) !important;border:1px solid var(--border) !important;color:#fff !important;border-radius:10px !important;}
button {background: var(--primary) !important;color:white !important;border-radius:10px !important;}
h1, h2, h3 {color: var(--primary-light) !important;text-align:center;}
"""

demo = gr.Blocks(title="DeepSeek‑Coder 穩固版", css=CSS)
with demo:
    gr.Markdown("# 🧑‍💻 DeepSeek‑Coder 專業代碼助手（穩固版）")
    gr.Markdown("### 防超時 · 防記憶體爆 · 筆記永久 Gist 存儲")

    with gr.Tabs():
        with gr.TabItem("💬 AI 對話"):
            chatbot = gr.Chatbot(height=520, bubble_full_width=False)
            msg = gr.Textbox(placeholder="輸入問題 / 貼上代碼片段...", label="訊息", lines=2)
            clear_btn = gr.Button("清空對話", variant="secondary")
            msg.submit(chat_response, [msg, chatbot], [msg, chatbot])
            clear_btn.click(lambda: None, None, chatbot, queue=False)

        with gr.TabItem("📒 筆記簿分類"):
            cats = get_categories()
            cat_drop = gr.Dropdown(choices=cats, label="選擇分類", value=cats[0])
            note_view = gr.Textbox(label="筆記內容", lines=18, interactive=False)
            note_input = gr.Textbox(label="新增筆記/代碼片段", lines=4)
            save_btn = gr.Button("儲存到分類")
            status = gr.Textbox(label="狀態", interactive=False)

            cat_drop.change(load_notes, inputs=cat_drop, outputs=note_view)
            save_btn.click(save_note, inputs=[cat_drop, note_input], outputs=status)

app = demo.app
 
 
四、最終部署步驟
 
GitHub 新建倉庫，上傳上面 3 個文件
 
Vercel 導入倉庫
 
填入 3 個環境變量
 
Deploy 一次完成
 
放工直接跟住做就得，有任何卡住隨時叫我。
補齊一鍵存對話筆記完整版（最終定稿，替換index.py即可，其餘配置不變）
python
运行
import os
import json
import requests
import gradio as gr
from openai import OpenAI

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GIST_ID = os.getenv("GIST_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
你是 DeepSeek‑Coder 專業程式助手。
專長 Python、Shell、網頁、後端、腳本、Debug、代碼優化、邏輯解釋。
回答簡潔專業，程式碼使用 Markdown 區塊呈現。
"""

GIST_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# 從Gist載入筆記
def load_notes_from_gist():
    try:
        res = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=GIST_HEADERS, timeout=8)
        data = res.json()
        content = data["files"]["notes.json"]["content"]
        return json.loads(content)
    except:
        return {"通用": [], "Python": [], "Shell": [], "前端": []}

# 筆記存回Gist
def save_notes_to_gist(notes_data):
    payload = {
        "files": {
            "notes.json": {"content": json.dumps(notes_data, ensure_ascii=False, indent=2)}
        }
    }
    requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=GIST_HEADERS, json=payload, timeout=8)

# AI回覆：限6輪歷史、8秒超時防504/OOM
def chat_response(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for u, a in history[-6:]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": message})
    try:
        resp = client.chat.completions.create(
            model="deepseek-coder",
            messages=messages,
            timeout=8
        )
        ans = resp.choices[0].message.content
        history.append((message, ans))
        return "", history
    except Exception as e:
        err = f"請求超時或出錯：{str(e)}"
        history.append((message, err))
        return "", history

notes_data = load_notes_from_gist()

def get_categories():
    return list(notes_data.keys())

def load_notes(category):
    return "\n\n---\n\n".join(notes_data.get(category, []))

def save_note(category, note_content):
    if not note_content.strip():
        return "內容不能空白"
    if category not in notes_data:
        notes_data[category] = []
    notes_data[category].append(note_content.strip())
    save_notes_to_gist(notes_data)
    return f"✅ 已永久儲存到【{category}】"

# 一鍵儲存最後AI回覆
def save_last_chat(history, sel_cat):
    if not history:
        retu
