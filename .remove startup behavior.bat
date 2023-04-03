@echo off
schtasks /delete /tn "MicMuter" /f
echo Deleting shortcut from Startup folder.
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MicMuter.lnk"
echo Complete.
pause
