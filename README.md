# City Meeting Watcher

Version 0.1.1 watches one or more Livestream.com accounts/"events", downloads them using yt-dlp, and ffmpeg. Currently only works with Livestream.com.

### [Setup](#setup)
#### Linux
Install ffmpeg and pip using your package manager. Make sure it has the `silenceremove` function by running `fmpeg -hide_banner -filters | grep silenceremove`. You should be good if you get output that looks like `silenceremove     A->A       Remove silence`. If you do not get that output, see the Troubleshooting section.

#### First run wizard
Install the necessary dependencies using `pip -r requirements.txt` within the CityMeetingsWatcher folder.

The first time the script is ran, it will run a setup wizard in order to create a `settings.json` file. The contents should look something like this:

```
        {
          "dl-folder": "/srv/government",
          "account-id": "123456",
          "streams": {
              "stream-1": {
                  "id": "123456",
                  "name": "City Council",
                  "sub-folder": "city-council",
                  "prev-stream-id": "0",
              }.
           }
        }
```

Once the `settings.json` file is created, feel free to use `cron` or `systemd` timers to schedule running `main.py`. The SystemD files will be included here for convenience.

### [Running](#running)
Feel free to run the script after the wizard has been run to verify everything is working and prime the `prev-stream-id` entry in `settings.json`, otherwise I'd just let the system run the script on the timer.

### [Contributing](#contributing)
Contributions would be helpful. There are a few things I want to do with this script, including adding an archive mode that will archive more than just one video at a time, or a cleaning mode in case the script is being ran on a server with limited space (cough, cough). Please keep these in mind:

1. Python uses camelCase, but JSON uses kebab-case.
2. Please hardcode as few things as possible, doubly so if it could be traceable/potentially lead to doxxing.

### [Troubleshooting](#troubleshoot)
Q. I'm on Windows/Mac and I don't know/want to use Linux

A. There's not much I can do for you here. I don't have a Mac and I dislike coding on Windows, so my information is Linux only. Luckily, since the code is Python, everything should mostly be the same, and I'll accept PRs to update Documentation.

Q. Do you have plans to include other sites like Youtube or Facebook?

A. No, not at this time. My city uses Livestream, and because it has a public API, it works best for me.

Q. My version of ffmpeg didn't say it has the silenceremove feature

A. The best answer would be to update ffmpeg, as the silenceremove feature has been included in ffmpeg since 2015. If you're unable to do that for any reason, take out the `silenceremove=1:0:-30dB,` part of code on L#33 (this line will change as the script gets more updates)