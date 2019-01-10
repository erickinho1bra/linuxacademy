#!/usr/bin/env python3.7

import os, sys

newFile = input("What do you want to call your new file (e.g. cars.txt)? ")

message = ""

while message != "":
    message = input('Give me da message: ')
    f = open(f'{newFile}', 'a+')
    f.write(f'{message}\n')
else:
    print(f'I finished writing your file ', '{newFile}')
