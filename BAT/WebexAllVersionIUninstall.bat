@echo off
chcp 65001
echo 正在查找 Webex 产品代码...
for /f "tokens=2 delims={}" %%i in ('wmic product where "name like '%%Webex%%'" get IdentifyingNumber /format:list ^| findstr IdentifyingNumber') do (
    set ProductCode={%%i}
echo 产品代码为%%i
)

if not defined ProductCode (
    echo 未找到 Webex 安装，请检查是否已安装。
    pause
    exit /b
)

echo 正在卸载 Webex，请稍候...
start /wait msiexec /x %ProductCode% /qn

echo Webex 已卸载完成。
pause
