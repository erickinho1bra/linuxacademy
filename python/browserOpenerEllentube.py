#!/usr/bin/env python3

import webbrowser
import sys
import signal

# function that handles CTRL+C
def signal_handler(signal, frame):
    # print a blank nothing to make prompt go to next line
    print("")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


sites = ["widgets.ellentube.com",
"ellentube.com",
"new.ellentube.com",
"www-new.ellentube.com",
"share.ellentube.com",
"share.ellentube.com/video/ellen-reveals-she-dated-brad-pitts-ex-girlfriend.html"]

#sites = ["ellentube-mail.com", "ellentube.com"]

count = 0
realCount = 0
openedSites = []
for site in sites:
    website = "http://" + site
    if website in openedSites:
        print("Duplicate found!")
        website = ""
    else:
        openedSites.append(f"{website}")
        count += 1
        realCount += 1
        print("------"f"{realCount}""------------"f"{website}""----------------------------")
        chrome_path = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome %s --incognito'
        webbrowser.get(chrome_path).open_new(site)
    if count == 6:
        input("Press enter to continue")
        count = 0
