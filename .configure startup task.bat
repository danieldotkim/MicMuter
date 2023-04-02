@echo off
schtasks /create /tn "StartMicMuter" /tr "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File 'C:\Program Files (x86)\MicMuter\TaskSchedulerStarter.ps1'" /sc onlogon /ru %USERNAME% /rl highest
pause