---
creation_date: 2026-06-07
source: "Perplexity"
tags:
  - ai/perplexity
status: inbox
---

# VPS-kvm2 vps 詳細部署hermes agent on a 8GB Ram KVM2 server?

**Date:** 2026-06-07 23:08
**Source:** Perplexity

---

回答
連結
圖片
視頻
分享
下載 Comet
VPS: kvm2 vps 詳細部署hermes agent on a 8GB Ram KVM2 server?
Hermes Agent 完整设置教程：一步一步指南
Hermes Agent 完整安装教程（Win + Mac）+ 9 个核心技巧
別再修龍蝦了！最聰明Hermes Agent 全平台安裝全攻略，自我 ...

在 8GB RAM 的 KVM2 VPS 上部署 Hermes Agent，最推薦使用 Docker 一鍵部署（簡單、資源隔離好）或 手動安裝 + tmux 背景運行（更靈活）。以下是完整步驟：

方法一：Docker 一鍵部署（推薦新手）
1. 安裝 Docker
bash
# 更新系統
sudo apt update && sudo apt install -y curl git

# 安裝 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 加入 docker 群組
sudo usermod -aG docker $USER
newgrp docker
2. 使用 Hostinger 一鍵模板或官方 Docker
bash
# 克隆官方倉庫
git clone https://github.com/NousResearch/Hermes-Agent.git
cd Hermes-Agent

# 使用 Docker Compose 部署
docker-compose up -d

或使用現有 Docker 映像後配置環境變數 。
youtube
zeabur

方法二：手動安裝（完整控制）
1. 環境準備
bash
# 安裝依賴
sudo apt update
sudo apt install -y python3.10 python3-pip python3-venv nodejs npm git curl

# 確認版本
python3 --version  # 需要 3.10+
node -- version    # 需要 18+
2. 安裝 Hermes Agent
bash
# 克隆倉庫
git clone https://github.com/NousResearch/Hermes-Agent.git
cd Hermes-Agent

# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝
pip install -e .
3. 初始化配置
bash
# 初始化設定（選 Quick setup）
hermes setup

# 配置 LLM 供應商（OpenRouter/Claude/OpenAI）
hermes gateway setup

# 啟動 Web 介面（http://localhost:7860）
hermes start
4. 使用 tmux 背景運行（VPS 必需）
bash
# 安裝 tmux
sudo apt install -y tmux

# 建立 tmux 會話
tmux new -s hermes

# 在 tmux 中啟動
source venv/bin/activate
hermes start

# 按 Ctrl+B 然後 D 離開 tmux（程序繼續運行）
關鍵配置要點
項目	建議設定
API 提供商	OpenRouter（支援多模型）或 Claude 官方 
youtube

模型選擇	Claude 4.6 或 Gemma 4 31B（免費）
youtube
+1

HTTPS	安裝 Traefik 免費證書確保安全 
youtube

SSH 安全	關閉密碼登入，改用 SSH key 
youtube

記憶體	8GB RAM 足夠運行 Hermes + Python + Node + memory 索引 
youtube
常用指令
bash
# 啟動命令行對話
hermes chat

# 查看配置
hermes config

# 檢查環境
hermes doctor

# 查看長期記憶
/memory

# 安裝技能
hermes skills search [關鍵字]
hermes skills install [作者/名稱]
安全注意事項 ⚠️

SSH 強化：關閉密碼登入，改用 SSH key，避免 API key 被刷光
youtube

HTTPS 證書：安裝 Traefik 確保通信安全
youtube

API Key 保護：不要在公開倉庫暴露 API key

Hermes Agent 需要 24 小時在線以累積記憶，VPS 是最佳部署環境 。8GB RAM 的 KVM2 方案完全足夠運行完整功能 Including memory indexing 。
youtube

9 個來源
如果我有手機Android , 筆電Windows 11，用哪配置更好？
已完成 2 個步驟

結論：在 Windows 11 筆電上部署 Hermes Agent，Android 手機只當「遠端控制 / 聊天介面」，會比直接在 Android 上跑好很多。

這是基於技術與使用體驗的實際原因：

1. Hermes Agent 的「核心的」部署方式

Hermes 官方明確支援的部署平台是：
macOS、Linux、WSL2（Windows 上）、Termux，而且安裝流程是設計成「Linux 終端機的一鍵腳本」。手機端雖然有 Android 版 Apps 和 Termux 方案，但主要是作為：

本地聊天介面

用 Termux 當 Linux 終端機跑

橋接到 Android 手機的硬體（讀 SMS、觸控、相機等）

官方文件也明確把 Linux / macOS / WSL2 當成主要路徑，而不是原生 Android App 。
news.ycombinator
youtube

2. Windows 11 筆電：最佳「主部署」平台
優點
項目	說明
官方支援路徑	Windows 上建議用 WSL2 + Ubuntu，然後直接跑 curl ... | bash 安裝 Hermes Agent，流程完整、社群使用最多 
youtube

