---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# VPS-NVMe for Hostinger VPS - 豆包

**Date:** 2026-06-07 03:26
**Source:** 豆包

---

VPS:NVMe for Hostinger VPS
内容由豆包 AI 生成，请仔细甄别
Nginx simply explained
 
1. What Nginx is
 
Nginx = high-performance web server / reverse proxy software (free, open source, run on your KVM4 VPS).
 
2. Main jobs on your VPS (with Ollama + websites)
 
Host websites
Serve WordPress / static sites / OpenWebUI via domain name ( chat.yourdomain.com ,  blog.yourdomain.com ).
 
Reverse proxy (most useful for your AI)
Hide Ollama / Hermes backend ports behind domain:
 
- Point  chat.xxx.com → localhost:11434 (Ollama port) 
No need to expose raw server port directly to internet for safety.
 
Split multiple services on same 80/443 port
One VPS can run many sites/AI services under different domains using single IP.
 
Cache & speed up webpage load, add SSL(HTTPS).
 
3. Your real usage scenario on KVM4
 
- Nginx ≈ gatekeeper: route website traffic ↔ WordPress / OpenWebUI / Hermes panel
 
- Ollama + Qwen-VL runs backend separately, Nginx forwards web requests to AI API.
 
Short summary
 
Nginx is a popular server program to host websites & route your AI web frontends safely.
Simplified Nginx Explanation (trimmed for your Hostinger KVM4 VPS)
1. Basic Definition
Nginx is free open-source high-performance web server & reverse proxy application installed on your VPS.
2. Core Functions for your setup (Websites + Local Ollama AI)
Host websites: Deliver WordPress, static pages, OpenWebUI via custom domains like blog.yourdomain.com.
Reverse Proxy (key for your Ollama):
Mask internal backend ports from public internet:
Route chat.yourdomain.com → 127.0.0.1:11434 (default Ollama port), avoid exposing raw ports online for security.
Multi-service sharing: Run dozens of different websites/AI tools on one VPS IP via port 80(HTTP) /443(HTTPS) with separate domains.
Extra perks: Web caching for faster page loading + install SSL certificates to enable secure HTTPS.
3. Practical role on your KVM4 VPS
Acts as your server’s traffic gatekeeper: All incoming web requests go through Nginx, which distributes traffic to WordPress, OpenWebUI or your Hermes/Qwen-VL Ollama backend respectively. Your AI model runs independently in the background; Nginx handles all public-facing web access.
Quick Summary
Nginx manages website hosting and safely routes public domain traffic to your private local Ollama AI backend.
docker-compose.yml 一鍵包：Ollama + Hermes Agent + OpenWebUI + Nginx反向代理
 
適配你 KVM4(4C16G)，預設跑 qwen2-vl:7b-q4_K_M，部署完直接綁域名開網頁AI
 
1. 新建資料夾 + 建檔
 
bash
  
mkdir ai-stack && cd ai-stack
nano docker-compose.yml
 
 
貼下面全部代碼：
 
yaml
  
version: '3.8'

services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2.00'
          memory: 11G
    volumes:
      - ./ollama-data:/root/.ollama
    ports:
      - "127.0.0.1:11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0:11434

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: openwebui
    restart: always
    depends_on:
      - ollama
    volumes:
      - ./webui-data:/app/backend/data
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    expose:
      - "8080"

  hermes-agent:
    image: lmsys/hermes-agent
    container_name: hermes
    restart: always
    depends_on:
      - ollama
    environment:
      - OLLAMA_API=http://ollama:11434
      - DEFAULT_MODEL=qwen2-vl:7b-q4_K_M
    volumes:
      - ./hermes-data:/data
    expose:
      - "8000"

  nginx:
    image: nginx:alpine
    container_name: nginx-ai
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - open-webui
      - hermes-agent
 
 
2. 建立Nginx設定目錄 & 配置檔
 
bash
  
mkdir -p nginx/conf.d nginx/ssl
nano nginx/conf.d/ai.conf
 
 
貼入Nginx代理設定（後續改自己域名）：
 
nginx
  
