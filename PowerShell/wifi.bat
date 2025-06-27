@echo off
for /f %%i in ('powershell -NoProfile -ExecutionPolicy Bypass -File  "C:\Users\qw941\Desktop\py\PowerShell\wifi_return1or0.ps1"') do set wifiStatus=%%i

if %wifiStatus%==1 (
    echo Wi-Fi 已连接
) else (
    echo Wi-Fi 未连接
)
pause