資源充足	筆電通常有 8–16GB RAM、多核心 CPU，跑 Hermes + 模型 + Gateway 比手機穩定很多 
Memory

长駐能力	可以長期開著當伺服器，用 PowerShell / Terminal 或 tmux / systemd 跑，不會被系統關機或休眠強殺
工具生態	有完整 Git、Python、Node.js、CLI 工具，方便安裝 skill、設定 gateway、調試
安全性	可以在 WSL2 中隔離環境，用一般使用者跑，不用 root
部署方式（簡化版）
powershell
# PowerShell (管理員)
wsl --install          # 如果還沒裝 WSL2
wsl                    # 進入 Ubuntu

在 WSL2 的 Ubuntu 中：

bash
sudo apt update && sudo apt install -y curl git
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc
hermes setup

完成後再設定模型與 Gateway（如 Telegram）。這樣的流程在 Windows 上已經被教學驗證過，能無痛跑起來 。
youtube

3. Android 手機：適合當「遠端介面」，不是主伺服器
Android 的選項

官方 Android App（Google Play）

整合多模型、內建 Linux 終端機、可跑 code、支援 Telegram / Slack / Discord Gateway
play.google
+2

需要自己帶 API key，不用雲端帳號

適合：在手機上直接聊天、跑簡單指令、遠端控制

Termux + 一行安裝腳本

官方 Hermes 文件也提供 Android / Termux 的安裝頁面
hermes-agent.nousresearch

流程類似 macOS / Linux，但手機資源有限，跑大量工具或長期任務會較卡

用舊 Android 跑 agent 當伺服器

有人用舊 Android + Termux 跑 Hermes，當 24/7 agent，能讀 SMS、發社交貼文、處理 2FA 等
x

這需要：舊手機、長期插電、穩定網路、Root 或 Termux API，對一般使用者來說設定門檻較高

Android 的缺點（當主部署）
問題	影響
資源有限	RAM 小、CPU 弱，跑大型模型 + 多工具會卡，容易 overheating
系統限制	背景執行容易被殺，網路暫停、休眠，不適合長期 24/7 agent
設定複雜	Termux + API + 權限 + 啟動腳本，對一般使用者較麻煩
穩定性	手機更新、App 更新、系統清理都可能斷掉
4. 最佳配置建議：筆電部署 + Android 遠端控制
推薦架構

主部署：Windows 11 筆電 + WSL2 + Hermes Agent

Hermes 真正「伺服器端」跑在 WSL2 的 Ubuntu 上

設定好模型（如 Google Gemini、OpenRouter、MiniMax 等）與 Telegram Gateway

筆電可以長期開著，或當你用時才開

Android 手機：用 Telegram 或 Hermes Android App 當介面

用 Telegram 與 Hermes 對話：

在筆電上跑 hermes gateway setup → 選 Telegram → 建立 Bot → 拿到 Token → 啟動 hermes gateway &

然後在手機上打開 Telegram，點你的 bot，就能隨時打指令、查資料、控制任務
facebook
youtube

或用 Hermes Android App 直接連同一個 agent（透過 dashboard / API），在手上看進度、聊天、跑簡單指令
play.google
+1

這樣的好處

穩定性：主程式在筆電上，不太會被系統殺掉

彈性：手機隨時用 Telegram / App 控制，不用開筆電

資源：Heavy 任務在筆電跑，手機只做通訊與輕量操作

易維護：更新、設定、調試主要在筆電上，符合官方教學流程

5. 如果你更重視「手機為主」

如果你希望：

筆電不常開

主要用手機做所有事（包含長期任務）

那麼可以考慮：

舊 Android + Termux 跑 Hermes + 長期插電，當 24/7 agent
x

需要：舊手機、穩定網路、插電、背景執行不被殺（可能要 Root 或特殊設定）

或直接用 Hermes Android App 跑，但長期任務會比較受限制

這適合：

有舊 Android 手機、愛折腾、想省下 VPS 或筆電常開成本

但對一般使用者來說，穩定性和維護成本不如筆電 / VPS。

總結建議

對你目前的情況（Android 手機 + Windows 11 筆電）：

主部署：Windows 11 筆電 + WSL2 + Hermes Agent

遠端介面：Android 手機上用 Telegram（搭配 Hermes Gateway）或 Hermes Android App

如果你希望，我可以下一步直接幫你寫：

Windows 11 + WSL2 的完整 Hermes 安裝與 Telegram Gateway 設定腳本

Android 手機上如何用 Telegram 連上 Hermes 的步驟（含 BotFather、User ID、Token 設定）

你只要告訴我：

你比較想用 Telegram 還是 Hermes Android App 當主要介面？

你筆電的 RAM 大概多少（8GB / 16GB / 其他）？

21 個來源
我意思是kvm2 如何組態？

