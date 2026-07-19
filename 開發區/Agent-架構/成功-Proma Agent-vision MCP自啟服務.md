---
prefix: 成功
status: completed
created: 2026-06-20
---

# 成功-Proma Agent-vision MCP 自啟服務

## 功能描述
qwen-vision MCP server 註冊為 Windows 開機自動啟動，唔使再手動開 PowerShell。

## 設定方法
用 Windows Task Scheduler 註冊啟動 task。

```powershell
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c start /min `"`" `"C:\Users\kaisu\.proma\agent-workspaces\default\workspace-files\hermes-mqtt-bridge\start-qwen-vision.bat`""
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest
Register-ScheduledTask -TaskName "QwenVisionMCP" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force
```

## 管理方式
```powershell
# 檢查狀態
Get-ScheduledTask -TaskName QwenVisionMCP

# 立即啟動
Start-ScheduledTask -TaskName QwenVisionMCP

# 停止（熄 server 後）
Stop-ScheduledTask -TaskName QwenVisionMCP

# 刪除
Unregister-ScheduledTask -TaskName QwenVisionMCP -Confirm:$false
```

## 啟動腳本位置
`C:\Users\kaisu\.proma\agent-workspaces\default\workspace-files\hermes-mqtt-bridge\start-qwen-vision.bat`

## 相關檔案
- [[成功-Proma Agent-Qwen-vision MCP tool]]
