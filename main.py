# == City Meeting Watcher script == #
## Watches Livestream.com accounts for updates
##  and pipes them through yt-dlp to archive them
## and then converts the videos to audio through ffmpeg

import json, os, logging, datetime

logging.basicConfig(filename=f"citymeetingwatcher{datetime.datetime.now().strftime('%Y-%m')}.log", encoding="utf-8", level=logging.INFO)

def relay(msg):
    print(msg)
    logging.info(msg)
try:
    import requests
except:
    relay("Unable to import 'requests' package. Please install via pip!")
    exit()

def checkFolders(destFolder):
    if not os.path.isdir(destFolder):
        relay(f"Unable to find {destFolder}. Creating...")
        os.mkdir(destFolder)
    else:
        return

def vidConvert(dlFolder):
    for folder in os.listdir(dlFolder):
        currentFolder = os.path.join(dlFolder, folder)
        audioFolder = os.path.join(currentFolder, "audio")
        checkFolders(audioFolder)

        for vid in os.listdir(f"{currentFolder}"):
            if ".mp4" in vid:
                audio = vid.replace("mp4", "mp3")
                if audio not in os.listdir(audioFolder):
                    infile = os.path.join(currentFolder, vid)
                    outfile = os.path.join(audioFolder, audio)
                    relay(f'\t\t\t- Converting "{vid}" to "{audio}"')
                    ## the -n flag automatically answers "no" to any prompts
                    os.system(f'ffmpeg -i "{infile}" -map 0 -map -0:v -af silenceremove=1:0:-30dB,volume=2 "{outfile}" -n')
                    relay("\t\t\t- Done!")
                #else:
                    #relay(f'\t\t\t- "{audio}" already exists, skipping!')

def updateCheck(account, event):
        url = f"https://api.new.livestream.com/accounts/{account}/events/{event}"
        data = requests.get(url).json()

        ## Get latest Upload
        latestMeeting = data["feed"]["data"][0]
        meetingID = latestMeeting["data"]["id"]
        return meetingID

def infoParse(info):
    relay("Loading data...")
    updated = False
    dlFolder = info["dl-dir"]
    account = info["account-id"]

    for i in info["streams"]:
        event = info["streams"][i]["id"]
        name = info["streams"][i]["name"]
        subFolder = info["streams"][i]["sub-folder"]
        prevMeeting = info["streams"][i]["prev-stream-id"]
        relay(f"\t- {name} ({event})")

        ## Make sure folder to download exists
        destFolder = os.path.join(dlFolder, subFolder)
        checkFolders(destFolder)
        ## Get newest meeting ID
        meetingID = updateCheck(account, event)

        if meetingID != prevMeeting:
            updated = True
            relay(f"\t\t- Looks like there was an update! (Current: {meetingID}, Previous: {prevMeeting})")
            videoURL = f"https://livestream.com/accounts/{account}/events/{event}/videos/{meetingID}"
            os.system(f'yt-dlp -o "{destFolder}/%(upload_date>%Y-%m-%d)s - {name} Meeting.%(ext)s" {videoURL}')
            info["streams"][i]["prev-stream-id"] = meetingID
        else:
            relay("\t\t- No update found.")
    relay("\t- Converting video to audio...")
    vidConvert(dlFolder)
    if updated:
        with open("settings.json", 'w') as settingsFile:
            json.dump(info, settingsFile, indent=4)
        relay("Updated settings.json file with new previous stream ID.")

version = "0.1.4"
if __name__ == "__main__":
    relay(f"- Started on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}")
    ## Pull cached upload date
    ## Go through setup "wizard" if first run.
    if not os.path.isfile("settings.json"):
        import setup
        setup()
    else:
        relay(f"Running script version {version}")
        with open("settings.json", "r") as settingsFile:
            info = json.load(settingsFile)
        infoParse(info)
    relay(f"- Started at {datetime.datetime.now().strftime('%Y-%B-%d at %H:%M')}")
