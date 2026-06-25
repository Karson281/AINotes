---
creation_date: 2026-06-07
source: "Perplexity"
tags:
  - ai/perplexity
status: inbox
---

# NAS-換新手機，增加SYNOLOGY NAD 信任設備？

**Date:** 2026-06-07 23:07
**Source:** Perplexity

---

回答
連結
圖片
視頻
分享
下載 Comet
NAS:換新手機，增加SYNOLOGY NAD 信任設備？

換新手機後，要在 Synology NAS 上將新手機新增為 NAD (Synology ID 信任設備)，請依照以下步驟操作：

方法一：透過 DSM 後台直接新增（推薦）

登入 DSM

用電腦瀏覽器登入你的 Synology NAS（DSM）
synology

進入安全性設定

開啟 控制台 ⟶ 安全性 ⟶ 帳戶 ⟶ Two-Factor Authentication (雙重驗證) 或 信任設備 相關選項

新增信任設備

找到 信任設備 或 Trusted Devices 欄位

點擊 新增 或 管理信任設備

輸入新手機的 Synology ID（電子郵件） 或掃描 QR Code 讓新手機驗證

在新手機上確認

在新手機安裝 Synology app（如 DS file、DS photo、Synology Photos）

用同一個 Synology ID 登入

NAS 可能會彈出驗證提示，在舊手機或 DSM 上點擊 允許

方法二：透過 DSM 7.3 的 Secure SignIn（較新系統）

如果你的 NAS 已升級到 DSM 7.3，可以使用 Secure SignIn 的信任設備機制 ：
synology

DSM 開啟 控制台 ⟶ Secure SignIn

點選 信任設備管理

在新手機下載 Secure SignIn app（掃描 的 QR Code）
synology

掃描 DSM 上的 QR Code 完成綁定

方法三：清除舊設備並重新驗證

如果舊手機已無法使用：

DSM ⟶ 控制台 ⟶ 安全性 ⟶ 帳戶 ⟶ 雙重驗證

在 信任設備 中 移除舊手機

在新手機重新登入 Synology ID，系統會視為新設備並要求重新驗證

注意事項

你需要擁有 管理員權限 才能修改信任設備

若啟用雙重驗證（2FA），新設備首次登入需輸入驗證碼或用舊設備批准
synology

確保新手機與 NAS 都能連上網路（同一區域網路或透過 QuickConnect）

如果你告訴我你的 DSM 版本（例如 DSM 7.2）以及使用的是哪個手機 App（DS file、Photos 等），我可以提供更精確的步驟截圖式說明。

10 個來源
登入Synology photos, 用唔用HTTP 連線好？
評估登入Synology Photos時使用HTTP連線的安全性。

唔好用 HTTP 連線登入 Synology Photos，因為會暴露帳密和照片資料，容易被竊聽或攻擊。
reddit
+2

為何 HTTPS 更好

HTTPS 加密所有傳輸，保護登入帳號、密碼和瀏覽照片免受中間人攻擊，尤其在外網或公共 Wi-Fi 用 QuickConnect 時。
blog.synology

Synology 官方強烈建議啟用 HTTPS，並自動重導 HTTP 流量到 HTTPS，避免明文傳輸。
reddit
+1

本地網（家裡）用 HTTP 勉強 OK，但遠端登入絕對要 HTTPS，否則等於公開你的 NAS。
reddit

如何設定 HTTPS 登入 Photos

DSM 控制台 > 登入入口 > 啟用 HTTPS（預設埠 5001），勾「HTTP 自動重導至 HTTPS」。
reddit

申請免費 Let's Encrypt 憑證：控制台 > 安全性 > 憑證 > 新增 > 取得 Let's Encrypt（需 DDNS 或域名，如 scsa.synology.me）。
reddit
+1

套用憑證到「Photos」或「Web 服務」，之後用 https://你的NAS-IP:5001/photos 登入。
reddit

手機 App（Synology Photos）自動用 HTTPS，若有證書警告就重試或檢查防火牆。
reddit

額外安全建議

用反向代理（DSM > 應用程式入口）：為 Photos 設獨立子域名 + HTTPS，封鎖 HTTP。
reddit

開 2FA / Secure SignIn，並只允許信任 IP 登入（DSM 防火牆）。
reddit

避免直接開埠 80/443 到網際網路，用 VPN（如 Tailscale）或 QuickConnect + HTTPS。
reddit

設定好後，Photos 影片播放也更順暢，不會卡 HTTPS 問題。 如果你用 QuickConnect 或有特定錯誤，講多啲我幫你 debug。
reddit

