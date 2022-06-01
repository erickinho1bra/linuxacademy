''' 
This code is used when I combed through all my photos from a shoot and now want a way to get only those RAW files to a customer

How to use this file:
1. Export favorites to a designated empty folder (favoriteExportFolder)
2. Create a new empty folder that you will want your RAW files to go to (finalPhotosFolder)
3. Determine the path were all the photos are including photos that are NOT your favorites, aka your SD card (allPhotosFolder)
4. Change the values below
5. Run it 
'''
import os, shutil, time

# favoriteExportFolder = '<File path to where you exported low res favorites to>'
favoriteExportFolder = '/Users/xelima/Desktop/preEngagementPhotoDump'
listFavoriteExportFolder = os.listdir(favoriteExportFolder)
projectName = os.path.split(favoriteExportFolder)[1]
print(listFavoriteExportFolder)

# allPhotosFolder = '<File path to where ALL your photos are, aka your SD card>'
allPhotosFolder = '/Volumes/128 Adam/DCIM/101_FUJI/'
listAllPhotosFolder = os.listdir(allPhotosFolder)
print(listAllPhotosFolder)

# Photos will go to the "To Edit folder and backed up so the memoery card can be wiped"
toEditFolder = "/Users/xelima/Desktop/To Edit"
finalPhotosFolder = toEditFolder + '/' + projectName + '/'
finalJpegPhotosFolder = toEditFolder + '/final_' + projectName + '/'



# Cretae folder to export RAW files to
try:
    os.makedirs(finalPhotosFolder)
except FileExistsError:
    time.sleep(0.001)  # Prevent high load in pathological conditions
except:
    raise

# Create folder to export JPEG files to after editing them in Luminar
try:
    os.makedirs(finalJpegPhotosFolder)
except FileExistsError:
    time.sleep(0.001)  # Prevent high load in pathological conditions
except:
    raise



for photo in listFavoriteExportFolder:
    newFileNameJpg = os.path.splitext(photo)[0] + '.JPG'
    if newFileNameJpg in listAllPhotosFolder:
        base = os.path.splitext(photo)[0]
        rawFile = base + ".RAF"
        rawPathAndFile = allPhotosFolder + rawFile
        #print("rawFile = " + rawFile + "------------")
        #print("rawPathAndFile = " + rawPathAndFile + "------------")
        newPathAndFile = finalPhotosFolder + rawFile
        print("Copying RAW favorite (" + rawPathAndFile + ") file to other directory (" + newPathAndFile + ")")
        shutil.copyfile(rawPathAndFile, newPathAndFile)
    else:
        newFileNameJpeg = os.path.splitext(photo)[0] + '.jpeg'
        if newFileNameJpeg in listAllPhotosFolder:
            base = os.path.splitext(photo)[0]
            rawFile = base + ".RAF"
            rawPathAndFile = allPhotosFolder + rawFile
            print("Copying RAW favorite, " + rawFile + ", file to other directory")
            newPathAndFile = finalPhotosFolder + rawFile
            shutil.copyfile(rawPathAndFile, newPathAndFile)



