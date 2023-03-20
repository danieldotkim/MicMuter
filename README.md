# MicMuter
Python script that runs on tray and mutes/unmutes your microphone.

Launch MicMuter.exe to start.
The default key to mute/unmute is alt+` (tilde).

Run "make MicMuter.exe run on startup.bat" to make it launch on startup.
If you want to make MicMuter launch on start with admin, import StartMicMuter.xml to Task Scheduler.

Right click on the tray icon and click "Reset state to unmuted" if the mic is unmuted but the indicator shows muted icon.

The default icon color is set by your current Windows theme.
If it is light, it will show black icons, if it is dark, it will show white icons.
You can manually change that by clicking "Toggle black/white icons" in the tray menu.
If you want to go back to auto mode, please change the bw value to auto (bw = auto).

Volume, hotkey, and other settings can be changed in the config.ini.
Hotkey lists can be found here: https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
Put modifiers inside <>

-----
Sounds inspired from Discord mute/unmute sound.
Mute icons created by Freepik - Flaticon: https://www.flaticon.com/free-icons/mute
Modified the icons to fit the theme.
