---
prefix: 成功->停用
status: completed
created: 2026-06-20
---

# 成功-MQTT Bridge-docker-compose + subscriber script

## 功能描述
MQTT Bridge 嘅程式碼已經全部寫好，包含 VPS 端 Mosquitto Docker 同 Windows 端 Python subscriber。

## 檔案位置
所有檔案喺 `workspace-files/hermes-mqtt-bridge/`：

| 檔案 | 用途 | 部署位置 |
|------|------|---------|
| `docker-compose.yml` | Mosquitto MQTT Broker | KVM2 VPS |
| `mosquitto/config/mosquitto.conf` | MQTT 設定（auth, persist） | KVM2 VPS |
| `mqtt-subscriber.py` | Windows MQTT→Obsidian 橋接 | Windows PC |
| `hermes-config-singapore.yaml` | Hermes 新加坡 config 參考 | 可選 |

## MQTT Subscriber 功能
- 訂閱 `proma/inbox` → 收到任務寫入 `tasks/inbox/`
- 監控 `tasks/hermes-outbox/` → 自動 publish 回 `proma/outbox`
- Windows toast notification 新任務通知
- OneDrive/Google Drive 自動同步（Vault 已 sync）

## Subscriber 啟動
```powershell
pip install paho-mqtt watchdog plyer
python mqtt-subscriber.py
```

## 相關檔案
- [[成功-MQTT Bridge-設計架構]]
- [[有待跟進-MQTT Bridge-落地部署]]
