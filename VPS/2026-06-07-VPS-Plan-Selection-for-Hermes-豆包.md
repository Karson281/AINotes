---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# VPS-Plan Selection for Hermes - 豆包

**Date:** 2026-06-07 03:25
**Source:** 豆包

---

VPS: Plan Selection for Hermes
内容由豆包 AI 生成，请仔细甄别
Hostinger KVM4（4vCPU+16GB RAM+200GB NVMe+16TB流量）價格（2026官網現價、港區/美元/人民幣）
 
一、分訂購週期價格（重點：首年優惠價｜續約原價）
 
1. 綁24個月（最划算、推薦Ollama長期跑AI）
 
- 首月優惠：$11.69 USD/月 ≈ 91 HKD / 84 RMB
 
- 2年後續約原價：$28.99 USD/月 ≈ 226 HKD / 208 RMB
 
2. 綁12個月
 
- 優惠：$12.99 USD/月 ≈101 HKD/93 RMB
 
- 續約：$28.99 USD/月
 
3. 月付不綁約（隨時退租、短期測試）
 
- 單月原價：$29.99 USD/月≈234 HKD/215 RMB（無折扣最貴）
 
4. 香港官網人民幣標價（hostinger.com/hk）
 
優惠價：94.99 CNY/月｜續約：211.99 CNY/月
 
二、硬體規格確認（跑Qwen-VL+Hermes Agent）
 
- 4vCPU(AMD EPYC)、16GB實體RAM、200GB NVMe、16TB月流量、1Gbps網路、免費每週備份
✅ 穩跑：Qwen2.5-VL 7B q4_K_M全功能Hermes Agent（32K上下文）
⚠️ 14B僅能測試、常開Agent容易吃滿記憶體swap
 
三、同方案對比（原KVM2升級成本）
 
KVM2(2核8G)優惠$8.09/月，升級KVM4每月多出約3.6~4.9美元，內存翻倍、NVMe/流量翻倍。
 
四、選購建議
 
長期部署Ollama私有Agent→選24月方案（單月最便宜）
 
先試用1~2個月測模型→選月付方案
 
需要幫你換算成港幣實付、或是KVM4專用Ollama安裝指令嗎？
Hostinger KVM4｜4核16G｜2026香港官网实价（USD/HKD/CNY）+Ollama+Hermes落地配置
一、套餐定价（3种签约周期，AMD EPYC｜16GB内存｜200GB NVMe｜16TB月流量｜1Gbps｜每周免费备份）
汇率参考：1USD≈7.8HKD≈7.2CNY
1. 24个月合约（长期部署Ollama首选，最低价）
美元优惠：$12.99/月｜港币≈101.3HKD/月｜人民币≈93.5CNY/月
合约到期续费原价：$28.99/月｜≈226.1HKD｜≈208.7CNY
香港官网人民币标价：优惠94.99CNY/月，续费211.99CNY/月
2. 12个月合约
优惠：$12.99/月｜≈101.3HKD｜≈93.5CNY
续费同原价$28.99/月
3. 月付无合约（短期测试试用）
原价：$29.99/月｜≈233.9HKD｜≈215.9CNY（无折扣最贵）
二、硬件适配AI部署明细（Qwen2.5-VL 7B q4_K_M + Hermes多进程）
模型内存占用：Qwen2.5-VL-7B q4_K_M CPU离线运行常驻4.2～5.8GB内存
KVM4剩余可用内存：16G - 系统1G - Ollama模型6G = 9G富余内存
✅ 稳定部署：4个Hermes独立systemd实例（8080/8081/8082/8083）并行多任务
⚠️ 14B量化模型满载占用≥11G，仅适合单实例测试，多开极易触发Swap爆满卡顿
三、KVM2→KVM4升级成本对比
KVM2(2核8G)24月优惠：$8.99/月
KVM4每月溢价：$4/月左右，内存/硬盘/流量全部翻倍，完美解决KVM2多Hermes实例OOM问题
四、Ollama+Hermes一键部署命令（Ubuntu24.04专用）
1. 安装Ollama
bash
curl -fsSL https://ollama.com/install.sh | sh
# 拉取目标多模态模型
ollama pull qwen2.5-vl:7b-q4_K_M

2. Ollama全局并发限制（避免爆内存）
bash
# 写入环境变量，限制最大加载模型3个、单模型并发2任务
echo 'export OLLAMA_MAX_LOADED_MODELS=3' >> /etc/profile
echo 'export OLLAMA_NUM_PARALLEL=2' >> /etc/profile
source /etc/profile

3. Hermes对接本地Ollama
Hermes启动参数追加：--base-url http://127.0.0.1:11434/v1沿用之前hermes@.service多实例配置，4端口直接全开。
五、选购建议
长期私有化Agent商用（≥6个月）：24个月套餐，性价比天花板
新项目测模型（1-2个月）：月付套餐，随时停机退款
TG网关分流：4个Hermes端口分组分流用户，完全无任务排队阻塞
需要我生成4实例Hermes一键启停shell脚本吗？
完全可以共存，本身就係一組搭配架構，Hermes一定要靠Ollama先可以跑本地Qwen-VL
 
