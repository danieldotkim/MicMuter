@echo off

set "CURRENT_DIR=%~dp0"
set "MIC_MUTER_EXE=%CURRENT_DIR%MicMuter.exe"
set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MicMuter.lnk"

schtasks /create /tn "MicMuter" /tr "\"%MIC_MUTER_EXE%\"" /sc once /st 00:00 /sd 01/01/2000 /ru %USERNAME% /rl highest /f

echo Creating MicMuter (Administrator).bat.
set "BAT_FILE=%CURRENT_DIR%\MicMuter (Administartor).bat"
echo schtasks.exe /run /tn MicMuter > "%BAT_FILE%"
echo Done.

echo Creating MicMuter (Administrator).bat shortcut in Startup folder.
set "SHORTCUT_FILE=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MicMuter.lnk"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(\"%SHORTCUT_PATH%\"); $Shortcut.TargetPath = '%BAT_FILE%'; $Shortcut.IconLocation = '%MIC_MUTER_EXE%'; $Shortcut.Save();"
echo Done.

pause