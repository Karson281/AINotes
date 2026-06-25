---
creation_date: 2026-06-07
source: "豆包"
tags:
  - topic/untagged
status: inbox
---

# 建站-Hostinger VPS開源網站與AI環境整合部署方案 - 豆包

**Date:** 2026-06-07 03:25
**Source:** 豆包

---

建站：Hostinger VPS開源網站與AI環境整合部署方案
内容由豆包 AI 生成，请仔细甄别
Hostinger VPS【全免費開源網站】5套可靠方案（軟件永久免費、淨用你現有KVM4伺服器，唔使額外買主機）
 
全部源碼免費、無授權費、Docker兼容、可同Ollama/Hermes一齊共存，沿用之前docker-compose架構，Nginx統一反向代理綁域名
 
 
 
1、WordPress（最穩、首選｜博客/官網/小商城）
 
✅ 100%開源永久免費，全球4成網站在用，插件/主題海量免費
 
- Docker一鍵塞入你現有 docker-compose.yml ，同Ollama共用Nginx
 
- 域名：site.xxx.com，免費Let’s Encrypt SSL自動證書
 
- 適用：個人博客、產品官網、小型資訊站
 
yaml
  
wordpress:
  image: wordpress:latest
  depends_on:
    - wpdb
  volumes:
    - ./wp-data:/var/www/html
  environment:
    WORDPRESS_DB_HOST: wpdb:3306
    WORDPRESS_DB_NAME: wpdb
    WORDPRESS_DB_USER: wpuser
    WORDPRESS_DB_PASSWORD: wp123
wpdb:
  image: mariadb:10.11
  volumes:
    - ./wp-mysql:/var/lib/mysql
  environment:
    MYSQL_ROOT_PASSWORD: root123
    MYSQL_DATABASE: wpdb
    MYSQL_USER: wpuser
    MYSQL_PASSWORD: wp123
 
 
2、Halo（國產中文免費CMS｜輕量博客）
 
全中文後台、國人開源免費、佔資源細（512M RAM就得），適合技術日誌、個人站
 
- 域名：blog.xxx.com，Nginx反向代理
 
- 優點：體積細、更新快、無垃圾付費綁定
 
3、Nextcloud（免費私有雲盤｜文件分享網站）
 
完全開源免費，自建私人雲盤、團隊文件管理，替代百度雲
 
- 域名：cloud.xxx.com，存檔放VPS硬碟，數據唔外流
 
4、Coolify/Dokploy（免費伺服器面板｜一鍵裝所有網站）
 
 
 
全開源永久免費Web面板，裝完後網頁點擊一鍵部署WP/Halo/靜態網站，自動配SSL、反向代理
Hostinger原生支援Dokploy一鍵系統模板，裝完不用手動配Nginx
 
好處：後續加任何網站唔改yml，網頁操作
 
5、Hexo/Hugo（靜態免費網站｜極速博客）
 
無數據庫、超省資源，生成純靜態HTML，開源永久免費，訪問速度極快
 
重點：同你AI堆（Ollama+Hermes+OpenWebUI）共存規劃
 
你KVM4（4C16G）資源分配：
 
- Ollama：2C11G（維持Qwen本地運行）
 
- 網站全套：1.5C~2C、3~4G RAM（WP+Halo+Nextcloud一齊跑都綽綽有餘）
 
- Nginx統一管理：chat/agent/site/blog/cloud 五個子域名分流
 
額外免費福利
 
SSL證書：Let’s Encrypt永久免費HTTPS，Nginx一鍵申請
 
軟件全部零授權費，淨支出只有域名年需要我直接幫你整合入現有docker-compose.yml，一次起全AI+網站全套嗎？
整合部署總結與優化建議
整套 5 套開源站點 + Ollama/Hermes/OpenWebUI AI 環境可完全合併到同一個 docker-compose.yml，共用 Nginx 反向代理、共用 Let’s Encrypt 免費 SSL，依托 4C16G KVM4 伺服器資源分配合理，無需新增伺服器、無任何軟體授權費。
一、資源校核（4C16G）
Ollama：2C 11G（Qwen 大模型常駐）
五套網站打包：1.5～2C、3～4G
Nginx + 系統佔用剩餘資源，總資源不溢出、可平穩並行運行
備註：Nextcloud 存儲直接掛載本機 VPS 硬碟，僅耗存儲空間、不額外佔內存
二、各站點對應子域名規劃（Nginx 統一反向代理）
表格
項目	綁定子域名	類型
OpenWebUI (AI 對話)	
chat.xxx.com
File
	AI 服務
