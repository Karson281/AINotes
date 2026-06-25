---
prefix: 有待跟進
status: pending
created: 2026-06-20
---

# 有待跟進-MQTT Bridge-落地部署

## 需要完成嘅事項
### KVM2 VPS：起 Mosquitto
- [ ] SSH / Browser Console 入 VPS
- [ ] `cd ~/mqtt-bridge && docker compose up -d`
- [ ] 設 MQTT 密碼：`docker compose exec mosquitto mosquitto_passwd -b /mosquitto/config/passwd proma <password>`
- [ ] `docker compose restart`
- [ ] 測試連線

### Windows：起 Subscriber
- [ ] Install Python 套件：`pip install paho-mqtt watchdog plyer`
- [ ] Edit `mqtt-subscriber.py`：
  - `MQTT_BROKER = "your-kvm2-ip"`
  - `MQTT_PASS = "your-password"`
- [ ] 啟動：`python mqtt-subscriber.py`

## 背景
Code 已寫好，只差執行部署。落地後 Hermes publish 嘅訊息會自動落入 Obsidian Vault。

## 前置條件
- Docker 已在 VPS 安裝（Manus setup 時應有）
- VPS 已開 firewall port 1883

## 執行後驗證
```bash
# VPS test
mosquitto_pub -h localhost -t "proma/inbox" -m '{"title":"test"}'
```
Inbox 應該自動出現喺 `開發區/tasks/inbox/`
