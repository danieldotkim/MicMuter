# MicMuter
Lightweight program that allows you to mute or unmute your microphone easily through a tray icon.
It is available via portable zip and installer. They can be found in [Releases](https://github.com/ddanielkim/MicMuter/releases)

The default hotkey to mute/unmute is alt+` (tilde).

If the microphone is desynced with the tray icon, right-click the tray icon and select "Set state to unmuted" or "Set state to muted."

Your current Windows theme determines the default icon color. MicMuter will show black icons for light themes and white icons for dark themes. You can manually change the icon color by selecting "Toggle black/white icons" in the tray menu. If you want to go back to the default color scheme, change the bw value to "auto" in the config.ini file.

The script allows you to customize various settings, such as volume, hotkey, and more, through the config.ini file. Refer to the list of available hotkeys [here](https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key) (modifiers should be put inside <>).
You may choose up to 10 different hotkeys.

Sounds inspired by Discord mute/unmute sound.
Icons created by [Freepik - Flaticon](https://www.flaticon.com/free-icons/mute).
Modified the icons to fit the MicMuter theme.
