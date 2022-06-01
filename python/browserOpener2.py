#!/usr/bin/env python3

import webbrowser
import time
import sys
import signal
import subprocess


count = 0

# function that handles CTRL+C 
def signal_handler(signal, frame):
    # print a blank nothing to make prompt go to next line
    print("")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

subprocess.call("./safariOsaScript")

while count < 1000:
    webbrowser.open_new('https://shop-origin-staging.dccomics.com')
    time.sleep(2)
    #webbrowser.open_new('https://shop-dev.dccomics.com')
    #time.sleep(4)
    count += 1
