import win32api
import win32gui
from pynput import keyboard
from pygame import mixer
import configparser
from infi.systray import SysTrayIcon
import time
import webbrowser
import sys
import os
import winreg

config_name = 'config.ini'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)
resources_path = os.path.join(application_path, 'resources')

def write_config():
    with open(config_path, 'w') as configfile:
        config.write(configfile)

# Create the configuration file if it does not exist
if not os.path.exists(config_path):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'unmuteOnExit': '1',
        'volume': '0.3',
        'output_device': '',
        'hotkey0': '<alt>+`',
        'hotkey1': '',
        'hotkey2': '',
        'bw' : 'auto',
        'mute_sound': 'muted.wav',
        'unmute_sound': 'unmuted.wav'
    }
    write_config()

# Load the configuration file
config = configparser.ConfigParser()
config.read(config_path)
unmuteOnExit = int(config['DEFAULT']['unmuteOnExit'])
volume = float(config['DEFAULT']['volume'])
output_device = config['DEFAULT']['output_device']
hotkey0 = config['DEFAULT']['hotkey0']
hotkey1 = config['DEFAULT']['hotkey1']
hotkey2 = config['DEFAULT']['hotkey2']
bw = config['DEFAULT']['bw']
mute_sound = os.path.join(resources_path, config['DEFAULT']['mute_sound'])
unmute_sound = os.path.join(resources_path, config['DEFAULT']['unmute_sound'])

# Create the tray icon and set the unmuted icon
icon_muted_b = os.path.join(resources_path, 'muted_b.ico')
icon_unmuted_b = os.path.join(resources_path, 'unmuted_b.ico')
icon_muted_w = os.path.join(resources_path, 'muted_w.ico')
icon_unmuted_w = os.path.join(resources_path, 'unmuted_w.ico')

# Set bw status from config
icon_muted = 'icon_muted_' + bw
icon_unmuted = 'icon_unmuted_' + bw

# Initialize the mixer
if output_device == '':
    mixer.init()
elif output_device != '':
    mixer.init(devicename=output_device)

# Set the volume for the sound files
ms = mixer.Sound(mute_sound)
ums = mixer.Sound(unmute_sound)
ms.set_volume(volume)
ums.set_volume(volume)

# Defines a global variable 'm' to keep track of mute/unmute status
m = 0

def mute():
    global m
    if m == 0:
        ms.play()
        tray.update(icon_muted)
    else:
        ums.play()
        tray.update(icon_unmuted)

    WM_APPCOMMAND = 0x319
    APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000

    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
    m ^= 1

def mute_wrapper(event):
    mute()

def github():
    webbrowser.open('https://github.com/ddanielkim/')

def github_wrapper(event):
    github()

def reset_state():
    global m
    m = 0
    tray.update(icon_unmuted)

def reset_state_wrapper(event):
    reset_state()
# unmutes before quitting
def quit_program(systray):
    global m
    if m == 1 and unmuteOnExit == 1:
        mute()
    time.sleep(1)
    tray.shutdown()

def is_dark_mode_enabled():
    # Open the registry key that contains the system's personalization settings
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize')
    # Read the value of the "AppsUseLightTheme" key
    # Returns 0 if light mode is enabled, 1 if dark mode is enabled
    value = winreg.QueryValueEx(key, 'AppsUseLightTheme')[0]
    # Return True if dark mode is enabled, False otherwise
    return value == 0

darkmode = is_dark_mode_enabled()

def bwtoggle():
    global bw
    global icon_muted
    global icon_unmuted
    global m

    if (config['DEFAULT']['bw'] == 'auto' and darkmode == True) or config['DEFAULT']['bw'] == 'w':
        config['DEFAULT']['bw'] = 'b'
        icon_muted = icon_muted_b
        icon_unmuted = icon_unmuted_b
    elif (config['DEFAULT']['bw'] == 'auto' and darkmode == False) or (config['DEFAULT']['bw'] == 'b'):
        config['DEFAULT']['bw'] = 'w'
        icon_muted = icon_muted_w
        icon_unmuted = icon_unmuted_w

    if m == 0:
        tray.update(icon_unmuted)
        print('unmuted')
    elif m == 1:
        tray.update(icon_muted)

    write_config()

def bwtoggle_wrapper(event):
    bwtoggle()

# Initialize the correct tray icon based on config
if (bw == 'auto' and darkmode == False) or bw == 'b':
    icon_muted = icon_muted_b
    icon_unmuted = icon_unmuted_b
elif (bw == 'auto' and darkmode == True) or bw == 'w':
    icon_muted = icon_muted_w
    icon_unmuted = icon_unmuted_w
    
# Tray menu
menu_options = (("Mute/Unmute", None, mute_wrapper), ("Toggle black/white icons", None, bwtoggle_wrapper), ("Reset state to unmuted", None, reset_state_wrapper), ("Created by https://github.com/ddanielkim/", None, github_wrapper), ("Quit", None, quit_program),)
tray = SysTrayIcon(icon_unmuted, "MicMuter", menu_options)
tray.update(icon_unmuted) # set the tray icon to the unmuted icon
tray.start()

hotkeys = [hotkey0, hotkey1, hotkey2]
hotkey_dict = {}
for hotkey in hotkeys:
    if hotkey != '':
        hotkey_dict[hotkey] = mute
h = keyboard.GlobalHotKeys(hotkey_dict)
h.start()