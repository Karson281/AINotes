---
creation_date: 2026-06-08
source: "Copilot"
tags:
  - ai/copilot
status: inbox
---

# Agent-hermes agent 手機教學

**Date:** 2026-06-08 00:23
**Source:** Copilot

---

Invite
Friday, May 29
You said
Copied
hermes agent 手機教學
Copilot said

Hermes Agent 可以在手機上安裝並使用，最常見的方法是透過 Android 的 Termux 終端模擬器。這樣你就能直接在手機上運行 Hermes 的核心功能，包括持久記憶、技能管理和排程任務。
什么值得买

📱 手機安裝 Hermes Agent 教學（Android）
1. 環境準備

安裝 Termux（或 ZeroTermux 等替代品）

存儲空間需求：約 3GB

安裝時間：大約 1 小時

網路代理工具：建議準備，避免下載超時
什么值得买

2. 安裝步驟

更新系統並安裝依賴

Bash
Copy
pkg update && pkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ffmpeg


Python：提供執行環境

clang/rust：編譯依賴

ffmpeg：媒體處理
什么值得买

克隆專案

Bash
Copy
git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git
cd hermes-agent


建立虛擬環境

Bash
Copy
python -m venv venv
source venv/bin/activate
export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"


安裝 Termux 兼容組件

Bash
Copy
python -m pip install -e '.[termux]' -c constraints-termux.txt


建立全局命令連結

Bash
Copy
ln -sf "$PWD/venv/bin/hermes" "$PREFIX/bin/hermes"

⚙️ 初始化與設定

檢查環境：hermes doctor

配置模型供應商：hermes setup 或 hermes model

支援平台串接：Telegram、Discord，可直接用手機訊息控制 Hermes
軟體玩家
+1

📊 功能限制（手機端）

支援：CLI 交互、MCP 協議、記憶管理、排程任務

不支援：Docker、語音轉寫、瀏覽器自動化（因 Android 環境限制）
什么值得买

🚨 常見問題排查

缺少 ANDROID_API_LEVEL → 執行 export ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"

ripgrep 或 Node 缺失 → pkg install ripgrep nodejs

Python 包編譯失敗 → 安裝完整工具鏈：pkg install clang rust make pkg-config libffi openssl
什么值得买

✅ 總結：在 Android 手機上安裝 Hermes Agent 的最佳方式是透過 Termux，雖然功能比桌面端少，但仍能提供持久記憶、技能管理和排程自動化。如果你主要想用手機隨時呼叫 Hermes（例如透過 Telegram），這套流程就能滿足需求。

要不要我幫你整理一份 「快速安裝指令清單」，方便你直接複製貼上？

什么值得买

Hermes 官方教程！在安卓手机上安装 Hermes Agent

軟體玩家

AI 助理會「自我進化」！Hermes Agent 完整教學：安裝、設定、連接 Telegram，讓 AI 越用越聰明

Show all
Edit in a page
Message Copilot
Smart
