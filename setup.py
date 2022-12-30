## Setup file. Is called from the main Meeting Grabber.py, but could probably be ran standalone.

## Exported information looks something like:
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
import os, json
try:
    import requests
except:
    print("Unable to import 'requests' package. Please install via pip!")
    exit()

def getFolder(defaultMainFolder):
    configDir = input(
        f"Where do you want the files to be downloaded to? [default: {defaultMainFolder}]\n\t=> "
    )
    if configDir == "":
        configDir = defaultMainFolder
    print(f"\tOkay, will download and serve files from {configDir}")

    if not os.path.isdir(configDir):
        try:
            os.mkdir(configDir)
        except PermissionError:
            retry = input(f"Unable to create folder {configDir}. Would you like to try again?[Y/n]")
            if retry.lower() in ["", "y", "yes"]:
                getFolder(defaultMainFolder)
            else:
                print("Please check your folder's settings and try again.")
                exit()
    return configDir

def init():
    ## Initialize new dictionary to insert JSON data into
    info = {}
    ## Get some basic information about the system
    homeFolder = os.path.expanduser("~")
    if "vm" in os.popen("hostnamectl | grep Chassis").read():
        print("Running in a VM, probably a server?")
        defaultMainFolder = "/srv/GVT Meeting Archive"
    else:
        print("Assuming we're running on a PC")
        defaultMainFolder = f"{homeFolder}/GVT Meeting Archive"
    ## Get the desired folder from the User and add it to the empty dictionary above
    configDir = getFolder(defaultMainFolder)
    info["dl-dir"] = configDir

    ## I'd like to break out the following part into its own function, but I don't know if it's worth it
    ## Keeping for now.
    ## In my case, I want to follow 3 feeds, but others may want to follow a different number. This allows for that.
    feeds = input("How many feeds do you want to follow?\n\t=> ")
    ## TODO: Break this into a try-except case? Is it worth it?
    if int(feeds):
        print(f"\tOkay, let's set up your {feeds} feeds.")

    streams = {}
    for feed in range(1, int(feeds)+1):
        feedURL = input("Please enter the livestream.com url of the feed you wish to follow\n\t=> ")
        ## Split the url into different chunks
        feedSplit = str(feedURL).split("/")
        ## URL will look something like [... "accounts", "123456", "events", "654321"]
        ## This looks for each, and assigns the number to a variable for use later
        account = feedSplit[feedSplit.index("accounts") + 1]
        event = feedSplit[feedSplit.index("events") + 1]
        print(f"\tReceived account number {account} and event {event}")

        ## We really only need the account ID from the first link,
        ## so we'll send it to our dictionary from earlier
        if feed == 1: info["account-id"] = account
        ## Replace bad characters or duplicate words with something more manageable
        ## and then make a foldername from the new name
        ## TODO: Maybe add a more robust filter list?
        feedName = requests.get(feedURL).json()["full_name"].replace("&", "and").replace(" Meetings", "")
        subFolder = feedName.lower().replace(" ", "-")
        print(f"\tReceived feed name of {feedName} and downloading into {configDir}/{subFolder}")
        ## send the new information to the dictionary above
        streams[f"stream-{str(feed)}"] = {"id": event, "name": feedName, "sub-folder": subFolder, "prev-stream-id": "0"}

    info["streams"] = streams
    ## We have all the inforamation we need, now we can write it to the file
    with open("settings.json", "a") as settingsFile:
        json.dump(info, settingsFile, indent=4)
    ## Verifying the write was correct
    ## TODO: initialize the folders?
    if os.path.isfile("settings.json"):
        print("Data written successfully to `settings.json`, you should be all set!")
        exit()
print("Settings File (settings.json) not found!")
createFile = input("Would you like to create one? [Y/n]\n\t=> ")

if createFile.lower() in ["", "yes", "y"]:
    init()
else:
    print("Okay, quitting!")
    exit()
