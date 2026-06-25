---
creation_date: 2026-06-07
source: "Perplexity"
tags:
  - ai/perplexity
status: inbox
---

# NAS-利用tailscale 在內地翻牆香港屋企的NAS ,達到翻牆到香港上網目的。

**Date:** 2026-06-07 23:08
**Source:** Perplexity

---

回答
連結
圖片
視頻
分享
下載 Comet
NAS:利用tailscale 在內地翻牆香港屋企的NAS ,達到翻牆到香港上網目的。
SYNOLOGY NAS + Tailscale VPN 內網穿透/翻牆免PORT設定 ...
TailScale实现异地组网、远程访问，点对点跑满你的带宽 ...
「Tailscale 内网穿透教程| 免费实现NAS 远程访问，简单安全 ...

可以，用 Tailscale 把你內地裝置的預設出口改成香港屋企 NAS，效果就等於「經香港上網」，而且同時可以順便回家存取 NAS 內網資源 。
ruohai
+1

你要的架構

做法是：

香港屋企的 NAS 先變成 Tailscale 的 Exit Node，即出口節點，所有流量都可經它出網 。
ivonblog
+1

內地手機或電腦也裝 Tailscale，連回同一個尾網後，指定香港 NAS 做出口 。
ruohai
+1

之後你的上網流量對外 IP 會顯示成香港住宅網路，而不是內地網路 。
ivonblog

NAS 端設定

如果你的 NAS 是 Linux / Synology 類型，核心概念是先啟用 IP forwarding，再把 NAS 宣告成出口節點 。
ruohai
+1

常見步驟是：

啟用 IP forwarding。

在 NAS 上啟用「宣告出口節點」。

到 Tailscale 管理頁面把這台 NAS 核准為 exit node 。
ivonblog
+1

有些教學也會同時設定 subnet route，讓你從外面直接連回家中 NAS 內網 IP，而不只是在外網上網 。
youtube
ruohai

內地裝置設定

內地那台裝置連上 Tailscale 後，選擇香港 NAS 作為出口節點即可，之後所有流量就會走香港屋企的網路出去 。
ruohai
+1

你可以用這個方式驗證：

連線前查一次外網 IP。

指定 exit node 後再查一次。

如果成功，顯示的就會是香港住宅 IP 。
ivonblog

你要留意的事

這個方案本質上是「遠端回家上網」，不是傳統商業 VPN；穩定性很大程度取決於香港家中上行頻寬、路由品質，以及內地網路環境 。
fast.v2ex
+1

另外，部分資料提到在中國使用 Tailscale 可能會受網路環境影響，連線未必一直穩定 。如果你要長期穩定使用，通常會把 NAS 之外再準備一台香港 VPS 當備援出口節點 。
blog.l3zc
+2

實用建議

如果你的目標是「內地裝置穩定獲得香港 IP」，我會建議這個順序：

先用香港 NAS 當 exit node 測試。

再確認家中上行是否足夠、延遲是否可接受。

若不穩，再加一台香港 VPS 做第二出口點 。
blog.l3zc
+1

如果你要，我可以直接幫你整理成一份「Synology NAS + Tailscale Exit Node」的中文設定清單。

10 個來源
DS223J
已完成 2 個步驟

Synology DS223j（Realtek RTD1619B 四核 ARM CPU，1GB RAM）可以裝 Tailscale 基本連線和存取 NAS，但因為是低階 J 系列 + ARM 架構，官方 Package Center 版本的 Tailscale Web UI 常出問題（例如 "page not found"），且不支援當 exit node。
tailscale
+2

DS223j 限制與解決方案

DS223j 的 Tailscale 只能當普通節點（用來遠端存取 NAS 檔案），不適合當 exit node。原因：

CPU / RAM 太弱，處理全流量會卡住（Gigabit 網卡但 CPU 瓶頸）。
reddit

官方 Synology Tailscale package 在 J 系列 ARM 上 Web 介面有 bug，且不支援 exit node 功能。
reddit
+3