一、兩個分工（你部4vCPU+16GB KVM剛剛夾）
 
Ollama：負責跑大模型（Qwen-VL、Hermes3等）
佔RAM多，做圖文推理、模型載入，開放 127.0.0.1:11434 API接口
 
Hermes Agent：智能體外殼（任務拆解、記憶庫、40+工具、自動執行指令）
唔載模型，淨係透過API呼叫Ollama做推理、操控伺服器檔案/網頁/終端
 
簡單講：Ollama係AI大腦，Hermes係負責思考同做動作嘅手腳，缺一唔可以本地跑Agent
 
二、你VPS資源分配（16GB RAM最穩配置）
 
- Ollama + Qwen-VL 7B Q4_K_M：10～11GB RAM、2核CPU常駐
 
- Hermes常駐：1～1.5GB RAM、剩餘少量CPU
 
- 剩餘3～4GB RAM + 2vCPU：放Nginx、Wordpress、OpenWebUI等網站服務，唔衝突
 
三、一鍵啟動方法（Ollama原生支援Hermes）
 
bash
  
# 1.落Qwen-VL同Hermes模型
ollama pull qwen-vl:7b-q4_K_M
ollama pull hermes3
# 2.自動安裝+掛接Hermes（自動綁11434接口）
ollama launch hermes
 
 
之後Hermes入面直接切換 qwen-vl:7b 就可以圖文Agent運作
 
四、額外好處
 
隨時換模型：想轉Llama3、Qwen2.5只需要 ollama pull ，Hermes改個model名就得
 
搭配Nginx：開 chat.xxx.com 網頁介面，外網入面用Hermes Agent對話Qwen-VL
 
全離線：所有數據留係你KVM伺服器，唔使雲API費用
 
需要我直接俾docker-compose一鍵腳本：Ollama+Hermes+OpenWebUI+Nginx一齊部署？
Docker Compose 一键部署：Ollama + Hermes Agent + OpenWebUI + Nginx（适配 Hostinger KVM4｜Ubuntu24.04｜本地 Qwen-VL 7B）
架构分工：
Ollama：本地承载 Qwen-VL 7B-Q4_K_M、Hermes3 模型，内网 11434 端口
Hermes：Agent 调度、工具调用、记忆管理，多实例 Systemd 对接 Ollama API
OpenWebUI：可视化网页对话前端
Nginx：反向代理域名，外网安全访问
1. 新建部署目录 & compose 文件
bash
运行
mkdir -p /opt/ai-stack && cd /opt/ai-stack
nano docker-compose.yml

粘贴完整配置：
yaml
version: "3.8"

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: always
    volumes:
      - ./ollama-data:/root/.ollama
    deploy:
      resources:
        limits:
          cpus: '3.0'
          memory: 11G
    ports:
      - "127.0.0.1:11434:11434"
    environment:
      - OLLAMA_MAX_LOADED_MODELS=2
      - OLLAMA_NUM_PARALLEL=2

  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: openwebui
    restart: always
    volumes:
      - ./webui-data:/app/backend/data
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    ports:
      - "127.0.0.1:8088:8080"

  nginx:
    image: nginx:alpine
    container_name: ai-nginx
    restart: always
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - openwebui
    ports:
      - "80:80"

2. 初始化 Nginx 配置
bash
运行
mkdir -p ./nginx/conf.d
nano ./nginx/conf.d/default.conf

nginx
server {
    listen 80;
    server_name chat.你的域名.com;

    location / {
        proxy_pass http://openwebui:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

替换chat.你的域名.com为自有域名，无域名可本机 127.0.0.1:8088 访问 WebUI
3. 启动容器 & 拉取模型
bash
运行
# 启动整套服务
docker compose up -d

# 进入ollama容器拉取模型
docker exec -it ollama ollama pull qwen-vl:7b-q4_K_M
docker exec -it ollama ollama pull hermes3

4. Hermes 多进程对接本地 Ollama（沿用之前 systemd@模板）
修改/etc/systemd/system/hermes@.service里启动指令：
ini
ExecStart=/usr/local/bin/hermes chat --port %i --base-url http://127.0.0.1:11434/v1 --model qwen-vl:7b-q4_K_M

重载配置、开启 4 个实例（KVM4 标配：8080/8081/8082/8083）
bash
运行
systemctl daemon-reload
for p in 8080 8081 8082 8083;do systemctl start hermes@$p;systemctl enable hermes@$p;ufw allow $p/tcp;done

5. 资源占用核对（KVM4：4 核 16G）
Ollama：限 3 核、11G 内存 → Qwen-VL 常驻
OpenWebUI+Nginx：合计 < 1G
4 个 Hermes 实例：合计 2～3G
整机富余内存：1～2G，稳定富余不触发 Swap、无 OOM
配套运维命令
bash
运行
# 查看容器状态
docker compose ps
# 停止整套服务
docker compose down
# 实时日志
docker compose logs -f

需要我补充 TG 网关对接 4 个 Hermes 端口的分流配置吗？
快速
编程
超能模式
Beta
PPT 生成
AI 表格
图像生成
更多
