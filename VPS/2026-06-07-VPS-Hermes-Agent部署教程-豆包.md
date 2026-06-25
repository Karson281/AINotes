---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# VPS-Hermes Agent部署教程 - 豆包

**Date:** 2026-06-07 03:26
**Source:** 豆包

---

VPS:Hermes Agent部署教程
内容由豆包 AI 生成，请仔细甄别
補全Hermes一鍵部署+7B專用.env配置腳本
Hostinger KVM4(4C16G)一鍵部署：Ollama+Qwen2-VL-7B-Q4_K_M + Hermes Agent 完整Shell腳本
使用：新建deploy_hermes.sh，複製全部內容，chmod +x deploy_hermes.sh && ./deploy_hermes.sh
bash
运行
#!/bin/bash
set -e
echo "=====開始部署Ollama + Hermes Agent(Qwen2-VL-7B) KVM4優化配置====="

# 1.系統更新&基礎依賴
apt update -y && apt install git ca-certificates curl build-essential -y

# 2.安裝Ollama
curl -fsSL https://ollama.com/install.sh | sh
systemctl enable --now ollama

# 3.Ollama專用配置(4C16G優化)/etc/default/ollama
cat > /etc/default/ollama <<'EOF'
OLLAMA_HOST=127.0.0.1
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_NUM_PARALLEL=2
OLLAMA_MAX_VRAM=12G
OLLAMA_CPU_THREADS=4
OLLAMA_NO_AUTO_PULL=false
EOF
systemctl restart ollama

# 4.下載Qwen2-VL:7b-q4_K_M
echo "正在拉取Qwen2-VL 7B Q4_K_M模型，耗時依網速"
ollama pull qwen2-vl:7b-q4_K_M

# 5.配置2GB Swap(備用，KVM4日常基本不用swap)
if [ ! -f "/swapfile" ];then
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi
sysctl vm.swappiness=5
echo "vm.swappiness=5" >> /etc/sysctl.conf

# 6.安裝Node20+ & PM2
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install nodejs -y
npm install -g pm2

# 7.拉取Hermes-Agent源碼(替換為你真實Github倉庫地址，現行通用範例)
mkdir -p /opt/hermes-agent && cd /opt/hermes-agent
# =========如果你的Hermes倉庫地址不同，修改下面git地址=========
git clone https://github.com/yourname/Hermes-Agent.git tmp && mv tmp/* ./ && rm -rf tmp
npm install

# 8.生成KVM4專用.env(7B主力完整版配置 32K上下文)
cat > .env <<'EOF'
OLLAMA_URL=http://127.0.0.1:11434
DEFAULT_MODEL=qwen2-vl:7b-q4_K_M
SERVER_PORT=3000
MAX_CONTEXT_LENGTH=32768
MAX_HISTORY_ROUND=12
DISABLE_PRECOMPUTE_CACHE=false
DISABLE_BACKGROUND_PREFILL=false
MAX_IMAGE_PX=2000
MAX_UPLOAD_FILE_SIZE=5MB
MAX_AGENT_PARALLEL_TASK=2
SUB_AGENT_MAX_COUNT=3
ENABLE_AUTO_CTX_COMPRESS=true
EOF

# 9.PM2常駐啟動Hermes，內存上限1500M
pm2 delete hermes-agent || true
pm2 start npm --name hermes-agent --max-memory-restart 1500M -- start
pm2 startup
pm2 save

# 10.放行防火牆埠
ufw allow 3000/tcp
ufw allow 11434/tcp
ufw reload

echo "======================================"
echo "部署完成！"
echo "1.網頁訪問：http://你的VPS_IP:3000"
echo "2.模型：qwen2-vl:7b-q4_K_M | 上下文32K全開"
echo "3.如需切換8B：修改.env內DEFAULT_MODEL，pm2 restart hermes-agent"
echo "======================================"

補充操作說明
修改Hermes源碼地址
找到腳本內 git clone 行，替換成真實專案Github地址。
切換Qwen3-VL 8B高精度模式
bash
运行
cd /opt/hermes-agent
sed -i 's|DEFAULT_MODEL=qwen2-vl:7b-q4_K_M|DEFAULT_MODEL=qwen3-vl:8b-q4_K_M|' .env
# 同步壓縮上下文至24K
sed -i 's|MAX_CONTEXT_LENGTH=32768|MAX_CONTEXT_LENGTH=24576|' .env
sed -i 's|MAX_AGENT_PARALLEL_TASK=2|MAX_AGENT_PARALLEL_TASK=1|' .env
pm2 restart hermes-agent

