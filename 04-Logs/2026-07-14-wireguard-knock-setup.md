---
date: 2026-07-14
time: 18:48
project: VPS
tags: [wireguard, port-knocking, security, tailscale-alternative]
---

# VPS WireGuard + Port Knocking 替代 Tailscale 方案

## 背景
Tailscale 死線，VPS 無法透過 Tailscale IP 訪問。需要替代方案來安全連接 VPS。

## 方案選擇
經 Hermes 建議四個方案（Port Knocking / Cloudflare Tunnel / WireGuard / 放生）後，
選擇 **方案 C + A 組合**：WireGuard 直連 + Port Knocking 保護 WG port。

### 選擇原因
- Tailscale 底層即 WireGuard，用返同等加密質素
- 零 third-party dependency，唔使 account
- Full network access（所有 port 直通，唔似 CF Tunnel 要逐個 map）
- Port Knocking 令外面 scan 永遠 zero open port
- 雙重防線：knock fails → port 唔存在；WG key wrong → silent drop

## 已建立檔案
| 檔案 | 用途 |
|------|------|
| `vps-wireguard-knock-setup.sh` | VPS 端一鍵部署（WireGuard + knockd + iptables） |
| `wg-connect.ps1` | Windows PowerShell knock + 自動連接 |
| `wg-connect.bat` | Double-click batch wrapper |
| `wg-config.txt` | Windows 端 config template |
| `wg-check.sh` | VPS 端診斷 script |
| `wg-setup-readme.md` | 完整使用說明 |

所有檔案位置：`~/.proma/agent-workspaces/default/927d91ad-99c5-4498-97e7-d2a7e22dd9d6/`

## 待執行
- [ ] 透過 VPS provider console 連入 VPS
- [ ] 執行 vps-wireguard-knock-setup.sh
- [ ] Windows 安裝 WireGuard client + 匯入 config
- [ ] 設定 wg-config.txt 參數
- [ ] 測試連接
- [ ] 將 knock 序列存入 password manager

## 安全設計
- Outside scan → WG port 永遠 filtered（不存在）
- Knock 後 → 只開放 knocking IP，10 秒 timeout（但 rule persistent 直到 lock）
- WireGuard → Curve25519，wrong key = silent drop
- 設有「鎖門」close knock sequence 主動關閉 port