你要的是 KVM2 VPS 的具體配置（CPU/RAM/硬碟/OS/網路等），好讓 Hermes Agent 跑得穩。根據 Hermes 部署指引與 VPS 實戰經驗，下面是針對 Hermes Agent 的 KVM2 最佳配置 與 到部署步驟（含 Telegram Gateway）。

1. KVM2 硬體配置建議
最低可用（只跑 CLI + 簡單任務）
項目	建議
vCPU	1 核心
RAM	1–2 GB
硬碟	20 GB NVMe / SSD
流量	1 TB/月
適用	只跑 CLI、簡單任務、測試用

Hermes 在 1GB 記憶體筆電上能跑，但 VPS 要長期常駐 + Gateway + 多工具，建議 至少 2GB RAM。
Memory

推薦配置（適合長期常駐 + Telegram Gateway）
項目	建議
vCPU	2 核心
RAM	4 GB
硬碟	40–60 GB NVMe
網路	1 Gbps 带宽
流量	3–4 TB/月
OS	Ubuntu 24.04 LTS
適用	跑 Hermes + Telegram Gateway + 多 skill + cron 任務

現有教學明確推薦 Hostinger KVM2 就夠用，且年付更便宜，並建議用 Ubuntu 24.04 LTS，還可選擇 Docker 方式部署（每個 agent 獨立容器）。
x

雲端實戰也建議 2 核 4G 配置，搭配 Hermes 鏡像，5 步完成部署。
cloud.tencent

高配（多 agent / 繁重任務）
項目	建議
vCPU	4 核心
RAM	8 GB
硬碟	80–100 GB NVMe
流量	5 TB+/月
適用	多個 Hermes agent、大量 cron、複雜 skill、本地模型
2. 虚拟化與 OS 選擇

虛擬化：KVM（大多數 VPS 商都標 KVM）

OS：

首選：Ubuntu 24.04 LTS（官方 Hermes 安裝腳本對 Ubuntu/Debian 支援最好）
x

次選：Debian 12、Ubuntu 22.04 LTS

Docker：如果選 Hostinger 等，可透過 Marketplace 一鍵安裝 Hermes（Docker 容器方式），每個 agent 隔離更好
x

3. 網路與地理配置
機房位置

選擇機房時，主要看你的使用地區：

主要使用者/訪問地區	建議機房
歐洲 / 中東	歐洲機房（如巴黎、法蘭克福）
亞太 / 中國	洛杉磯、東京、新加坡
多地區監控/多出口	混搭不同機房（歐 + 美）

你人在香港，想對香港/台灣/亞太的延迟低，建議選 洛杉磯、東京、新加坡 機房，避免預設歐洲機房導致延遲高。
sites.google

網路線路（針對中國用戶）

電信：優先 CN2 GIA 線路

聯通：較寬容

移動：較為困難

如果主要從中國訪問，選 CN2 GIA 較穩。
sites.google

4. 部署 Hermes Agent（KVM2 VPS 步驟）
步驟 1：選 Ubuntu 24.04 LTS 並 SSH 登入

以 Hostinger 為例：

在 Hostinger 選 KVM2 + Ubuntu 24.04 LTS

部署完成後，改 hostname 方便辨識：

bash
hostname yaml-hermes

用 SSH 連上：

bash
ssh root@你的VPS_IP
# 或
ssh ubuntu@你的VPS_IP
步驟 2：安裝前置依賴
bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git
步驟 3：安裝 Hermes Agent

用官方一行安裝腳本：

bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc

官方安装流程會自動處理 uv、Python 3.11、Node.js 22、ripgrep、ffmpeg 等依賴。
Memory

步驟 4：初始設定
bash
hermes doctor
hermes setup
# 或
hermes setup --portal

hermes setup 會引導你選擇模型供應商（如 OpenAI、Google Gemini、OpenRouter、MiniMax 等）並輸入 API key。

步驟 5：接入 Telegram Gateway

在 Telegram 找 @BotFather，發 /newbot 建立機器人，用户名以 Bot 結尾

複製 Bot Token

找 @userinfobot 取得你的 Telegram User ID

在 Hermes 上：

bash
hermes gateway setup

選擇 Telegram → 貼上 Token → 貼上 User ID → 鎖定只回應你。
x

啟動 Gateway：

bash
hermes gateway &

完成後，手機用 Telegram 點你的 bot 即可控制 Hermes。
youtube
facebook

步驟 6：API key 管理（安全）

不要在聊天裡直接貼 key。SSH 進容器 / VPS：

bash
hermes config set GITHUB_TOKEN <你的token>
hermes config set OPENAI_API_KEY <你的key>

key 會存進 /opt/data/.env，模型看不到，安全性較高。
x

步驟 7：設定開機自啟（systemd）

若要 24/7 常駐，建議建 systemd 服務（可簡化版）：

bash
sudo nano /etc/systemd/system/hermes.service

內容類似：

text
[Unit]
Description=Hermes Agent Service
After=network.target

[Service]
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/hermes run
Restart=always
Environment="PATH=/root/.local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target

然後：

bas
