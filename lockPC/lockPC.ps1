# LockScreen.ps1

# 使用 WScript.Shell COM 对象来调用锁屏命令
$wshell = New-Object -ComObject wscript.shell
$wshell.SendKeys('^{ESC}')
