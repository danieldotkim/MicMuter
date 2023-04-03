# MicMuter
Light weight program that allows you to mute or unmute your microphone easily through a tray icon.
It is available via portable zip and installer. They can be found in [Releases](https://github.com/ddanielkim/MicMuter/releases)

The default hotkey to mute/unmute is alt+` (tilde).

In the event that the microphone is unmuted, but the indicator shows a muted icon, simply right-click the tray icon and select "Reset state to unmuted".

The default icon color is determined by your current Windows theme. MicMuter will show black icons for light themes, and white icons for dark themes. You can manually change the icon color by selecting "Toggle black/white icons" in the tray menu. If you want to go back to the default color scheme, simply change the bw value to "auto" in the config.ini file.

The script allows you to customize various settings such as volume, hotkey, and more, through the config.ini file. Refer to the list of available hotkeys [here](https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key) (modifiers should be put inside <>).

Sounds inspired from Discord mute/unmute sound.
Icons created by [Freepik - Flaticon](https://www.flaticon.com/free-icons/mute)
Modified the icons to fit the MicMuter theme.
