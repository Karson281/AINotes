---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# VPS-Docker-本地私有化部署與雲端API分別及架構 - 豆包

**Date:** 2026-06-07 03:05
**Source:** 豆包

---

VPS:Docker-本地私有化部署與雲端API分別及架構
内容由豆包 AI 生成，请仔细甄别
唔係雲端API，係完全本地私有化部署（本地VPS跑模型）
 
1、簡單講解分別
 
✅ 你而家呢套docker環境：本地離線私有部署
 
Qwen2-VL-7B 模型下載存係你 Hostinger KVM4 嘅 NVMe 硬碟，
 
- Ollama 喺你部VPS入面直接載入權重、CPU本地推理
 
- OpenWebUI、Hermes Agent 淨係透過**本機內網API（11434）**同Ollama溝通
 
- 唔經過阿里雲/任何第三方雲API、唔使扣點數、唔使網絡連接阿里先用到AI
 
- 所有對話內容、圖片全部留喺你VPS，數據唔外洩
 
❌ 雲端API係另一回事（唔係你呢個方案）
 
雲端API＝調用阿里百煉/通義千問官網接口，發送文字/圖片去阿里伺服器運算、收結果，要計流量收費。
 
2、你架構數據流向
 
瀏覽器 → Nginx → OpenWebUI/Hermes → 本機Ollama(127.0.0.1:11434) → VPS本地Qwen-VL模型運算
全程唔出你部Hostinger伺服器
 
3、補充：想轉雲端API先要改設定
 
如果日後想用阿里雲Qwen API，先刪本地模型，改OLLAMA_BASE_URL指向阿里官方接口就得，而家預設係本地運行。
粵語簡潔整理｜本地私有化 VPS 部署 VS 雲端 API 分別
一、兩種方案核心區分
✅ 你而家：VPS 本地私有化部署（Docker+Ollama+Qwen2-VL-7B）
模型權重完整落喺 Hostinger KVM4 NVMe 硬碟，完全唔靠第三方雲伺服器
Ollama 本地載入模型，靠 VPS CPU 做離線推理；
OpenWebUI、Hermes Agent 只用本機回環地址 127.0.0.1:11434 內網通訊，唔出 VPS 機器；
唔接入阿里 / 任何廠商雲 API、唔使扣費、斷咗外網都可以正常用 AI；
所有聊天記錄、上傳圖片只存在你 VPS 硬碟，數據唔外流。
❌ 雲端 API 調用（阿里百煉 / 通義千問官網接口）
本地只負責傳輸內容，文字、圖片全部上傳去阿里遠程伺服器做運算；
按調用次數 / 流量計費、扣點收費；
依賴外網連接阿里服務，對話數據會經由阿里雲處理存儲。
二、你現有架構完整數據流向
瀏覽器 → Nginx 反向代理 → OpenWebUI/Hermes Agent → 本機 127.0.0.1:11434 (Ollama) → VPS 本地 Qwen2-VL 模型計算整條數據鏈全程封閉在單台 Hostinger VPS 內，數據唔流出伺服器
三、切換雲端 API 操作邏輯
而家預設本地推理，若之後想用阿里雲 Qwen 官方 API：
用 Ollama 指令刪除 VPS 本地緩存嘅 Qwen2-VL 模型；
修改環境變數OLLAMA_BASE_URL，由本機地址改成阿里雲官方 API 接口地址；
重啟對應服務即切換成雲端收費調用模式。
需要我幫你整理一份簡短操作備忘清單（切換雲端指令、還原本地部署步驟）嗎？
一定要裝 Docker，原因好簡單（針對你Ollama + Hermes + OpenWebUI + Nginx）
 
1、點解要用Docker？
 
唔會亂晒VPS系統
Ollama、WebUI、Hermes、Nginx各自隔離環境，唔會軟件版本衝突，刪除服務一隻指令搞掂，唔殘留垃圾檔案。
 
之前俾你嘅 docker-compose.yml 整套一鍵部署
唔使逐樣手動安裝依賴、配置環境變數， docker compose up -d  即開全套AI環境。
 
方便限制CPU同RAM
之前設定：Ollama鎖 2vCPU + 11GB RAM，自動控資源，唔會Qwen-VL亂搶內存搞掛網站。
 
2、Hostinger VPS（Ubuntu系統）一鍵安裝Docker指令
 
bash
  
# 更新套件
apt update && apt upgrade -y

# 安裝docker+docker-compose
apt install docker.io docker-compose-plugin -y

# 開機自啟動Docker
systemctl enable --now docker
 
 
安裝完輸入
 
bash
  
docker -v
docker compose version
 
 
有版本號=安裝成功，之後直接入之前 ai-stack 資料夾執行  docker compose up -d 
 
3、唔裝Docker得唔得？
 
都得，但缺點超多：
 
- 逐個手動安裝Ollama、Python環境、Hermes、OpenWebUI、Nginx
 
- 手動分內存、分CPU好麻煩
 
- 後續更新、卸載極易搞壞系統
跑你呢套AI堆，Docker係最省心首選
 
小總結
 
✅ 想沿用之前一鍵配置 → 必裝Docker
✅ 安裝就上面3行指令，2分鐘搞掂
粵語精簡總結｜點解跑 Ollama+OpenWebUI+Hermes+Nginx 一定要裝 Docker
一、裝 Docker 三大好處（對應你 Hostinger Ubuntu VPS）
環境隔離，唔整亂原生系統
Ollama、Agent、WebUI、Nginx 各自獨立容器，軟件版本唔衝突；刪服務淨係停容器就得，唔殘留依賴雜檔。
docker-compose 一鍵成套部署
唔使逐樣裝 Python、運行庫、配置環境變數，落去ai-stack目錄執行docker compose up -d直接起全鏈 AI 服務。
精準管控硬體資源
配置檔可以直接鎖定 Ollama：2vCPU+11GB 記憶體，防止 Qwen2-VL 佔盡資源令整個 VPS 宕機。
二、Hostinger Ubuntu 一鍵安裝 Docker 指令
bash
运行
# 更新系統套件
apt update && apt upgrade -y
# 安裝docker同compose插件
apt install docker.io docker-compose-plugin -y
# 設置開機自啟
systemctl enable --now docker

驗證安裝：
bash
运行
docker -v
docker compose version

輸出版本號即成功，之後進項目文件夾啟動整套服務。
三、唔裝 Docker 可行但弊端極大
手動逐個編譯 / 安裝 Ollama、Hermes (Python 環境)、OpenWebUI、Nginx；
人手配置 CPU、內存限制繁瑣；
後續升級、卸載容易殘留文件、破壞 VPS 原生系統。
小結
想沿用之前配置好嘅一鍵私有化 AI 堆：必須安裝 Docker，幾條指令兩分鐘搞妥。
需要我幫你整理成可直接複製嘅部署備忘短句嗎？
快速
编程
超能模式
Beta
PPT 生成
AI 表格
图像生成
更多
