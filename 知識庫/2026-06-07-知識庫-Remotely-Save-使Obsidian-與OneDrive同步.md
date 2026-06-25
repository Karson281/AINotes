---
creation_date: 2026-06-07
source: "Perplexity"
tags:
  - ai/perplexity
status: inbox
---

# 知識庫-Remotely Save 使Obsidian 與OneDrive同步

**Date:** 2026-06-07 23:08
**Source:** Perplexity

---

回答
連結
圖片
分享
下載 Comet
知識庫：Remotely Save 使Obsidian 與OneDrive同步

Remotely Save 是 Obsidian 的免費社群插件，能讓你的筆記庫（Vault）透過 OneDrive 個人版在多設備間同步（Mac、Windows、iPhone、Android 等）。
21obsidian
+1

快速設定步驟
步驟	操作內容
1. 準備 OneDrive 帳號	準備一個 OneDrive 個人版帳號（微軟帳號），登入地址：https://onedrive.live.com/login 
21obsidian
+1

2. 安裝插件	每台設備的 Obsidian 都要：
- 設定 → 第三方插件 → 關閉安全模式
- 社區瀏覽 → 搜尋「Remotely Save」→ 安裝並啟用 
sspai

3. 選擇服務並授權	- 進入 Remotely Save 設定
- 「選擇遠端服務」選 OneDrive（個人版）
- 點擊「鑑權」→ 複製連結到瀏覽器 → 登入微軟帳號 → 點擊「接受」授權 
21obsidian
+1

4. 首次同步	- 連接成功後，OneDrive 的「應用」資料夾會出現 remotely-save 資料夾
- 在 Obsidian 手動點擊同步按鈕，上傳當前 Vault 到 OneDrive 
21obsidian
+1

5. 其他設備同步	新設備：
① 建立空資料夾 → 用 Obsidian 打開
② 安裝 Remotely Save → 選 OneDrive 個人版 → 用同一帳號授權
③ 手動同步，把 OneDrive 內容拉回本地 
21obsidian
+1
自動同步設定

在插件設定中可選擇自動同步頻率：

啟動後 30 秒自動同步

每 1 分鐘 / 每 10 分鐘 / 每 30 分鐘同步一次
reddit
+1

注意事項

同步對象是整個 Vault，不是單篇筆記
21obsidian

開始前建議備份原有倉庫，避免操作不當導致資料丟失
sspai

支援同步 .obsidian 配置文件（需在設定中開啟「同步配置資料夾」）
forum-zh.obsidian

OneDrive 個人版提供 5GB 儲存空間，比 Dropbox 的 2GB 更適合
reddit

這方案免費且跨平台，適合不想付費買 Obsidian Sync 的使用者 。
blog.csdn

10 個來源
obsidian 可同步至筆記等電腦或onedrive?

是的，Obsidian 可以同步到筆記型電腦或其他電腦，也能用 OneDrive 同步，但需要設定同步方式（Obsidian 本身不直接自動同步）。

主要同步方案對照表
方案	適用平台	是否免費	設定方式
官方 Obsidian Sync	全平台（Windows/Mac/iOS/Android/Linux）	❌ 付費（$5–10/月）
sspai
youtube
	內建功能，開關即用 
reddit

OneDrive + Remotely Save 插件	Windows/Mac/Android/iOS	✅ 免費（需 OneDrive 帳號）
sspai
+1
	安裝 Remotely Save 插件，授權 OneDrive 後同步 
sspai

OneDrive 直接同步（資料夾放 OneDrive）	Windows/Mac（桌面版）	✅ 免費	將 Vault 直接放在 OneDrive 資料夾內 
reddit
youtube

iCloud	Apple 生態系（Mac/iOS/iPad）	✅ 免費	Vault 放在 iCloud Drive 
reddit
youtube

其他雲端	全平台	✅ 免費	Google Drive、Dropbox、坚果雲等 
reddit
youtube
OneDrive 同步的兩種方式：

Remotely Save 插件（推薦）

安裝 Remotely Save 社區插件

選擇 OneDrive 個人版並授權

點擊同步按鈕即可自動同步
sspai
+1

優點：不需安裝 OneDrive 同步客戶端，跨平台支援好

直接將 Vault 放入 OneDrive 資料夾

Windows：把 Vault 資料夾放到 OneDrive\Documents

桌面版自動同步
youtube
reddit

注意：手機版不建議直接這樣用，可能有同步問題
reddit

總結：

✅ 筆記型電腦與其他電腦：完全可以同步，用 OneDrive/iCloud/Remotely Save 等

✅ OneDrive 可以同步：推薦用 Remotely Save 插件，免費且跨平台穩定
21obsidian
+1

⚠️ 手機版：建議用 Remotely Save 或官方 Obsidian Sync，避免直接用 OneDrive 資料夾
reddit

11 個來源
remotely save 有向重要？
已完成 2 個步驟

Remotely Save 很重要，但僅限於想免費同步 Obsidian 筆記的用戶；如果你願意付費或只在單一設備使用，則不需要。

Remotely Save 的重要性分析
情況	是否需要 Remotely Save	原因
想免費跨平台同步（手機+電腦）	✅ 非常重要 
sspai
+1
	官方 Sync 月費 $5–10 太貴，Remotely Save 免費支援 OneDrive/Dropbox/S3/WebDAV 
