#!/usr/bin/enc python

# Function to modify a string like "2022-02-20-13" into UTC time so that it looks like "2022-03-04-13"
def modifyDateTimeToUtc(dateTimeString):
  dateTimeList = list(dateTimeString.split("-"))
  dateTimeHourInt = int(dateTimeList[3])
  dateTimeHourUtcInt = int(dateTimeList[3]) + 8
  if dateTimeHourInt in (0, 1):
      dateTimeHourUtcString = "0" + str(dateTimeHourUtcInt)
  elif dateTimeHourInt in range(2, 16):
      dateTimeHourUtcString = str(dateTimeHourUtcInt)
  elif dateTimeHourInt in range(16, 24):
      dateTimeHourUtcString = "0" +str(dateTimeHourUtcInt - 24)
      dateTimeDayUtcInt = int(dateTimeList[2]) + 1
      dateTimeDayUtcString = str(dateTimeDayUtcInt)
      dateTimeList[2] = dateTimeDayUtcString
  dateTimeList[3] = dateTimeHourUtcString
  dateTimeStringUtc = "-".join(str(element) for element in dateTimeList)
  return dateTimeStringUtc

for i in range(0, 24):
  if i < 10:
      j = "0" + str(i)
      timeToConvert = f"2022-12-31-{j}"
  else:
      timeToConvert = f"2022-12-31-{i}"
  #print("Modifying: timeToConvert", timeToConvert)
  print(modifyDateTimeToUtc(timeToConvert))