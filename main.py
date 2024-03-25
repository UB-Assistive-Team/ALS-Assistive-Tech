"""
Main module for controlling TV and other functions.

This module contains functions for controlling TV commands such as power on/off,
mute/unmute, volume up/down, and channel up/down. It also provides functions for
managing configuration, resetting mouse position, speaking text, and cleaning up
resources.

"""

import eel
import serial_com
#import rfcontroller # This import should be commented out when testing on a PC
import json
import pyautogui
import threading
#import pyttsx3
from gtts import gTTS
import os
from serial_com import send_command, TVCommand  # Import the send_command function and TVCommand enum from serial_com.py

def powerOnOff():
    """Send power on command."""
    serial_com.send_command(serial_com.TVCommand.TURN_ON_OFF.value)

def muteUnmute():
    """Send mute command."""
    serial_com.send_command(serial_com.TVCommand.MUTE_UNMUTE.value)

def volumeUp():
    """Send volume up command."""
    serial_com.send_command(serial_com.TVCommand.VOLUME_UP.value)

def volumeDown():
    """Send volume down command."""
    serial_com.send_command(serial_com.TVCommand.VOLUME_DOWN.value)

def channelUp():
    """Send channel up command."""
    serial_com.send_command(serial_com.TVCommand.CHANNEL_UP.value)

def channelDown():
    """Send channel down command."""
    serial_com.send_command(serial_com.TVCommand.CHANNEL_DOWN.value)

#controller = rfcontroller.RFController() # Comment this out when developing on desktop
screenWidth, screenHeight = pyautogui.size()
pyautogui.FAILSAFE = False

def togglePlug(command):
    """Toggle plug."""
    print(command) # For testing on a PC, this line should be uncommented, and the following line should be commented out
    #controller.sendcode(command) # This line should be commented out when testing on PC, the library is not available on PC

def storeConfig(setting, value):
    """Store configuration."""
    config = {}
    with open('config.json', 'r') as openfile:
    #with open('/home/pi/ALS-Assistive-Tech/config.json', 'r') as openfile:
        config  = json.load(openfile)
    with open('config.json', 'w') as writefile:
    #with open('/home/pi/ALS-Assistive-Techp/config.json', 'w') as writefile:
        config[setting] = value
        json.dump(config, writefile)

def loadConfig():
    """Load configuration."""
    with open('config.json', 'r') as openfile:
    #with open('/home/pi/ALS-Assistive-Tech/config.json', 'r') as openfile:
        config = json.load(openfile)
        eel.loadConfig(config)

def resetMouse():
    """Reset mouse position."""
    pyautogui.moveTo(0, screenHeight)

def speak_from_text(text):
    """Speak from text."""
    speak_text(text)  # The function defined above

def cleanup():
    """Cleanup resources."""
    serial_com.ser.close()
    print("Serial port closed")

if __name__ == "__main__":
    eel.init('/home/pi/ALS-Assistive-Tech/web', allowed_extensions=[".js",".html"])
    resetMouse()
    eel.start('index.html', cmdline_args=['--start-fullscreen'])

    # Call send_commands() after server starts
    serial_com.send_commands()

def speak_text(text):
    """Speak text."""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("mpg123 output.mp3")  # use 'mpg123 output.mp3' or a suitable alternative.

# Example usage:
speak_text("Hello world, this is a test of Google Text to Speech")