blog.csdn
+1

只用桌面版（不需同步）	❌ 不需要	單機使用即可，無需同步插件
只用 Apple 生態系（Mac+iOS）	❌ 可選	iCloud 已內建自動同步，無需插件 
youtube

願意付費買官方 Sync	❌ 不需要	官方 Sync 更穩定、簡便，但需月費 
blog.csdn

有技術能力自建 OSS/WebDAV	✅ 推薦使用 
cnblogs
	配合阿里云 OSS/腾讯云 COS，每年約 25 元內，比 iCloud 穩定快速 
forum-zh.obsidian
+1
Remotely Save 的核心優勢
blog.csdn
+1

✅ 完全免費（基本功能）

✅ 支援 OneDrive、Dropbox、S3、WebDAV 等多種雲端

✅ 跨平台（Windows/Mac/Android/iOS 全支援）

✅ 端到端加密保護隱私
blog.csdn

✅ 開源、更新勤快
linux

風險與缺點（需注意）
缺點	說明
⚠️ 同步衝突	偶有衝突問題，建議定期備份 
linux
+1

⚠️ 大文件同步慢	>8M 文件可能卡住，建議移到不同步資料夾 
forum-zh.obsidian

⚠️ 設定繁瑣	需手動授權雲端、填入金鑰，對新手較複雜 
linux

⚠️ 不小心清空筆記	若同步空庫會快速清空所有筆記，需謹慎操作 
linux
總結：

如果你需要免費跨平台同步（尤其手機+電腦），Remotely Save 是非常重要的核心工具，幾乎是最佳免費方案
sspai
+1

搭配 OneDrive 或自建 OSS，整合效果好，適合大多數用戶
cnblogs
+1

但建議先備份筆記庫，測試穩定後再同步重要資料
pkmer
+1

11 個來源
remotely saved 係乜嘢插件？

Remotely Save 係 Obsidian 嘅一個非官方社區插件，主要功能係幫你將筆記同步到雲端储存服務，實現多設備（電腦、手機、平板）之間嘅同步 。
cnblogs
+2

核心功能
功能	說明
雲端同步	支援 OneDrive、Dropbox、Amazon S3、阿里云 OSS、七牛雲、WebDAV 等多種云服务 
cnblogs
+1

跨平台	Windows、Mac、Android、iOS、Linux 全部支援 
bilibili
+1

完全免費	基本同步功能免費，可有付費進階功能（智能衝突處理）
blog.csdn
+1

多語言支援	包含繁體中文、簡體中文、英文等多種語言 
blog.csdn
點樣用？

安裝插件：Obsidian 設定 → 社區插件市場 → 搜尋 Remotely Save → 安裝並啟用
bilibili
+1

選擇云服务：喺插件設定嗰度揀用什么云（例如 OneDrive personal）
forum-zh.obsidian

授權認證：點擊 Auth 連結，登入云帳號並授權
forum-zh.obsidian

點擊同步：按側邊欄同步按鈕，筆記就會上傳/下載
cnblogs
+1

邊個需要？

✅ 需要免費跨平台同步（尤其手機 + 電腦）嘅用戶

✅ 唔想買官方 Obsidian Sync（月費 $5–10）

✅ 有 OneDrive、Dropbox 或自建 OSS 儲存空間

注意：

係第三方插件，唔係官方開發
github
+1

建議定期備份，避免同步衝突導致資料丟失
linux

11 個來源
哪裡下載？

Remotely Save 有 2 種下載方式：

1️⃣ 最簡單：直接在 Obsidian 內安裝（推薦）
blog.csdn

打開 Obsidian

進入 設定 → 社區插件 → 瀏覽

搜尋框輸入 Remotely Save

點擊 安裝 → 启用

有時因為網絡問題需稍等片刻先見到插件
blog.csdn

2️⃣ 手動安裝（當官方安裝失敗時）
blog.csdn
+2

下載來源：

GitHub Releases（官方）：https://github.com/remotely-save/remotely-save/releases
github

官方網站：https://remotelysave.com
github

安裝步驟：

下載最新版本的 remotely-save-*.zip 壓縮包
blog.csdn

找到你嘅 Obsidian 儲存庫資料夾

進入 .obsidian/plugins/ 資料夾（如果無 plugins 就新建一個）
blog.csdn
+1

將下載嘅插件解壓到 plugins 資料夾內

重啟 Obsidian 即可見到插件
blog.csdn

手機版安裝（Android/iOS）
bilibili

手機版通常無法直接登入第三方插件市場

建議用手動安裝方式，將插件文件複製到手機儲存庫嘅 .obsidian/plugins/ 資料夾
bilibili

或借用電腦安裝後同步過去

提示：安裝後需喺插件設定嗰度授權雲端服務（OneDrive/Dropbox 等）先可以同步 。
forum-zh.obsidian

12 個來源
後續問題
如何在 Remotely Save 中綁定 OneDrive 帳戶
安裝後同步失敗該如何排查網絡錯誤
Remotely Save 支援哪些 WebDAV 服務供應商
Pro
免费预览次数已用完。现在使用基础搜索。
升级




詢問後續問題
搜尋
模型
