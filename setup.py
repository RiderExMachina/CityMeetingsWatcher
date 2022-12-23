## Setup file. Is called from the main Meeting Grabber.py, but could probably be ran standalone.

import os, json

def init():
    if "vm" in os.popen("hostnamectl | grep Chassis").read():
        print("Detected running in VM")
    else:
        print("Are we running on a desktop?")

print("Settings File (settings.json) not found!")
createFile = input("Would you like to create one? [Y/n]\n\t-> ")

if createFile.lower() in ["", "yes", "y"]:
    init()
else:
    print("Okay, quitting!")
    exit()
