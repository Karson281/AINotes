---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# Apps-主/子筆記簿Agent程式 - 豆包

**Date:** 2026-06-07 03:26
**Source:** 豆包

---

Apps: 主/子筆記簿Agent程式
内容由豆包 AI 生成，请仔细甄别
我直接幫你升級到 主筆記簿 + 子筆記簿
每個子筆記簿獨立：模型選擇、Agent人物設定、系統提示詞、對話歷史
結構係：
 主筆記簿(例如：炒股) → 子筆記簿(短線/長線/新聞分析) 
完全分開，唔混亂，直接複製覆蓋舊程式即可。
 
最終完整版程式碼（主/子筆記簿 + 獨立Agent+模型+角色+畫圖+負向提示詞）
 
python
  
import streamlit as st
import requests
from together import Together

st.set_page_config(page_title="Together AI｜主/子筆記簿 Agent", page_icon="🤖", layout="wide")

# 結構：主筆記簿 → 子筆記簿（每個子簿獨立設定）
if "book_data" not in st.session_state:
    st.session_state.book_data = {
        "預設主簿": {
            "sub_books": {
                "預設子簿": {
                    "history": [],
                    "system_prompt": "你係友善專業嘅AI助手，用淺白中文回答。",
                    "model_key": "Deepseek‑V4‑Pro（最強中文）"
                }
            }
        }
    }
if "main_book" not in st.session_state:
    st.session_state.main_book = "預設主簿"
if "sub_book" not in st.session_state:
    st.session_state.sub_book = "預設子簿"

# API
API_KEY = st.text_input("🔑 輸入 Together API Key", type="password")
if not API_KEY:
    st.warning("請輸入 API Key")
    st.stop()
client = Together(api_key=API_KEY)

# 文字模型
text_models = {
    "Deepseek‑V4‑Pro（最強中文）": "deepseek-ai/DeepSeek-V4-Pro",
    "Deepseek‑V4‑Flash（平價推理）": "deepseek-ai/DeepSeek-V4-Flash",
    "GLM‑5.1‑FP4（中文超強）": "zhipuai/GLM-5.1-FP4",
    "Qwen3‑Coder（爬蟲/寫代碼）": "Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8",
    "Qwen2.5‑7B‑Turbo（輕量快速）": "Qwen/Qwen2.5-7B-Instruct-Turbo"
}
img_model = "Qwen/Qwen-Image-2.0"
negative_prompt = "模糊，變形，醜陋，多餘手指，水印，文字，雜亂，低清"

# 左側面板：主簿 + 子簿 + Agent設定
with st.sidebar:
    st.title("📒 主/子筆記簿管理")

    # 新增主筆記簿
    new_main = st.text_input("新增主筆記簿")
    if st.button("➕ 新增主簿") and new_main.strip():
        if new_main not in st.session_state.book_data:
            st.session_state.book_data[new_main] = {
                "sub_books": {
                    "預設子簿": {
                        "history": [],
                        "system_prompt": "你係友善專業嘅AI助手，用淺白中文回答。",
                        "model_key": "Deepseek‑V4‑Pro（最強中文）"
                    }
                }
            }
            st.success(f"已新增主簿：{new_main}")

    # 選擇主筆記簿
    main_list = list(st.session_state.book_data.keys())
    st.session_state.main_book = st.radio("選擇主筆記簿", main_list)
    main_data = st.session_state.book_data[st.session_state.main_book]

    # 新增子筆記簿
    new_sub = st.text_input("新增子筆記簿")
    if st.button("➕ 新增子簿") and new_sub.strip():
        if new_sub not in main_data["sub_books"]:
            main_data["sub_books"][new_sub] = {
                "history": [],
                "system_prompt": "你係友善專業嘅AI助手，用淺白中文回答。",
                "model_key": "Deepseek‑V4‑Pro（最強中文）"
            }
            st.success(f"已新增子簿：{new_sub}")

    # 選擇子筆記簿
    sub_list = list(main_data["sub_books"].keys())
    st.session_state.sub_book = st.radio("選擇子筆記簿", sub_list)
    sub_data = main_data["sub_books"][st.session_state.sub_book]

    # 【重點】每個子簿獨立：模型 + 角色設定
    st.markdown("### 🤖 Agent 設定（本本子專用）")
    curr_model = sub_data["model_key"]
    agent_model = st.selectbox("選擇模型", list(text_models.keys()),
                              index=list(text_models.keys()).index(curr_model))
    sys_prompt = st.text_area("人物/系統提示詞", value=sub_data["system_prompt"], height=120)

    if st.button("✅ 儲存本簿設定"):
        sub_data["model_key"] = agent_model
        sub_data["system_prompt"] = sys_prompt
        st.success("設定已儲存！")

    if st.button("🗑️ 清空本子對話"):
        sub_data["history"] = []
        st.rerun()

# 模式選擇
mode = st.radio("模式", ["文字對話", "AI 畫圖"], horizontal=True)

# 讀取當前子簿數據
chat_history = sub_data["history"]
system_prompt = sub_data["system_prompt"]
model_id = text_models[sub_data["model_key"]]

# 顯示對話
for msg in chat_history:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"])
        else:
            st.markdown(msg["content"])

