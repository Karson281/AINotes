---
date: 2026-07-02
tags: [hermes, cron, security, housekeeping]
---

# 工作日誌 — Cron 時區修正 & SOUL.md 安全修復

## 完成事項

### 1. Cron 時區修正
- `hermes-update-check` 排程由 `0 3 * * 1`（UTC Mon 03:00 / HKT Mon 11:00）
  改為 `0 19 * * 1`（UTC Mon 19:00 / HKT Tue 03:00）
- 下次執行：2026-07-06 19:00 UTC

### 2. SOUL.md 安全修復（Hermes 主導，Proma 代寫 Log）
- `/root/.hermes/SOUL.md` 中硬編碼嘅 Bearer Token 及 Tailscale IP 地址
  替換為環境變數 `${OBSIDIAN_AUTH}` 及 `${OBSIDIAN_URL}`
- 對應變數已加入 `/root/.hermes/.env`
- 工作日誌由 Proma 代寫入（Hermes VPS 因 CGNAT 無法直連本地 Obsidian）

### 3. DeepSeek Key Cleanup
- 舊 key（尾碼 faa2）只存在於 backup snapshots 同 session dumps
- 當前 config.yaml + .env 已用新 key（尾碼 20）
- Stock Analysis cron job 預計下次觸發會自動修復

### 4. 共同記憶更新
- CLAUDE.md 加入明確 Vault 根路徑警告條款
- 預防日後再寫錯路徑

## 教訓
- 寫入 Obsidian Vault 必須明確指定 `D:\kaisu\Google Drive\AINotes\`（非 `D:\Users\kaisu\`）
- Hermes Cron 時間要用 UTC 表達，需注意 UTC+8 轉換
