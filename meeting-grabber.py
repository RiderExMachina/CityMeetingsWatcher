#== City Meeting Watcher script ==#
## Watches Livestream.com accounts for updates
##  and pipes them through yt-dlp to archive them.
## TODO: Also converts videos to audio through ffmpeg

import json, os
try:
    import requests
except:
    print("Unable to import 'requests' package. Please install via pip!")

#url = "https://api.new.livestream.com/accounts/11220190/events/3725902/"

## Pull cached upload date
if not os.path.isfile("settings.json"):
    import setup
    setup()
else:
    with open("settings.json", "a") as settingsFile:
        mainFolder = settingsFile["dlFolder"]
        uraPrevMeeting = settingsFile["col-ura-prev"]
        ccPrevMeeting = settingsFile["col-cc-prev"]
        pazPrevMeeting = settingsFile["col-paz-prev"]

version = "0.0.1"
## Livestream IDs
##  City Council: 3725902
##  URA         : 3725864
##  Plan & Zone : 6554264
events = {
        1: {
            "id": "3725864",
            "name": "URA",
            "folder": "col-ura",
            "prevMeeting": uraPrevMeeting
            },
        2: {
            "id": "3725902",
            "name": "City Council",
            "folder": "col-cc",
            "prevMeeting": ccPrevMeeting
            },
        3: {
            "id": "6554264",
            "name": "Panning & Zoning",
            "folder": "col-paz",
            "prevMeeting": pazPrevMeeting
            }
    }


def updateCheck(events):
    updated = False
    for i in events:
        event = events[i]["id"]
        name = events[i]["name"]
        subFolder = events[i]["folder"]
        prevMeeting = events[i]["prevMeeting"]
        dlFolder = os.path.join(mainFolder, subfolder)
        eventURL = f"https://api.new.livestream.com/accounts/11220190/events/{event}"
        data = requests.get(url).json()

        ## Get latest Upload
        latestMeeting = data["feed"]["data"][0]
        meetingID = latestMeeting["data"]
        if meetingID != cachedMeetingID:
            updated = True
            videoURL = f"https://livestream.com/accounts/11220190/events/{event}/videos/{meetingID}"
            os.chdir(dlFolder)
            os.system(f'ytd-lp -o "%(upload_date>%Y-%m-%d)s - {name} Meeting.%(ext)s" {videoURL}')
            #with open(settings, 'a') as settingsFile:
    if updated:
        return
