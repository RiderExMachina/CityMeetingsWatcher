import json
import requests
#url = "https://api.new.livestream.com/accounts/11220190/events/3725902/"

## Pull cached upload date
#with open("settings.json", "a") as settingsFile:
    
## Livestream IDs
##  City Council: 3725902
##  URA         : 3725864
##  Plan & Zone : 6554264

for code in ["3725902", "3725864", "6554264"]:
    url = f"https://api.new.livestream.com/accounts/11220190/events/{code}"

    data = requests.get(url).json()

    ## Get latest Upload
    latestMeeting = data["feed"]["data"][0]
    latestDate = data["feed"]["data"][0]["data"]["caption"]
