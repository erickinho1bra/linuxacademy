#!/usr/bin/env python3.6

import os, sys

file_name = input("What file would you line to read a line from? ").strip()

#see if file exists in current directory
fh = os.path.isfile(f'{file_name}')
try:
    f = open(f'{file_name}', 'r')
except FileNotFoundError as f:
    print(f'\tError: {f}')
    sys.exit(2)
else:
    fh = os.path.isfile(f'{file_name}')
    print(f'\tWorking with file "{file_name}"')
    # check file length
    flen = len(open(f'{file_name}').readlines())
    file_length = flen - 1
    # get user input on what line they would like to read
    print(f'The file "{file_name}" has {file_length} lines')
    line_number = int(input(f"What line would you like to read from {file_name}? "))
    # check if file the line they want to read exists in file
    if line_number <= file_length:
        print('You chose a valid number')
        arr = f.readlines()
        line = arr[line_number]
        print(f'Line {line_number} of "{file_name}" file says: {line}')
    else:
        print('The number you gave me is too high')
