#!/usr/bin/env python
import csv, os
from datetime import datetime
from time import sleep
from subprocess import Popen
import stat



cols = ["Character Name", "Series Name", "Profession", "Age"]

rows = [["Mando", "Mandalorian", "Bounty Hunter", 35],
        ["Grogu", "Mandalorian", "Jedi Master", 50],
        ["Eleven", "Stranger Things", "Kid", 14],
        ["Jon", "Game of Thrones", "King", 30],
        ["Ross", "Friends", "Paleontologist", 35]]


userHome = os.path.expanduser('~')
currentDateTime = datetime.today().strftime('-%Y-%m-%d_%H:%M')
csvFileName = f"bigTestTime-{currentDateTime}.csv"
csvFilePath = userHome + "/Downloads/" + csvFileName

# Finally export query to CSV file
with open(csvFilePath, 'w') as f:
    write = csv.writer(f)
    write.writerow(cols)
    write.writerows(rows)

print("Your CSV file has been exported to " + csvFilePath + "!")
print("Opening file now...")
sleep(1)
os.system(f"chmod +x {csvFilePath} && open {csvFilePath}")