Hermes Agent	
agent.xxx.com
File
	AI 代理
WordPress 官網 / 商城	
site.xxx.com
File
	動態 CMS
Halo 技術博客	
blog.xxx.com
File
	輕量 CMS
Nextcloud 私有雲盤	
cloud.xxx.com
File
	雲盤系統
Coolify/Dokploy 面板	
panel.xxx.com
File
	後續一鍵部署管理
Hexo/Hugo 靜態站	
static.xxx.com
File
	純靜態
三、部署兩種方案選擇
方案 1：直接合併單一 docker-compose.yml（推薦）
我可以幫你：
把原有 Ollama+OpenWebUI+Hermes 配置 + WP+Halo+Nextcloud+Dokploy 容器全部寫入同一 yml
新增統一 Nginx 容器，配置各域名反向代理規則
整合 acme.sh/letsencrypt 自動續簽 SSL 證書配置
統一數據卷掛載路徑（所有數據、資料庫、網站文件隔離存本地，方便備份）
啟動指令：docker compose up -d 一次性拉起全部服務
方案 2：Dokploy 面板託管部署（後續易維護）
先部署 Dokploy 到
panel.xxx.com
File
，後續在面板網頁圖形化一鍵安裝 WP/Halo/Nextcloud/Hexo，無需手動改 yml、自動配置 SSL 與反向代理，適合後續頻繁新增網站。
四、關於 Hexo/Hugo 補充說明
Hexo/Hugo 為本地生成靜態 HTML，不需要常駐容器跑數據庫與後台：
本地寫文章→生成靜態文件→掛載至 Nginx 對應目錄綁定
static.xxx.com
File
幾乎不佔伺服器 CPU / 內存，資源零消耗
五、需要你補充 3 項資訊即可開始整合 yml
你的主域名：xxx.com 具體域名
現有 Ollama/OpenWebUI 原 docker-compose 存放路徑
數據存儲掛載目錄偏好（如/data/xxx/統一存所有數據）
確認後我直接輸出完整版合併 docker-compose.yml 配置檔。
免費域名 + Hostinger VPS 對接方案（分兩類：完全免費二級域｜低成本頂級域）
 
一、免費可靠域名（唔使畀錢，直接綁你VPS IP）
 
1. Freenom（.tk/.ml/.ga/.cf/.gq）
 
✅ 免費1年續期，最平入門，缺點：域名隨機、少少廣告風險，適合測試：
 chat.xxx.tk 、 agent.xxx.tk 、 blog.xxx.tk 
⚠️ 不建議長期正式站
 
2. DuckDNS（超推、完全免費、穩定無廣告）
 
格式： xxx.duckdns.org ，免費永久，可自訂子域名
 
- 例： myai.duckdns.org 、 chat-my.duckdns.org 
 
- 綁定：填寫你Hostinger VPS公網IP就得，DNS秒生效
 
最適合你：chat/agent/site三個子域名一齊用
 
3. No-IP
 
免費二級域 xxx.no-ip.org，每個月登入續免費，穩定。
 
二、平價實用頂級域名（正式使用，年費幾十港幣）
 
 .xyz/.site/.online ，各大域名商首年$5～$15 HKD，正式長期建站、AI網站首選。
 
三、域名綁VPS步驟（好簡單）
 
註冊免費域名 → DNS管理新增A紀錄
 
A紀錄值 = 你Hostinger KVM4嘅公網IP
 
Nginx配置改用呢個域名：
 
nginx
  
server_name chat.xxx.duckdns.org;
 
 
Certbot 免費申請SSL，全網站HTTPS
 
四、對應你而家架構規劃（一套域名分3個子站）
 
- chat.xxx.duckdns.org → OpenWebUI AI對話
 
- agent.xxx.duckdns.org → Hermes Agent後台
 
