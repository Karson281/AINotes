---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# Agent-Zo Computer 評價 - 豆包

**Date:** 2026-06-07 03:24
**Source:** 豆包

---

Agent: Zo Computer 評價
内容由豆包 AI 生成，请仔细甄别
Zo Computer Free｜Hermes Agent 測試版完整部署規劃（專為免費版資源裁剪，避休眠、防OOM爆記憶）
 
前置重點（Zo Free硬性規限）
 
- 免費機：記憶體約1GB上限、閒置自動休眠、不能綁自訂域名、僅可用官方 .zo.space 二級域名、Docker可用但資源受限
 
- ✅ 方案：不用本機Ollama跑本地大模型（裝模型會爆盤+超內存休眠），全程接入第三方LLM API（OpenRouter/Kimi），最契合Zo免費資源
 
- 分工：Zo=Hermes測試、後續正式版遷去Hostinger VPS跑本地Ollama+全功能Gateway
 
一、開啟Zo終端環境
 
登入 zo.computer → 新建Linux實例（Free套餐預設Ubuntu）
 
打開網頁版Terminal（內置Docker已預裝，不用手動安裝docker）
 
先檢查環境
 
bash
  
docker --version
git --version
 
 
出現版本即正常，Zo Free自帶依賴環境
 
二、一鍵安裝Hermes（官方原生CLI安裝，優於Docker大包部署，省空間）
 
bash
  
# Hermes官方一鍵安裝腳本（自動裝Python3.11/uv/ffmpeg/Node，無需sudo）
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/install.sh | bash
# 載入環境變數
source ~/.bashrc
# 驗證安裝
hermes --version
 
 
安裝佔碟約700MB，遠低於Docker鏡像2GB，適合Zo免費存儲
 
三、Hermes初始化配置（關鍵：免資源超載設定）
 
1. 啟動配置嚮導
 
bash
  
hermes setup
 
 
一步步選項參數（照抄即可）：
 
LLM Provider：選OpenRouter（最平、多免費額度模型，不用本地載模型）
 
填入你的 OpenRouter API Key （提前去openrouter.ai申請免費key）
 
模型挑選： qwen-turbo / gpt-3.5-turbo-instruct （輕量，耗資源極低）
 
Terminal後端：Local（不要選Docker沙盒！）
 
選Docker沙盒會額外佔內存，Zo 1GB RAM撐不住，測試用Local終端足夠
 
Gateway通道：先Skip（後續再裝Telegram機器人，避免後台常駐耗資源）
 
設定Agent名稱： Zo-Hermes-Test 
 
2. 優化配置防休眠&OOM（手動改配置檔）
 
bash
  
nano ~/.hermes/config.yaml
 
 
替換關鍵配置（關閉瀏覽器自動化，最吃內存功能直接停用）：
 
yaml
  
browser:
  enable: false  # 關閉Playwright瀏覽，省500M+內存
terminal:
  backend: local
  timeout: 90
logs:
  persist: false # 關閉日誌存檔，減硬碟佔用
 
 
儲存退出：Ctrl+O → Enter → Ctrl+X
 
四、測試對話（CLI互動測試）
 
bash
  
hermes
 
 
輸入指令測試：
 
- 幫我建立一個test.txt檔案，寫入Hermes部署在Zo Free
 
- 查詢系統剩餘儲存空間
 
正常回覆即部署成功。
 
五、可選：後續加Telegram機器人（閒置才開，不用常駐）
 
想Telegram遠端操控Hermes再執行，不用就關閉gateway避免休眠
 
bash
  
hermes gateway install
 
 
去Telegram @BotFather 新建Bot，拿Bot Token
 
粘貼Token，綁定
 
啟動： hermes gateway run 
 
用完即關： Ctrl+C ，長掛會觸發Zo閒置休眠
 
六、Zo免費版使用守則（避免被凍結/休眠）
 
❌ 禁止：Ollama pull任何模型（7B模型>3GB，直接爆存儲）
 
✅ 只靠API調用LLM（OpenRouter/Kimi免額度）
 
不用時關閉gateway，只保留hermes配置檔
 
每3天登入一次Zo，防止實例閒置回收
 