# 輸入框
user_input = st.chat_input("輸入指令 / 畫圖提示詞")
if user_input:
    chat_history.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if mode == "文字對話":
        messages = [{"role":"system","content":system_prompt}] + chat_history
        res = client.chat.completions.create(model=model_id, messages=messages)
        reply = res.choices[0].message.content
        chat_history.append({"role":"assistant","content":reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    else:
        st.info("🖼️ 生成圖片中...")
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type":"application/json"}
        payload = {
            "model": img_model,
            "prompt": user_input,
            "negative_prompt": negative_prompt,
            "n":1,"size":"1024x1024"
        }
        res = requests.post("https://api.together.xyz/v1/images/generations", headers=headers, json=payload)
        img_url = res.json()["data"][0]["url"]
        st.image(img_url)
        chat_history.append({"role":"assistant","content":img_url, "type":"image"})

    # 回寫保存
    main_data["sub_books"][st.session_state.sub_book]["history"] = chat_history
 
 
功能完全對應你要求
 
✅ 主筆記簿 + 子筆記簿 多層分類
例：
 
- 主簿：炒股
 
- 子簿：短線交易、長線價值、財經新聞分析、技術走勢
 
- 主簿：爬蟲
 
- 子簿：AASTOCKS、明報新聞、地產數據
 
✅ 每個子筆記簿完全獨立
 
- 獨立選擇模型
 
- 獨立Agent人物設定
 
- 獨立系統提示詞
 
- 獨立對話記憶
 
✅ 文字對話 + AI畫圖（Qwen‑Image‑2.0 中文最強）
 
✅ 內置負向提示詞
 
✅ 全部雲端運算，弱電腦完全無壓力
 
執行指令
 
cmd
  
cd /d D:\hk_scraper
streamlit run together_gui.py
 
 
示範Agent直接抄入子簿
 
炒股短線子簿
 
plaintext
  
你係港股短線交易分析師，專注技術分析、成交量、資金流向，簡潔用廣東話講重點，唔做投資保證。
 
 
爬蟲子簿
 
plaintext
  
你係專業Python爬蟲工程師，寫穩定代碼，廣東話註解，專門爬香港財經、新聞、股市數據。
 
 
需要我幫你再做一個 匯出全部筆記簿成檔案、匯入備份 功能嗎？
完整可用程式（補齊代碼縮排、語法錯誤，新增匯入匯出備份功能）
修改重點：
修正原文最後多餘空格語法報錯
新增全部筆記簿匯出 JSON 備份、匯入恢復功能
保留原有全部功能：主 / 子筆記簿分級、各子簿獨立模型 / 系統提示詞 / 對話記錄、文字對話 + AI 繪圖、負向提示詞
python
运行
import streamlit as st
import requests
import json
from together import Together

st.set_page_config(page_title="Together AI｜主/子筆記簿 Agent", page_icon="🤖", layout="wide")

# 結構：主筆記簿 → 子筆記簿（每個子簿獨立設定）
if "book_data" not in st.session_state:
    st.session_state.book_data = {
        "預設主簿": {
            "sub_books": {
                "預設子簿": {
                    "history": [],
                    "system_prompt": "你係友善專業嘅AI助手，用淺白中文回答。",
                    "model_key": "Deepseek‑V4‑Pro（最強中文）"
                }
            }
        }
    }
if "main_book" not in st.session_state:
    st.session_state.main_book = "預設主簿"
if "sub_book" not in st.session_state:
    st.session_state.sub_book = "預設子簿"

# API
API_KEY = st.text_input("🔑 輸入 Together API Key", type="password")
if not API_KEY:
    st.warning("請輸入 API Key")
    st.stop()
client = Together(api_key=API_KEY)

# 文字模型
text_models = {
    "Deepseek‑V4‑Pro（最強中文）": "deepseek-ai/DeepSeek-V4-Pro",
    "Deepseek‑V4‑Flash（平價推理）": "deepseek-ai/DeepSeek-V4-Flash",
    "GLM‑5.1‑FP4（中文超強）": "zhipuai/GLM-5.1-FP4",
    "Qwen3‑Coder（爬蟲/寫代碼）": "Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8",
    "Qwen2.5‑7B‑Turbo（輕量快速）": "Qwen/Qwen2.5-7B-Instruct-Turbo"
}
img_model = "Qwen/Qwen-Image-2.0"
negative_prompt = "模糊，變形，醜陋，多餘手指，水印，文字，雜亂，低清"

# 左側面板：主簿 + 子簿 + Agent設定 + 備份匯入匯出
with st.sidebar:
    st.title("📒 主/子筆記簿管理")

    # 新增主筆記簿
    new_main = st.text_input("新增主筆記簿")
    if st.button("➕ 新增主簿") and new_main.strip():
        if new_main not in st.session_state.book_data:
            st.session_state.book_data[new_main] = {
                "sub_books": {
                    "預設子簿": {
                        "history": [],
                        "system_prompt": "你係友善專業嘅AI助手，用淺白中文回答。",
                        "model_key": "Deepseek‑V4‑Pro（最強中文）"
                    }
                }
            }
            st.success(f"已新增主簿：{new_main}")

    # 選擇主筆記簿
    main_list = list(st.session_state.book_data.keys())
    st.session_state.main_book = st.radio("選擇主筆記簿", main_list)
    main_data = st.session_state.book_data[st.session_state.main_book]

    # 新增子筆記簿
    new_sub = st.text_input("新增子筆記簿")
    if st.button("➕ 新增子簿") and new_sub.strip():
        if new_sub not in main_data["sub_books"
