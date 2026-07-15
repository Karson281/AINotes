# 工作日誌 — 2026-07-14 (二)

## 目標
建立安全嘅 Windows → VPS 遠端存取通道，用 WireGuard + Port Knocking 取代 Tailscale。

## 完成事項

### 1. VPS WireGuard + knockd 安裝
- 安裝 wireguard、knockd、iptables
- 生成 server/client keypair
- `/etc/wireguard/wg0.conf` — VPS 端 WG config
- `/etc/knockd.conf` — 自訂 iptables 開門/關門 script

### 2. 埠號設定
| 項目 | 值 |
|------|-----|
| VPS WG IP | 10.99.99.1/24（內網）|
| Client WG IP | 10.99.99.2/32 |
| WG port | 51820（預設 iptables DROP，knockd 控制開關）|
| Knock open ports | 存於 `/root/wg-client-config/knock-info.txt`（⚠️ 不外傳）|
| Knock timeout | 5 分鐘後自動關門 |
| VPS server public key | 存於 `/root/wg-client-config/`（⚠️ 不外傳）|

### 3. Windows 端工具
- WireGuard Windows app — tunnel `windows-client` 已匯入
- PowerShell knock (`ConnectAsync` + 500ms timeout) — 解決 iptables DROP 導致 TCP timeout 問題
- 桌面捷徑 `wg.ps1` → double-click 零視窗連線

### 4. 連線流程 ✅
```
Windows: powershell knock（三 ports）
     ↓ SYN (iptables DROP, knockd libpcap 照收)
VPS: knockd → OPEN SESAME → iptables ACCEPT 51820
     ↓
Windows: WireGuard Activate → WG handshake
     ↓
Windows: ssh root@10.99.99.1 → ✅ Login
```

## 已知問題 / 待辦
- WireGuard CLI `/activatetunnel` 參數未完全驗證（目前靠 GUI activate）
- 5 分鐘自動鎖門，用耐咗要再 knock
- VPS 仍保留 SSH（非標準 port）作緊急後備

## VPS 資訊
- Public IP: （⚠️ 敏感，不紀錄於此）
- SSH (public): 非標準 port（⚠️ 敏感，不紀錄於此）
- WG tunnel: 10.99.99.1（內網 IP，經 knock 開門）
