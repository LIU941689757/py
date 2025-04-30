@echo off
setlocal enabledelayedexpansion

:: 変数設定
set "uninstallRegPath=HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
set "desktopPath=%USERPROFILE%\Desktop"
set "guidListFile=%desktopPath%\WebexGUIDs.txt"
set "installerPath=%desktopPath%\WebexInstaller.msi"

:: Webex が見つかったかどうかのフラグ
set "webexFound=false"

:: Webex に関係するアンインストールキーを検索
for /f "tokens=*" %%A in ('reg query "%uninstallRegPath%"') do (
    reg query "%%A" /v "DisplayName" 2>nul | find /i "Webex" >nul
    if !errorlevel! == 0 (
        set "webexFound=true"
        goto :uninstall
    )
)

:: Webex が見つからなかった場合、インストールを実行
echo Webex が見つかりませんでした。インストールを開始します...
msiexec /i "%installerPath%" /quiet /norestart
goto :eof

:uninstall
echo Webex がインストールされています。リストにあるすべてのバージョンをアンインストールします...

:: GUID リストを読み込み、順にアンインストール
for /f "usebackq tokens=* delims=" %%G in ("%guidListFile%") do (
    echo GUID をアンインストール中: %%G ...
    msiexec /x %%G /quiet /norestart
)

echo アンインストールが完了しました。
exit /b