bash
运行
# 切換前先拉取8B模型
ollama pull qwen3-vl:8b-q4_K_M

Hostinger後台補充
Hostinger控制面板防火牆手動放行：3000、11434 埠。
資源對照（部署完閒置）
Ollama載入7B：9.5~11GB RAMHermes常駐：<1.2GB RAM系統剩餘：4GB+空閒內存，無Swap。
KVM4（4vCPU+16GB RAM）：Ollama+Hermes Agent 照常跑，剩餘資源仲可以整大量網站/自託服務（廣東話講解）
 
一、資源現況（跑Qwen2.5-VL 7B Q4_K_M + Hermes常駐）
 
- AI側佔：RAM約10～11GB、CPU閒置2～3核，剩餘5GB左右RAM+1～2個vCPU完全空閒，200GB NVMe都用唔曬
 
- 資源分開用：Ollama綁定2核、網站同其他程式用剩餘2核，唔會互相搶資源卡頓
 
二、可以額外整嘅網站功能（全部一齊共存無壓力）
 
1、常規建站（WordPress/靜態網站/小型商城）
 
WordPress多站點：Nginx+MySQL，可架3～5個個人部落格、小型企業官網、資訊站，日IP幾千訪客都穩定；小型WooCommerce網店（細型電商）都得
 
靜態網站（Hexo/VitePress/Hugo）：幾十個靜態站都無所謂，極少佔內存
 
PHP程式網站：Typecho、Zblog、Discuz論壇（小型社群論壇）
 
2、AI配套專屬網頁（同Hermes打通，最實用）
 
Open WebUI（AI對話網站）：綁Ollama，獨立域名 chat.xxx.com，網頁版私有Qwen-VL圖文對話，連埋Hermes Agent做後端智能調用
 
Hermes後台控制面板網站：hermes-control網頁面板，瀏覽器管理Agent任務、記憶體、自訂工具
 
自製API網站：前端網頁呼叫本機Ollama API，整自訂AI工具網站（OCR、圖片解析、文檔總結網頁）
 
3、自託雲端工具網站（自架服務）
 
- n8n自動化流程網站：自動爬網、郵件處理、Hermes任務觸發，網頁後台配置自動化工作流
 
- Coolify面板：一站式伺服器管理網頁，一鍵新增網站、資料庫、Docker應用，唔使手動敲指令部署網站
 
- FileBrowser私有雲盤網站：xxx.com/drive，私人雲盤，Hermes可自動讀寫盤內圖片/文件做VL解析
 
- RSS聚合網站、短網址服務、私人代理面板全部都裝到
 
4、小型後台/程式服務
 
- Node.js/Python開發小程式網站、後台管理系統
 
- 私人數據庫（PostgreSQL/MySQL），供網站同Agent共用存資料
 
三、資源使用分界建議（唔卡機最佳配置）
 
Ollama + Hermes：限定2vCPU、最大11GB RAM（docker資源限制）
 
網站+Nginx+數據庫+各類網頁服務：剩餘2vCPU、4～5GB RAM
 
就算網站突發訪客暴衝，AI最多輕微減速，唔會崩潰OOM
 
四、唔建議嘅場景
 
- 大型商城、日訪過萬流量大站（會搶資源拖慢Ollama推理）
 
需要我幫你整一套docker-compose一鍵配置：Ollama+Hermes+OpenWebUI+Nginx網站環境嗎？
KVM4 (4C16G) Docker Compose 一鍵套件｜Ollama+Hermes+OpenWebUI+Nginx 建站環境（粵語備註、資源隔離分核）
分工邏輯：Ollama 綁定 2 核、上限 11G 內存｜剩餘 2 核 + 5G RAM 留俾 OpenWebUI、網站、資料庫、各類自建服務，互不搶資源儲存：200GB NVMe 空間極充裕，數據持久化掛載本地目錄
1、全量 docker-compose.yml 直接複製使用
yaml
version: "3.8"

# 資源隔離網段，AI同網站服務分開網絡
networks:
  ai_net:
  web_net:

