---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-Hermes Agent-MQTT cron 修正

## 功能描述
修正 MQTT outbox forwarder cron job，避免 log file 空白時仍不斷 send empty message 去 Telegram。

## 背景
原先嘅 cron job 每 2 分鐘檢查 `/root/.hermes/mqtt_outbox.log`，有檔案就 send_message，但空白內容也照 send。修正後加咗 empty content check。

## 建立方式
由 Hermes Agent 內部 cron system 建立，非 crontab。

```bash
# 經由 Hermes chat 建立
hermes chat
# 對 Hermes 講：
「幫我創建一個 cron job，名 mqtt-outbox-forwarder，每2分鐘執行一次。檢查 /root/.hermes/mqtt_outbox.log，有非空白內容先 send_message 然後清空」
```

## Script 內容
`/root/.hermes/scripts/mqtt-outbox-forwarder.sh`：
```bash
#!/bin/bash
LOGFILE="/root/.hermes/mqtt_outbox.log"
if [ ! -f "$LOGFILE" ]; then exit 1; fi
CONTENT=$(cat "$LOGFILE" | head -c 4000)
if [ -z "$CONTENT" ]; then exit 1; fi
echo "$CONTENT"
```

## Cron Job 管理
```bash
# 列出所有 cron jobs
hermes cron list

# 移除 cron job
hermes cron remove mqtt-outbox-forwarder
```

## 語法要點
- 指令用 `hermes cron remove`（唔係 `stop`）
- `hermes cron list` 睇到所有 active jobs
