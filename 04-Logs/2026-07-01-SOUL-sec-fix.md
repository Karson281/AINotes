# 安全修復記錄

**日期：** 2026-07-01
**類型：** 安全加固 — SOUL.md 憑據外洩修正

## 修改內容

1. **`/root/.hermes/SOUL.md`** — curl 指令中硬編碼的 Bearer Token 及 Obsidian URL（內部 Tailscale IP 地址）替換為環境變數引用
2. **`/root/.hermes/.env`** — 新增 `OBSIDIAN_AUTH` 和 `OBSIDIAN_URL` 兩個環境變數

## 違反規則

- CLAUDE.md 規則 1：API Key 明文寫入可持久化檔案
- CLAUDE.md 規則 2：內部 IP 地址暴露
- CLAUDE.md 規則 9：可推斷片段留在 SOUL.md 中

## 驗證

- ✅ SOUL.md 已修正 — Bearer Token 改為 `${OBSIDIAN_AUTH}`，IP 改為 `${OBSIDIAN_URL}`
- ✅ .env 已補充對應變數
- ✅ JSON `\n` 轉義正確（`od -c` 驗證）
- ✅ 工作日誌由 Proma 代寫入（Hermes VPS 因 CGNAT 無法直接連接本地 Obsidian）

## 備註

本次修改不包含任何 Token 值或 IP 地址的明文片段。
