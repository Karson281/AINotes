---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-MQTT Bridge-設計架構

## 功能描述
Hermes → MQTT → Obsidian Vault → Proma Agent 嘅全鏈路設計，用檔案系統做松耦合（Loose Coupling）。

## 架構圖
```
手機 ──→ Hermes Agent (VPS)
              │ publish proma/inbox
              ▼
        Mosquitto (Docker @ KVM2)
              │
              ▼
        MQTT Subscriber (Windows PC)
              │ 寫入 .md
              ▼
        Obsidian Vault tasks/inbox/
              │
              ▼
        Proma Agent 讀取 → 分析 → 寫回 hermes-outbox/
              │
              ▼
        Subscriber publish 回 MQTT
              │
              ▼
        Hermes Agent 收到結果
```

## Topics 協議
| Topic | 方向 | 用途 |
|-------|------|------|
| `proma/inbox` | Hermes → Proma | 任務請求 |
| `proma/outbox` | Proma → Hermes | 分析結果 |
| `hermes/exec` | Proma → Hermes | 執行指令 |

## 訊息格式 (JSON)
```json
{
  "title": "分析 0363.HK",
  "type": "stock-analysis",
  "description": "今日走勢點睇？",
  "data": { "code": "0363.HK" }
}
```

## 相關檔案
- [[成功-MQTT Bridge-docker-compose+subscriber script]]
- [[有待跟進-MQTT Bridge-落地部署]]
