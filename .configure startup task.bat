schtasks /create /tn "StartMicMuter" /tr "\"C:\Program Files (x86)\MicMuter\MicMuter.exe\"" /sc onlogon /ru %USERNAME% /rl HIGHEST /f
