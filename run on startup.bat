@echo off
setlocal

set "programPath=C:\Program Files (x86)\MicMuter\MicMuter.exe"
set "shortcutPath=%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\MicMuter.lnk"

:: Check if the shortcut already exists
if exist "%shortcutPath%" (
    echo Shortcut already exists.
    goto :end
)

:: Create the shortcut
echo Creating shortcut...
powershell -c "(New-Object -ComObject WScript.Shell).CreateShortcut('%shortcutPath%').TargetPath = '%programPath%'"

echo Shortcut created successfully.

:end