- blog.xxx.duckdns.org → WordPress網站
DuckDNS 免費域名 + Hostinger VPS 整套落地部署方案（優先選 DuckDNS，永久免費無廣告、最适配你 4C16G AI + 建站環境）
一、域名選型定案（優先 DuckDNS，捨棄 Freenom）
1. 最優方案：DuckDNS 永久免費二級域名
自定義前綴（例：kv4-ai），主域固定.duckdns.org整套站點規劃：
chat.kv4-ai.duckdns.org → OpenWebUI（Ollama 對話前台）
agent.kv4-ai.duckdns.org → Hermes Agent 後端面板
site.kv4-ai.duckdns.org → WordPress 官網 / 小商城
blog.kv4-ai.duckdns.org → Halo 輕量博客
cloud.kv4-ai.duckdns.org → Nextcloud 私有雲盤
panel.kv4-ai.duckdns.org → Dokploy 伺服器管理面板
✅ 優勢：永久免費、無彈窗廣告、DNS 解析穩定、支持批量新增 A 記錄綁同一 VPS 公網 IP，Let’s Encrypt SSL 完美簽發證書。⚠️ Freenom (.tk/.ml 等) 域名運營不穩、隨機回收域名、隱藏廣告，只用於臨時測試，正式 AI + 建站直接不用；No-IP 需每月手動續簽免費，維護麻煩作備選。
2. 長期正式方案：低成本頂級域
後續需要商業化再入 .xyz/.site/.online，首年約 5~15 港幣 / 年，後續續費也偏低，適合長期運營正式網站。
二、DNS 綁定 Hostinger VPS 操作步驟
進入
DuckDNS 官網
File
，登錄後輸入自定義前綴（如 kv4-ai）創建域名；
在 DNS 頁 A 記錄填入Hostinger KVM4 VPS 公網 IP，保存，DNS 一般 1~5 分鐘生效；
可開啟 DuckDNS 動態 IP 更新腳本（Hostinger 固定公網 IP 可省略），防止 IP 變動導致域名失效。
三、Docker+Nginx+SSL 整合部署邏輯（沿用你原有 docker-compose 架構）
架構設計
統一 Nginx 容器做反向代理 + SSL，Certbot 自動申請 & 續期 Let’s Encrypt 免費 SSL 證書，全站強制 HTTPS；
Ollama、OpenWebUI、Hermes、WordPress、Halo、Nextcloud、Dokploy 全部容器納入同一docker-compose.yml，依賴隔離、數據卷本地掛載；
資源沿用原有分配：Ollama 2C11G，全套網站服務 1.5~2C/3~4G 內存，剩餘資源留系統與 Nginx，4C16G 資源冗余充足。
Nginx 配置範例片段（chat 節點示例，其他域名格式統一替換 server_name）
nginx
server {
    listen 80;
    server_name chat.kv4-ai.duckdns.org;
    # HTTP自動跳轉HTTPS+Certbot域名驗證
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name chat.kv4-ai.duckdns.org;
    ssl_certificate /etc/letsencrypt/live/chat.kv4-ai.duckdns.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/chat.kv4-ai.duckdns.org/privkey.pem;
    # 反向代理指向OpenWebUI容器內部端口
    location / {
        proxy_pass http://openwebui:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

agent/site/blog/cloud/panel 域名只替換server_name與對應容器內網地址即可。
四、兩種部署執行選擇
方案 A：手動整合 yml（現有 Ollama 環境不動，一次性合併所有服務）
提供三項資訊即可生成完整docker-compose.yml：
自定義 DuckDNS 前綴（自訂想要的名字）；
Hostinger VPS 公網 IP；
本地數據存放根目錄（例：/data/vps-data/統一存所有網站、資料庫、AI 數據）。
部署指令：docker compose up -d 一鍵啟動全部 AI + 網站，Certbot 容器定時自動續簽 SSL 證書。
方案 B：先裝 Dokploy (
panel.xxx.duckdns.org
File
) 圖形面板
先單獨部署 Dokploy 到面板域名，面板自動配置 DNS、SSL、反向代理；
後續網站 / AI 服務在網頁後台一鍵部署，無需手動修改 Nginx 與 yml，日後新增站點零配置門檻，適合新手長期維護。
五、Hexo/Hugo 靜態站補充部署
無需常駐容器，本地生成靜態 HTML 文件，掛載至 Nginx 本地目錄，綁定static.kv4-ai.duckdns.org，不佔用伺服器 CPU 內存。
六、後續維護優點
域名終身免費（DuckDNS），僅後續換頂級域才產生域名費用，軟件全開源零授權費；
SSL 證書免費自動續簽，無證書到期中斷網站風險；
統一 Nginx 管理所有子域名，後續新增網站只需要新增一條 Nginx 配置。
需要我直接按你自定的 DuckDNS 前綴，輸出完整版整合 docker-compose.yml 嗎？
快速
编程
超能模式
Beta
PPT 生成
AI 表格
图像生成
更多
