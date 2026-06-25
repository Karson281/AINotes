---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-整合哲學-Hermes+Proma+Obsidian 協作架構

## 核心概念：星型拓樸 (Star Topology)

本方案採用 **以 Obsidian MCP Server 為中介的星型拓樸**。兩個 Agent 無需直接建立雙向連線，而是共同透過 MCP 協議對 Obsidian Vault 進行讀寫，實現**解耦、非同步的協同工作**。

```
                          ┌─────────────────┐
                          │   你的手機       │
                          └────────┬────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
               ┌────▼───┐   ┌────▼────┐   ┌────▼────┐
               │ Hermes │   │ Obsidian│   │ Proma   │
               │ Agent  │◄──┤ Vault   ├──►│ Agent   │
               │ (VPS)  │   │ (中樞)  │   │ (本地)  │
               └────────┘   └─────────┘   └─────────┘
```

## 三大角色分工

| 組件 | 角色定位 | 核心能力 |
|------|---------|---------|
| **Hermes Agent (VPS)** | 24/7 常駐大腦 | 背景監控、網絡爬蟲、自我進化學習循環、持久化記憶 |
| **Proma Agent (本機)** | 本地執行雙手 | 本地檔案操作、腳本執行、桌面自動化、工作區管理 |
| **Obsidian (本機)** | 中樞神經 | 消息隊列 (Message Queue)、結構化知識庫、共享狀態層 |

## 協作流程
```
Hermes 發現異動 / 收到手機任務
    → 寫入 Obsidian tasks/inbox/（MQTT / Obsidian MCP）
    → Proma 讀取任務 → 分析決策
    → 結果寫回 tasks/done/ 或 tasks/hermes-outbox/
    → Hermes 收到結果 → 執行下一步 / 通知用戶
```

## 關鍵技術
- **MCP (Model Context Protocol)**：統一協議層，所有工具通過 MCP 連接
- **Obsidian Vault**：共享存儲層（Google Drive 同步）
- **MQTT Broker**：Hermes → Obsidian 嘅即時通道（待落地）
- **Google Drive**：跨裝置同步層（手機 Obsidian 都睇到）
