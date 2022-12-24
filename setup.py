## Setup file. Is called from the main Meeting Grabber.py, but could probably be ran standalone.

import os, json

def init():
	homeFolder = os.path.expanduser("~")
	if "vm" in os.popen("hostnamectl | grep Chassis").read():
        print("Running in a VM, probably a server?")
		defaultMainFolder = "/srv/government"
	else:
        print("Assuming we're running on a PC")
		defaultMainFolder = f"{homeFolder}/government"
		
    configDir = input(f"Where do you want the files to be downloaded to? [default: {defaultMainFolder}]\n\t=>")
    if configDir == "":
        configDir = defaultMainFolder
    print(f"Okay, will download and serve files from {configDir}")
    

print("Settings File (settings.json) not found!")
createFile = input("Would you like to create one? [Y/n]\n\t=> ")

if createFile.lower() in ["", "yes", "y"]:
	init()
else:
	print("Okay, quitting!")
	exit()
