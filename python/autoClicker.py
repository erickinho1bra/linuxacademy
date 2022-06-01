#!/usr/bin/env python3

import pyautogui, signal, sys
import time
from time import sleep
from multiprocessing import Process
import multiprocessing

# function that handles CTRL+C
def signal_handler(signal, frame):
    # print a blank nothing to make prompt go to next line
    print("")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# function that shows a running clock in between clicks
def clock():
    while True:
        localtime = time.localtime()
        # formats the local times
        result = time.strftime("%I:%M:%S %p", localtime)
        # prints the local time
        print(result, end="", flush=True)
        # carriage return so it looks like a real clock with changing seconds
        print("\r", end="", flush=True)
        time.sleep(1)

# function to click on a specific area
def click():
    while True:
        place=(pyautogui.position())
        x = int(place[0])
        y = int(place[1])
        print("Let me click that (" + str(x) + ", " + str(y) +  ") coordinate for you, baybeh. Just wait 5 seconds!")
        pyautogui.click(x, y)
        sleep(5)


# main function handler
if __name__ == "__main__":
    # allows for multi-processing in this little script so that the functions can run simultaneously
    multiprocessing.set_start_method('spawn')
    # sets up the two processes
    p1 = Process(target = clock)
    p1.start()
    p2 = Process(target = click)
    p2.start()