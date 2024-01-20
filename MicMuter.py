import os
import sys
import webbrowser
import atexit
import win32api
import win32gui
import winreg
from pygame import mixer
from pynput import keyboard
from infi.systray import SysTrayIcon
import configparser

@atexit.register
def quit_program(systray):
    global m
    if m == 1 and unmuteOnExit == 1:
        mute()
    if m == 1:
        config['DEFAULT']['last_state'] = '1'
    if m == 0:
        config['DEFAULT']['last_state'] = '0'
    write_config()
    tray.shutdown()

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
        'unmute_on_exit': '0',
        'volume': '0.3',
        'output_device': '',
        'hotkey0': '<alt>+`',
        'hotkey1': '',
        'hotkey2': '',
        'hotkey3': '',
        'hotkey4': '',
        'hotkey5': '',
        'hotkey6': '',
        'hotkey7': '',
        'hotkey8': '',
        'hotkey9': '',
        'bw': 'auto',
        'last_state': '',
        'mute_sound': 'muted.wav',
        'unmute_sound': 'unmuted.wav'
    }
    write_config()

# Load the configuration file
config = configparser.ConfigParser()
config.read(config_path)
unmuteOnExit = int(config['DEFAULT']['unmute_on_exit'])
volume = float(config['DEFAULT']['volume'])
output_device = config['DEFAULT']['output_device']

# Define hotkeys dynamically
hotkey0 = config['DEFAULT']['hotkey0']
hotkey1 = config['DEFAULT']['hotkey1']
hotkey2 = config['DEFAULT']['hotkey2']
hotkey3 = config['DEFAULT']['hotkey3']
hotkey4 = config['DEFAULT']['hotkey4']
hotkey5 = config['DEFAULT']['hotkey5']
hotkey6 = config['DEFAULT']['hotkey6']
hotkey7 = config['DEFAULT']['hotkey7']
hotkey8 = config['DEFAULT']['hotkey8']
hotkey9 = config['DEFAULT']['hotkey9']

hotkeys = [hotkey0, hotkey1, hotkey2, hotkey3, hotkey4, hotkey5, hotkey6, hotkey7, hotkey8, hotkey9]

bw = config['DEFAULT']['bw']
last_state = config['DEFAULT']['last_state']
mute_sound = os.path.join(resources_path, config['DEFAULT']['mute_sound'])
unmute_sound = os.path.join(resources_path, config['DEFAULT']['unmute_sound'])

# Create the tray icon and set the unmuted icon
icon_muted_b = os.path.join(resources_path, 'muted_b.ico')
icon_unmuted_b = os.path.join(resources_path, 'unmuted_b.ico')
icon_muted_w = os.path.join(resources_path, 'muted_w.ico')
icon_unmuted_w = os.path.join(resources_path, 'unmuted_w.ico')
icon_last_state = os.path.join(resources_path, 'muted_b.ico')

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

    # Update the configuration with the current state
    config['DEFAULT']['last_state'] = str(m)
    write_config()

def github():
    webbrowser.open('https://github.com/danieldotkim/')

def github_wrapper(event):
    github()

def set_state_to_unmuted():
    global m
    m = 0
    tray.update(icon_unmuted)

def set_state_to_unmuted_wrapper(event):
    set_state_to_unmuted()

def set_state_to_muted(dummy_argument=None):
    global m
    m = 1
    tray.update(icon_muted)

def set_state_to_muted_wrapper(event):
    set_state_to_muted()

def is_dark_mode_enabled():
    # Open the registry key that contains the system's personalization settings
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize')
    # Read the value of the "AppsUseLightTheme" key
    # Returns 0 if light mode is enabled, 1 if dark mode is enabled
    value = winreg.QueryValueEx(key, 'AppsUseLightTheme')[0]
    # Return True if dark mode is enabled, False otherwise
    return value == 0

darkmode = is_dark_mode_enabled()

def mute_wrapper(event):
    mute()

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

def open_config():
    webbrowser.open(config_path)

def open_config_wrapper(event):
    open_config()

# Initialize the correct tray icon based on config
if (bw == 'auto' and darkmode == False) or bw == 'b':
    icon_muted = icon_muted_b
    icon_unmuted = icon_unmuted_b
elif (bw == 'auto' and darkmode == True) or bw == 'w':
    icon_muted = icon_muted_w
    icon_unmuted = icon_unmuted_w
    
# Tray menu
menu_options = (
    ("Mute/Unmute", None, mute_wrapper),
    ("Created by https://github.com/danieldotkim/", None, github_wrapper),
    ("Toggle black/white icons", None, bwtoggle_wrapper),
    ("Set state to unmuted", None, set_state_to_unmuted_wrapper),
    ("Set state to muted", None, set_state_to_muted),
    ("Open Configuration", None, open_config_wrapper),
    ("Quit", None, quit_program),
)

tray = SysTrayIcon(icon_unmuted, "MicMuter", menu_options)

# Set icon based on last state
if last_state == '0' or last_state == '':
    tray.update(icon_unmuted)
    m = 0
if last_state == '1':
    tray.update(icon_muted)
    m = 1

# tray.update(icon_unmuted) # set the tray icon to the unmuted icon
tray.start()

hotkeys = [hotkey0, hotkey1, hotkey2, hotkey3, hotkey4, hotkey5]
hotkey_dict = {}
for hotkey in hotkeys:
    if hotkey != '':
        hotkey_dict[hotkey] = mute
h = keyboard.GlobalHotKeys(hotkey_dict)
h.start()