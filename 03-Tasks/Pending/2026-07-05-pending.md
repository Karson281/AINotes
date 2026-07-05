---
date: 2026-07-05
tags: [pending, telegram, gateway, hermes]
---

# Telegram Bot 叫唔醒 — 解決方案

## 問題
Hermes Gateway Telegram Bot 每日會「訓死」，要手動開 desktop `hermes chat` 先叫得醒，未能 7/24 運作。

## 原因診斷（2026-07-05）
- VPS: 🇭🇰 香港（中國移動香港）
- Gateway service: ✅ 正常運行
- DNS: ✅ 食到 `api.telegram.org`
- Telegram 連線: ⚠️ 有時 timeout，但 auto-retry（5分鐘間隔）
- Service definition: ⚠️ 曾有 outdated 提示（已 restart 修正）

---

## 方案 A — Gateway Restart ✅（已執行）

**操作：**
```bash
hermes gateway restart
```

**效果：**
- 更新 service definition 至最新版本
- 重新整頓 Telegram 連線
- 輕量級，唔會 lost session history

**Status:** ✅ 已於 2026-07-05 11:00 HKT 執行，Telegram 成功 reconnect

---

## 方案 B — Cron Job 朝早自動 Ping（備用）

如果方案 A 後都係日日訓死，set 一個 cron job 朝早 08:00 HKT 自動 send keepalive。

**指令：**
```bash
hermes cron create "0 0 * * *" \
  --prompt "send a message to my Telegram saying 'Good morning, gateway alive'" \
  --deliver telegram
```

或者用 no_agent script 模式直接 call Telegram API keepalive。

**效果：**
- 每日 08:00 bot 自己出聲，確保 gateway 唔會 idle 到訓死
- 零干擾，只係 ping 一下

---

## 方案 C — 唔搞，手動叫醒

每次 Telegram bot 冇反應時，開 desktop 行一次：
```bash
hermes chat -q "test"
```
或者直接同 CLI 講句嘢，gateway 就會 wake up。

**適用情況：**
- 如果 restart 後好返好多（例如一星期先死一次）
- 唔想為咗呢個問題加 cron job

---

## 跟進備註
- 2026-07-05 已執行 `hermes gateway restart`，service definition updated
- Telegram connected at 11:00 HKT，現在運作正常
- MCP obsidian_vault 有連接問題（可能係 ideapad offline 或 `${OBSIDIAN_MCP_KEY}` env var 問題），日後有需要再跟進
