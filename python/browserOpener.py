#!/usr/bin/env python3

import webbrowser
import io
import sys
import signal
from time import sleep

# function that handles CTRL+C 
def signal_handler(signal, frame):
    # print a blank nothing to make prompt go to next line
    print("")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


sites = ["ellentv.com",
"www.ellentv.com",
"ellentv.com",
"m.ellentv.com",
"games.ellentv.com",
"media.ellentv.com",
"tpix-media.ellentv.com",
"viggle.ellentv.com",
"ellentv-mail.com",
"www.ellentv-mail.com",
"ellentv-mail.com",
"widgets.ellentube.com",
"www-v2.ellentube.com",
"ellentube.com",
"www-2.ellentube.com",
"new.ellentube.com",
"www-new.ellentube.com",
"share.ellentube.com",
"www.ellentube-mail.com",
"ellentube-mail.com",
"ellentube-mail.com",
"photos.ellen.warnerbros.com",
"ellen.warnerbros.com",
"www.ellen.warnerbros.com"]

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
    if count == 5:
        input("Press enter to continue")
        count = 0