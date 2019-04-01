#!/usr/bin/env python3.6

message = input('Message: ')
count = input('Count: ').strip()

if count:
    count = int(count)
else:
    count = 1

def messageRepeater(message, count):
    while count > 0:
        print(message)
        count -= 1

messageRepeater(message, count)
