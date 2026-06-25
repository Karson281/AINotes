@echo off
set PYTHON=C:\Users\kaisu\AppData\Local\Microsoft\WindowsApps\python3.exe
set SCRIPT=C:\Users\kaisu\OneDrive\AINotes\.scripts\vault-polling.py
set WORKDIR=C:\Users\kaisu\OneDrive\AINotes

schtasks /create /tn "Vault Polling Agent" /tr "%PYTHON% %SCRIPT%" /sc onstart /delay 0000:30 /f /it /rl highest
if %errorlevel% equ 0 (
    echo SUCCESS! Task created.
    echo.
    echo Please run it manually to test:
    echo   Task Scheduler -^> right-click "Vault Polling Agent" -^> Run
    echo.
    echo Check log: notepad %WORKDIR%\.scripts\polling.log
) else (
    echo FAILED. Please run as Administrator.
)
pause
