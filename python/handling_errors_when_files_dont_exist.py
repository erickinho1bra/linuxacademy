#!/usr/bin/env python3.6
# this is a file that prints a requested line of a requested filer

import os, argparse, sys

parser = argparse.ArgumentParser(description='Read a line of a file')
parser.add_argument('--filename', '-f', help='the file to read')
parser.add_argument('--linenumber', '-l', type=int, help='the line number to read')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 2.0')
args = parser.parse_args()
#file_name = input("What file would you like to read a line from? ").strip()
file_name = args.filename

# see if file is in current directory
fh = os.path.isfile(f'{file_name}')
try:
    f = open(f'{file_name}', 'r')
except FileNotFoundError as f:
    print(f'\tError: {f}')
    sys.exit(2)
else:
    fh = os.path.isfile(f'{file_name}')
    print(f'Working with file "{file_name}"')
    # check file length
    flen = len(open(f'{file_name}').readlines())
    file_length = flen - 1
    # get user input on what line they would like to read
    print(f'The file "{file_name}" has {file_length} lines')
    #line_number = int(input(f"What line would you like to read from {file_name}? "))
    line_number = args.linenumber
    # check if the line they want to read exists in file
    if line_number <= file_length:
        #print('You chose a valid number')
        arr = f.readlines()
        line = arr[line_number]
        print(f'Line {line_number} of "{file_name}" file says: {line}')
    else:
        print('The number you have me is too high')
