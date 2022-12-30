# == City Meeting Watcher script == #
## Watches Livestream.com accounts for updates
##  and pipes them through yt-dlp to archive them.
## TODO: Also converts videos to audio through ffmpeg

import json, os

try:
    import requests
except:
    print("Unable to import 'requests' package. Please install via pip!")
    exit()

def checkFolders(destFolder):
    if not os.path.isdir(destFolder):
        os.mkdir(destFolder)

def updateCheck(account, event):
        url = f"https://api.new.livestream.com/accounts/{account}/events/{event}"
        data = requests.get(url).json()

        ## Get latest Upload
        latestMeeting = data["feed"]["data"][0]
        meetingID = latestMeeting["data"]["id"]
        return meetingID

def infoParse(info):
    print("Loading data...")
    updated = False
    dlFolder = info["dl-dir"]
    account = info["account-id"]

    for i in info["streams"]:
        event = info["streams"][i]["id"]
        name = info["streams"][i]["name"]
        subFolder = info["streams"][i]["sub-folder"]
        prevMeeting = info["streams"][i]["prev-stream-id"]
        print(f"{name} ({event})")
        ## Make sure folder to download exists
        destFolder = os.path.join(dlFolder, subFolder)
        checkFolders(destFolder)
        ## Get newest meeting ID
        meetingID = updateCheck(account, event)

        if meetingID != prevMeeting:
            updated = True
            print(f"\t- Looks like there was an update! (Current: {meetingID}, Previous: {prevMeeting})")
            videoURL = f"https://livestream.com/accounts/11220190/events/{event}/videos/{meetingID}"
            os.system(f'yt-dlp -o "{destFolder}/%(upload_date>%Y-%m-%d)s - {name} Meeting.%(ext)s" {videoURL}')
            info["streams"][i]["prev-stream-id"] = str(meetingID)
    if updated:
        with open("settings.json", 'w') as settingsFile:
            json.dump(info, settingsFile, indent=4)
        #    return

# url = "https://api.new.livestream.com/accounts/11220190/events/3725902/"
## Livestream IDs
##  City Council: 3725902
##  URA         : 3725864
##  Plan & Zone : 6554264
version = "0.0.5"
if __name__ == "__main__":
    ## Pull cached upload date
    ## Go through setup "wizard" if first run.
    if not os.path.isfile("settings.json"):
        import setup
        setup()
    else:
        ## Exported information looks like this:
        # {
        #   "dlFolder": "/srv/government",
        #   "accountID": "123456",
        #   "streams": {
        #       "stream-1": [{
        #           "id": "123456",
        #           "name": "City Council",
        #           "subFolder": "city-council",
        #           "prev-stream-id": "0",
        #       }].
        #    }
        #}
        with open("settings.json", "r") as settingsFile:
            info = json.load(settingsFile)
        infoParse(info)