# AI主聊天頁面 chat.你的域名.com
server {
    listen 80;
    server_name chat.xxx.com;
    location / {
        proxy_pass http://open-webui:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Hermes後台 agent.你的域名.com
server {
    listen 80;
    server_name agent.xxx.com;
    location / {
        proxy_pass http://hermes-agent:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
 
 
之後將  chat.xxx.com / agent.xxx.com  換成你實際域名，域名DNS指向VPS IP
 
3. 啟動容器 + 下載模型
 
bash
  
# 啟動整套服務
docker compose up -d

# 進入ollama容器拉7B VL模型
docker exec -it ollama ollama pull qwen2-vl:7b-q4_K_M
# 可選：拉hermes基礎模型
docker exec -it ollama ollama pull hermes3
 
 
4. 使用方法
 
chat.xxx.com → OpenWebUI網頁，揀選 qwen2-vl:7b，支援上圖多模態對話
 
agent.xxx.com → Hermes Agent控制面板，開啟工具調用、自動任務、伺服器操控
 
資源控制：Ollama鎖2核+11G記憶體，剩餘2C+5G RAM留俾Nginx、Wordpress等其他網站
 
5. SSL HTTPS加密（後續）
 
需要免費SSL證書我再補certbot一鍵指令，一齊配置HTTPS。
 
重點備註
 
- 全部服務內網互通，Ollama 11434唔對外公開，安全性高
 
- Hermes預設綁定Qwen2-VL 7B做Agent推理，圖片OCR+自動任務原生可用
簡化版部署手冊｜Docker-Compose 一鍵打包：Ollama+Qwen2-VL+OpenWebUI+Hermes Agent+Nginx 反向代理
專用 Hostinger KVM4（4 核 16G），預載 qwen2-vl:7b-q4_K_M，綁定域名即可上線網頁 AI
一、初始化資料夾與配置檔
bash
运行
mkdir ai-stack && cd ai-stack
nano docker-compose.yml

貼入docker-compose.yml完整配置：
yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2.00'
          memory: 11G
    volumes:
      - ./ollama-data:/root/.ollama
    ports:
      - "127.0.0.1:11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0:11434

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: openwebui
    restart: always
    depends_on:
      - ollama
    volumes:
      - ./webui-data:/app/backend/data
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    expose:
      - "8080"

  hermes-agent:
    image: lmsys/hermes-agent
    container_name: hermes
    restart: always
    depends_on:
      - ollama
    environment:
      - OLLAMA_API=http://ollama:11434
      - DEFAULT_MODEL=qwen2-vl:7b-q4_K_M
    volumes:
      - ./hermes-data:/data
    expose:
      - "8000"

  nginx:
    image: nginx:alpine
    container_name: nginx-ai
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - open-webui
      - hermes-agent

二、建立 Nginx 目錄 + 反向代理設定
bash
运行
mkdir -p nginx/conf.d nginx/ssl
nano nginx/conf.d/ai.conf

Nginx 配置（後續替換自訂域名）：
nginx
# OpenWebUI 聊天前台 chat.xxx.com
server {
    listen 80;
    server_name chat.xxx.com;
    location / {
        proxy_pass http://open-webui:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Hermes Agent 後台 agent.xxx.com
server {
    listen 80;
    server_name agent.xxx.com;
    location / {
        proxy_pass http://hermes-agent:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

修改 chat.xxx.com / agent.xxx.com 為自己域名，域名 DNS A 記錄指向 VPS 公網 IP
三、一鍵啟動服務 + 拉取 AI 模型
bash
运行
# 後台啟動全部容器
docker compose up -d

# 下載預設多模態模型 Qwen2-VL 7B量化版
docker exec -it ollama ollama pull qwen2-vl:7b-q4_K_M

# 可選：下載Hermes專用模型
docker exec -it ollama ollama pull hermes3

四、訪問說明
chat.xxx.com → OpenWebUI 網頁對話，選用qwen2-vl:7b-q4_K_M，支援上傳圖片、OCR、多模態問答
agent.xxx.com → Hermes Agent 控制面板，開啟函數調用、自動任務、Agent 自動執行
資源分配（KVM4 4C16G 專屬）
Ollama：限定2 核 + 11GB 內存
剩餘：2 核 + 5GB RAM 預留給 Nginx、WordPress 或其他網站程式
五、後續 HTTPS SSL（免費證書）
需要可執行 Certbot 自動簽證，一鍵全域名改成 HTTPS。
關鍵優勢
Ollama 11434 僅綁定本機127.0.0.1，埠口不暴露公網，透過 Nginx 域名反向代理，伺服器安全性高
容器內網互通，不用手動改 API 位址
Hermes 預設綁定 Qwen2-VL 7B，開箱即用圖文 Agent 功能
需要我補充Certbot 一鍵 SSL 腳本嗎？
快速
编程
超能模式
Beta
PPT 生成
AI 表格
图像生成
更多