定期清理緩存： rm -rf ~/.hermes/cache/* 
 
七、後續遷移Hostinger方案
 
Zo測試配置完後，複製 ~/.hermes 整個資料夾打包，丟去Hostinger VPS，直接：
 
Hostinger安裝同樣Hermes
 
替換配置檔，切換Terminal後端=Docker沙盒、開啟瀏覽功能、常駐Telegram Bot
 
需要我幫你整理OpenRouter免費註冊拿API Key的步驟嗎？
OpenRouter 免費申請API Key簡易步驟（搭配Zo Hermes專用，免綁卡、有免費額）
1. 註冊帳號
開官網：openrouter.ai
Sign up，用Email註冊/Github一鍵登入，免信用卡
2. 領免費額度
新用戶自動贈送免費試用額（可跑Qwen-Turbo、Gemini Flash等輕量模型，剛好匹配Zo免費Hermes）
左側→Billing，查看剩餘免費餘額，用完後可儲值，測試階段只用免費額就夠
3. 複製API Key
左邊選：API Keys
Create API Key → 備註：Zo-Hermes-Test → 建立
複製生成的Key（只出現一次，存好）
4. 貼入Zo Hermes配置兩種方式
方式1：setup互動配置
bash
运行
hermes setup

Provider選openrouter，貼剛才API Key，模型選：qwen-turbo / google/gemini-flash-1.5
方式2：手動改config.yaml
bash
运行
nano ~/.hermes/config.yaml

填入：
yaml
llm:
  provider: openrouter
  api_key: "你的OpenRouter_Key"
  model: qwen-turbo

存檔後重啟hermes即可。
✅ 免費優選模型（Zo專用，便宜省額）
qwen-turbo｜中文優、便宜、消耗低
google/gemini-flash-1.5｜長文解析、免費額消耗少
minimax-01｜對話順暢
❌ 避坑
不要選GPT4、Claude Opus等高價模型，免費額消耗極快。
補充小指令
配置完測試：
bash
运行
hermes
# 測試指令：幫我查看主機剩餘硬碟空間

需要我給一段一鍵替換配置的成品yaml，直接覆蓋使用？
Zo Free 入面嘅 Hermes Agent 實用場景（唔跑本地模型、靠API LLM，唔爆RAM、唔易休眠）
 
一、日常電腦自動化（最實用）
 
遠端指令管理Zo雲機
Telegram發訊息，Hermes自動執行伺服器指令：
 
- 查剩餘硬碟/記憶體： 幫我睇而家剩餘RAM同儲存 
 
- 建立/刪除檔案、整理資料夾、打包備份程式碼
 
- 定時刪除臨時檔，避免Zo儲存爆滿
 
自動備份筆記、程式碼
寫一段備份規則：每日自動打包筆記資料夾、存去Zo雲盤。
 
二、資訊搜集、文檔處理
 
網頁資訊摘要（已關閉重型瀏覽，改用輕量爬取）
輸入網址→Hermes抓取內容、濃縮重點、生成筆記存成txt。
 
例如：總結某篇AI技術文章，自動存檔。
 
本地文件解析
上傳文字/TXT→Agent分類、整理條列式筆記、翻譯內容。
 
三、作為 Hostinger VPS 測試中轉站
 
1. Hermes 腳本、提示詞先行測試
 
- 所有Agent指令、自動化邏輯先在Zo測試無bug，再搬去Hostinger正式機（KVM4）使用本地Qwen-VL
 
- 免費機試錯，唔使浪費VPS資源亂裝亂改
 
2. 遠端監控Hostinger伺服器（小用途）
 
透過SSH指令讓Hermes遠程查Hostinger狀態：CPU、Ollama是否在線、網站是否掛掉。
 
四、個人小助理（Telegram遙控）
 
綁TG Bot之後手機隨時用：
 
手機發指令生成待辦清單，自動存於Zo；
 
翻譯短句、生成簡單shell腳本、寫docker小配置；
 
簡單算數、規劃文字內容。
 
五、學習用途（練Hermes Agent用法）
 
- 練習Agent工具調用、自訂function、提示詞優化；
 
- 摸熟配置後，先在Zo磨合，再完整部署Hostinger本地Ollama+Qwen-VL。
 
❌ Zo Free 做唔到嘅
 
本地跑Qwen-VL/2B/7B多模態（內存同硬碟唔夠）
 
7×24小時長掛服務（閒置休眠機制）
 
批量圖片OCR、大型文檔解析（耗資源過大）
 
簡單總結
 
Zo=Hermes練手+輕量自動化+遠端小助理+正式VPS前置測試機；Hostinger=正式本地AI（Qwen-VL）+全功能Agent+網站伺服器。
Zo Free｜Hermes Agent 落地使用手冊（純 API 調用 LLM｜免本地模型、防 OOM、減休眠）
核心定位
Zo：測試 + 輕量化自動化中轉站｜Hostinger：正式常駐 + 本地 Ollama 大模型執行全程依賴 OpenRouter API，唔佔 RAM 跑權重，完美契合 Free 版 1GB 記憶體 + 閒置休眠規則。
一、五大實用落地場景（附 TG 實際指令範本）
1. Telegram 遠端雲機管理（日常最常用）
綁 TG Bot 後手機發文字即執行 Shell，唔使入網頁開 Terminal
查硬碟 / RAM：查詢Zo剩餘儲存同記憶體用量
檔案操作：在notes資料夾新建todo.txt，寫入今日待辦清單
自動清理緩存：刪除.hermes全部緩存檔案，釋放空間
備份打包：打包/code目錄，壓縮成backup_當前日.zip存放雲盤
小技巧：用完即刻關閉 gateway（Ctrl+C），避免閒置空轉觸發休眠。
2. 文檔 / 網路資訊自動處理
已關閉 Playwright 重型瀏覽，採用輕量 http 爬取，資源消耗極低
網頁摘要：幫我總結呢個網址內容https://xxx.com，結果存成article.txt
本機檔處理：上傳 TXT/PDF → 分類整理呢份文件，條列式重點翻譯成繁體存檔
筆記歸檔：零散備註自動歸入對應分類資料夾。
3. Hostinger VPS 遠端測試監控（中轉核心價值）
Hermes 透過 SSH 遠連 Hostinger，做低成本預檢：
遠端連Hostinger，查詢CPU負載同Ollama運行狀態
測試一段自動化腳本，無bug就匯出腳本檔，之後上傳Hostinger部署
優勢：所有腳本、Agent 邏輯 Zo 免費試錯，唔使浪費 VPS 時長同資源。
4. 隨身 AI 小助理（手機即開即用）
TG 一發指令即刻輸出，依託 OpenRouter 免費額模型 (qwen-turbo/gemini-flash)
文案 / 翻譯：幫我翻譯一段英文技術文件、撰寫簡單Docker Compose配置
規劃清單：生成一週學習清單，儲存落Zo雲碟
Shell 輔助：寫一個自動備份的bash小腳本
5. Hermes 技術學習實驗場
測試 Function Call、自訂 Agent 工具、Prompt 優化，反覆調參
確認業務邏輯可行後，打包~/.hermes配置資料夾，遷移 Hostinger
Hostinger 開啟 Docker 沙盒、本地 Ollama、瀏覽爬蟲全功能正式上線
二、Free 版絕對禁止項目（避凍結、爆盤、頻繁休眠）
❌ 唔安裝 Ollama、唔 pull 任何參數模型 (1.8B/7B)，硬碟同 RAM 承載唔到❌ 唔長掛 gateway/nohup 後台駐留，閒置空閒程序容易觸發休眠❌ 唔做批量 OCR、海量文件一次性解析，突發高負載 OOM 宕機
三、日常保養小指令（維持機器穩定）
bash
运行
# 清理緩存釋放空間
rm -rf ~/.hermes/cache/*
# 手動喚醒休眠機
wake

四、兩機分工總結
Zo Free：Hermes 原型測試、TG 輕量自動化、文檔整理、VPS 前置驗證、個人備份存檔
Hostinger VPS：7×24 常駐、本地 Ollama (Qwen-VL 等)、全功能 Hermes、自綁域名網站、商業級自動化
需要我整理一套專屬 TG 常用快捷指令清單，直接複製落 Hermes 使用？
快速
编程
超能模式
Beta
PPT 生成
AI 表格
图像生成
更多
