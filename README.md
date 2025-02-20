@echo off
chcp 65001 >nul
title 贪吃蛇
mode con: cols=40 lines=20
setlocal enabledelayedexpansion

:: 启用 ANSI 终端控制（Win10 及以上）
for /f "tokens=2 delims=: " %%A in ('"echo prompt $E|cmd"') do set "ESC=%%A"

:: 初始化
set "snakeX=20"
set "snakeY=10"
set "foodX=10"
set "foodY=5"
set "dir=R"
set "length=1"

:: 隐藏光标
echo %ESC%[?25l

:: 生成食物
:gen_food
set /a "foodX=2+(!random! %% 36)"
set /a "foodY=2+(!random! %% 16)"

:: 方向控制
:get_key
choice /c WSAD /n /t 1 /d %dir% >nul
if errorlevel 4 set "dir=D"
if errorlevel 3 set "dir=A"
if errorlevel 2 set "dir=S"
if errorlevel 1 set "dir=W"

:: 移动
if "%dir%"=="W" set /a snakeY-=1
if "%dir%"=="S" set /a snakeY+=1
if "%dir%"=="A" set /a snakeX-=1
if "%dir%"=="D" set /a snakeX+=1

:: 判断碰撞
if %snakeX% lss 1 goto game_over
if %snakeX% gtr 38 goto game_over
if %snakeY% lss 1 goto game_over
if %snakeY% gtr 18 goto game_over

:: 吃食物
if %snakeX%==%foodX% if %snakeY%==%foodY% (
    set /a length+=1
    goto gen_food
)

:: 绘制游戏
cls
echo %ESC%[%foodY%;%foodX%H🍎
echo %ESC%[%snakeY%;%snakeX%H🐍

:: 继续循环
goto get_key

:game_over
cls
echo %ESC%[10;15H游戏结束！
echo %ESC%[12;10H你的得分：%length%
echo %ESC%[14;10H按任意键退出...
pause >nul
exit