Docker 版 Tailscale 也無法輕易當 exit node，需要手動改路由表，很麻煩。
reddit

推薦方案：在香港家裡另外加一台小機器當 exit node，DS223j 只負責檔案存取。

方案	優點	缺點	適合度
直接用 DS223j	不用買新硬體	Web UI bug + 無 exit node + 效能差	不推薦 
reddit
+1

DS223j 用 Docker Tailscale	繞過官方 package	仍無 exit node，需手動配置路由	勉強 
reddit

加 Raspberry Pi 4/5 或舊 PC	完美支援 exit node，效能足	需額外硬體（Pi 4 ~HK$400）	強烈推薦 
tailscale
+1
推薦設定：加一台 Exit Node 機
硬體選擇（香港買）

Raspberry Pi 4B/5 (4GB RAM)：最平最穩，裝 Raspberry Pi OS，支援 Tailscale exit node。家樂福/深水埗電子街有賣。

舊 Android 盒子 / mini PC：若有現成更好。

OpenWRT 路由器：如小米/TP-Link 支援 OpenWRT，直接在路由器裝 Tailscale 全家流量走香港 IP。

逐步指令（以 Raspberry Pi 為例）

假設你有 Pi 在香港家裡同一 LAN，跟 DS223j 一起。

在 Pi 上裝 Tailscale：

text
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

登入你帳號，確認在 Tailscale admin console 看到這台 Pi。
tailscale

設 Pi 為 Exit Node：

text
sudo tailscale set --advertise-exit-node

在 Tailscale 後台 (login.tailscale.com/admin/machines)，找到 Pi，點 Edit route settings > 啟用 "Use as exit node"。
tailscale
+1

在 DS223j 上裝 Tailscale（用來遠端存取 NAS）：

Package Center 搜 Tailscale，若裝不上，去 https://pkgs.tailscale.com/stable/ 下載 armv8 或 arm64 的 DSM7 spk 檔，手動安裝。
reddit
+1

登入後，SSH 進 DS223j 檢查狀態：sudo tailscale status。
reddit

可選：若想從內地直接用 Tailscale IP 訪問 DS223j 的 DSM / 檔案分享，加 subnet route：sudo tailscale set --advertise-routes=192.168.88.0/24（改成你 LAN 子網），後台批准。
lihaifeng

內地用：

Tailscale App 選 Pi 作為 exit node，全流量經香港 Pi 上網。

同時可存取 DS223j（用 Tailscale IP 或 subnet route）。
tailscale

這樣你達成長期「翻牆到香港上網」+「隨時存 NAS」的雙重目的，DS223j 只負輕任不會卡。

若你決定買 Pi 或有其他硬體，告訴我型號我再給精確指令！

19 個來源
在香港家中我有synology NAS , 我用tailscale 配合NAS am登入，請詳列步驟配合tailscale setup NAS as a server, 讓我在內地可以透過手機翻牆香港server 上網。
Setup Your Synology NAS As A Tailscale Exit Node
Setup Your Synology NAS As A Tailscale Subnet Router To ...
Complete Tailscale Guide - VPN without port forwarding on Synology NAS

DS223j 作為低階 NAS 不適合直接當 exit node（效能瓶頸 + 官方 Tailscale package 支援有限），建議用它只作檔案伺服器，搭配香港家中另一台常開機（如 Raspberry Pi）當 exit node。但如果你堅持用 NAS，下面詳列步驟先 setup NAS 基本 Tailscale 連線（可遠端存取），再試著設為 server/exit node（成功率低，預期會慢）。

前置準備

Tailscale 帳號（用 Google/MS 註冊，免費 100 裝置）。

在香港家中 LAN 內用電腦登入 DSM（內地先別試）。

DS223j DSM 7+，啟用 SSH（控制台 > 終端機 & SNMP > 啟用 SSH）。

步驟 1：香港家中安裝 Tailscale 到 DS223j

