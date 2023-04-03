@echo off
set "CURRENT_DIR=%~dp0"
set "MIC_MUTER_EXE=%CURRENT_DIR%MicMuter.exe"
set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MicMuter.lnk"

echo Creating MicMuter shortcut to startup menu.
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(\"%SHORTCUT_PATH%\"); $Shortcut.TargetPath = '%MIC_MUTER_EXE%'; $Shortcut.IconLocation = '%MIC_MUTER_EXE%'; $Shortcut.Save();"
echo Done.

pause
