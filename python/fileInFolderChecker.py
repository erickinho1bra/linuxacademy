# How to check if files in one directory/folder are in another directory/folder

import os

lstItemsPath="/Users/xelima/Documents/Fuji Delete Soon/100_FUJI/"
lstPath="/Volumes/Fuji 128/DCIM/100_FUJI/"

lstItems=os.listdir(lstItemsPath)
lst=os.listdir(lstPath)

for item in lstItems:
    if item in lst:
        print( "Yes", item)
    else:
        print("No", item)