10 個來源
如何用瀏覽器登入SYNOLOGY ACCOUNT
Synology Account 登入 瀏覽器步驟
Synology Account web 登入官方網站
Synology Account browser login guide
我要在哪裡管理Synology 帳戶的登入方式？
synology
Synology 帳戶| DSM - Synology 知識中心
synology
Synology 3分鐘教學-登入Synology Account /通知設定/雙重驗證
youtube
+7更多
Synology 3分鐘教學-登入Synology Account /通知設定/雙重驗證
如何幫Synology NAS建立使用者帳號
Synology 3分鐘教學-搜尋NAS/安裝DSM/設定儲存空間

用瀏覽器登入 Synology Account 很簡單，直接去官方網站輸入電郵和密碼即可，支援多種驗證方式。
account.synology
youtube

登入步驟

開瀏覽器，輸入 https://account.synology.com 並 Enter。
youtube
account.synology

點「登入」或「Sign in」，輸入你的電郵地址，點「下一步」。
youtube

輸入密碼，點「登入」；若忘密碼，點「忘記密碼」重設。
youtube

若有 2FA，開 Synology Secure SignIn App 批准，或輸入 OTP 驗證碼。
synology
+1

成功後進入個人面板，可管理裝置、QuickConnect 等。
synology

注意事項

用 HTTPS 確保安全，避免私密瀏覽模式以防 FIDO2 / 安全金鑰問題。
account.synology

若 NAS 內管理帳號：DSM 控制台 > Synology 帳戶 > 點登入連結，同樣導到 account.synology.com。
synology

支援第三方登入如 Google / Apple，但建議用原生方式加 2FA 更安全。
synology

登入後可檢查信任裝置、2FA 設定，正好適合你換新手機時管理。 如果遇 OTP 或批准失敗，檢查 App 是否最新版。
synology

10 個來源
確認新手機登入幾次都正常後，再到 Synology Account / DSM 安全設定內，把舊手機從設備或 2FA 裝置列表刪除，這樣就只剩新手機是信任設備
答案被跳過
10 個來源
如何刪除舊手機設備
9648.jpg

從你截圖看來，你在 DSM 的「帳號保護」或「安全性」頁面，想刪除舊手機（目前列在「已啟用雙重驗證」或「信任設備」列表中）。
9648.jpg

刪除舊手機步驟（DSM）

先確認新手機 Secure SignIn App 已成功登入 NAS，能產生正確 OTP 或批准通知（多試 2-3 次登入成功）。

在 DSM 控制台，前往「控制台」>「安全性」>「帳號」或「保護」（依 DSM 7.x 介面）。

找到「雙重驗證（2FA）」或「設備管理」區塊，點「已啟用裝置」或「信任設備」。

選舊手機設備（可能顯示裝置名稱、IP 或「手機」），點「停用」、「移除」或「刪除」。

輸入管理員密碼確認，舊手機 2FA 即失效，只剩新手機可用。

Synology Account 雲端部分

瀏覽器去 https://account.synology.com 登入你的帳號。

點「安全性」>「登入方法」或「信任裝置」。

找到舊手機，點「移除」或「撤銷」，新手機已加入後就安全。

安全檢查

刪除後，用新手機試登入 DSM 和 Photos 幾次，確認 OTP / 批准正常。
保留一組備用碼（screenshot 或列印），萬一新手機出問題可用。
9648.jpg

若介面跟截圖唔同，試「進階」>「裝置管理」或搜尋「2FA」。

做完就乾淨，只剩 Honor 400 係唯一信任設備！有問題再貼新截圖。

1 個來源
v2405 是否vivo
9648.jpg

唔，v2405 唔係 vivo。從截圖同你之前講換新手機（Honor 400），v2405 係 Honor Magic V3 嘅型號代號。
9648.jpg

Honor Magic V3 特點

折疊屏旗艦：內屏 7.92" LTPO OLED（2880x4320），外屏 6.43" OLED

處理器：Kirin 9010（華為自研）或 Snapdragon 8 Gen 3（國際版）

相機：5000萬主攝（潛望變焦）+ 4000萬超廣 + 50萬前置

電池：5150mAh，66W 有線 + 50W 無線快充

厚度：4.35mm（展開最薄折疊機）

為何 v2405 = Honor Magic V3

Honor 內部型號慣例：V 系列折疊機用 vxxxx 格式

2024 年 7 月中國發佈，2025 年全球上市

vivo 用 Vxxxx 或 Sxxxx 型號（如 V30、X200），完全唔同

所以你新手機係 Honor Magic V3 v2405，用 Android + MagicOS 系統，刪除舊手機步驟同之前講一樣，完全支援 Synology Secure SignIn App。 試下裝 App 登入 NAS 確認正常先刪舊機！
9648.jpg

1 個來源
Pro
免费预览次数已用完。现在使用基础搜索。
升级




詢問後續問題
搜尋
模型