services:
  # ① Ollama：限定2vCPU、最大11GB RAM，專門跑Qwen2.5-VL 7B q4_K_M
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 11G
    environment:
      OLLAMA_HOST: 0.0.0.0:11434
      OLLAMA_NUM_PARALLEL: 2
      OLLAMA_CPU_THREADS: 2
    volumes:
      - ./ollama_data:/root/.ollama
    ports:
      - "127.0.0.1:11434:11434"
    networks:
      - ai_net
    restart: always

  # ② OpenWebUI：獨立AI對話網站 chat.你的域名.com
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: openwebui
    volumes:
      - ./webui_data:/app/backend/data
    environment:
      OLLAMA_BASE_URL: http://ollama:11434
    ports:
      - "3001:8080"
    networks:
      - ai_net
      - web_net
    depends_on:
      - ollama
    restart: always

  # ③ Hermes Agent：KVM4專用7B配置、32K上下文
  hermes-agent:
    build: ./hermes
    container_name: hermes
    env_file: ./hermes/.env
    ports:
      - "3000:3000"
    networks:
      - ai_net
      - web_net
    environment:
      OLLAMA_URL: http://ollama:11434
    depends_on:
      - ollama
    restart: always

  # ④ Nginx+MySQL：建站基礎，剩餘2核自由使用
  nginx:
    image: nginx:alpine
    container_name: nginx
    volumes:
      - ./nginx/conf:/etc/nginx/conf.d
      - ./www_root:/usr/share/nginx/html
    ports:
      - "80:80"
      - "443:443"
    networks:
      - web_net
    restart: always

  mysql:
    image: mysql:8.0
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: 自訂密碼
      MYSQL_DATABASE: site_db
    volumes:
      - ./mysql_data:/var/lib/mysql
    ports:
      - "127.0.0.1:3306:3306"
    networks:
      - web_net
    restart: always

2、建立 Hermes 專用 .env（對應 7B、KVM4 滿配 32K 上下文）
路徑：./hermes/.env
env
OLLAMA_URL=http://ollama:11434
DEFAULT_MODEL=qwen2-vl:7b-q4_K_M
SERVER_PORT=3000
MAX_CONTEXT_LENGTH=32768
MAX_HISTORY_ROUND=12
DISABLE_PRECOMPUTE_CACHE=false
DISABLE_BACKGROUND_PREFILL=false
MAX_IMAGE_PX=2000
MAX_UPLOAD_FILE_SIZE=5MB
MAX_AGENT_PARALLEL_TASK=2
SUB_AGENT_MAX_COUNT=3
ENABLE_AUTO_CTX_COMPRESS=true

3、部署步驟（Hostinger Ubuntu 直接逐行打）
bash
运行
# 1.建立資料夾
mkdir -p /opt/ai-stack && cd /opt/ai-stack
mkdir -p hermes nginx/conf www_root ollama_data webui_data mysql_data

# 2.放入上面嘅docker-compose.yml同hermes/.env配置
# 3.安裝docker
apt update && apt install docker.io docker-compose-plugin -y
systemctl enable --now docker

# 4.後台拉取Qwen模型（容器啟動前先下載）
ollama pull qwen2-vl:7b-q4_K_M
# 同步將模型複入掛載目錄，避免容器重裝重下載
cp -r /usr/share/ollama/.ollama/models ./ollama_data/

# 5.一鍵啟動全套服務
docker compose up -d

4、各服務訪問地址
Hermes Agent：IP:3000
OpenWebUI (AI 對話網站)：IP:3001，後續 Nginx 綁定域名 chat.xxx.com
網站根目錄：./www_root，直接放 WordPress / 靜態網站，80 埠綁定域名
5、資源運行說明（廣東話重點）
Ollama 鎖死 2 核 + 11G RAM，無論網站爆訪、資料庫跑查詢，都搶唔到 AI 資源，7B 推理速度長期穩定
剩餘 2vCPU + 約 5GB RAM：Nginx+MySQL + 多個 WP 站 + FileBrowser+n8n 一齊跑都綽綽有餘
16TB 流量、1Gbps 寬頻：細型網站 + AI 訪問完全唔使驚爆流量
6、後續加裝自建服務（一齊兼容）
想加：FileBrowser、n8n、Coolify，直接落 docker-compose 新增 service 就得，全部放 web_net 網段、使用剩餘空閒資源。
需要我順便補 Nginx 範例配置（綁定多個域名：主站 + chat 子域名）嗎？
快速
编程
超能模式
Beta
PPT 生成
AI 表格
图像生成
更多