登入 DSM > 套件中心 > 搜尋 "Tailscale" > 安裝（若無官方版，下載 pkgs.tailscale.com/stable/ 的 arm64 DSM7 spk，手動上傳安裝）。
tailscale
+1

安裝後開啟 Tailscale app，跟隨畫面用 Google/MS 登入你的 tailnet（會跳轉瀏覽器授權）。

檢查狀態：SSH 進 NAS（ssh admin@NAS-IP），跑 sudo tailscale status，確認 "logged in" 且有 Tailscale IP（如 100.x.x.x）。

重啟 NAS 後若斷線，設 Task Scheduler（控制台 > 工作排程器 > 建立 > 使用者定義指令 > root 使用者 > 開機觸發）：

text
/var/packages/Tailscale/target/bin/tailscale up --accept-routes
synosystemctl restart pkgctl-Tailscale.service

儲存並立即執行。
hostbor
+1

NAS 現在可在 Tailscale admin console（login.tailscale.com/admin/machines）看到，內地手機裝 Tailscale App 登入同帳號，就能用 Tailscale IP 存取 DSM/檔案（如 smb://100.x.x.x）。

步驟 2：設 NAS 為 Server（Subnet Router，分享家中 LAN）

讓內地手機不只存 NAS，還能訪問家中其他裝置（如打印機）。

SSH 進 NAS：sudo tailscale up --advertise-routes=192.168.88.0/24 --accept-routes（改成你家中 LAN 子網，如 192.168.1.0/24）。

去 Tailscale admin console > Machines > 找 NAS > Edit route settings > 批准 subnet route（勾選）。

內地手機 Tailscale App 開啟 "Allow local network access"，就能訪問家中 LAN。
tailscale

步驟 3：設 NAS 為 Exit Node（翻牆上網，風險最高）

DS223j ARM CPU 弱，預期全流量會卡（<50Mbps），但可試：

SSH 進 NAS：sudo tailscale set --advertise-exit-node（或重跑 sudo tailscale up --advertise-exit-node）。

Tailscale admin console > Machines > NAS > Edit route settings > 勾選 "Use as exit node" + 批准。

內地手機端：

安裝 Tailscale iOS/Android App，登入同帳號，連線。

App 設定 > Exit Node > 選你的 NAS > 啟用 "Use exit node"。

全流量現在經香港 NAS 出網，你的公網 IP 變香港寬頻 IP，等於翻牆到香港上網。
tailscale

檢查：內地手機瀏覽 whatismyipaddress.com，IP 應顯示香港。

內地手機完整使用流程

Tailscale App 連線 > 選 NAS 作 exit node。

瀏覽器/Google/YouTube 等全走香港 IP（翻牆成功）。

存取 NAS：用 Tailscale IP 開 DSM（https://100.x.x.x:5001）或 File Station。

若想切回內地直連：App 停用 exit node。

注意與故障排除

效能：DS223j 當 exit node 易過熱/斷線，建議加風扇或換 Pi 4（HK$400）。

斷線：內地 GFW 可能擋 Tailscale UDP，重試或用 Tailscale Funnel（admin console 試開）。

存取 DSM：Tailscale IP + :5000/5001，HTTPS 需信任自簽證書。

若失敗：Docker 裝 Tailscale（DSM > Docker > 下載 tailscale/tailscale 映像），但 exit node 仍需 iptables 手動設路由，複雜不薦。

風險自負，內地政策變動大。

成功後內地手機即達 "翻牆香港上網 + 隨時用 NAS" 目的。若卡步驟，貼錯誤訊息我再 debug！
hostbor
+2

12 個來源
後續問題
如何設定Tailscale exit node讓內地手機路由香港流量
Tailscale手機端如何連接到NAS並翻牆
Synology NAS Tailscale常見問題與故障排除
Pro
免费预览次数已用完。现在使用基础搜索。
升级




詢問後續問題
搜尋
模型
