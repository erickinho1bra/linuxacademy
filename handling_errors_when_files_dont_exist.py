#!/usr/bin/env python3.6
# this is a file that prints a requested line of a requested filer

import argparse, sys

parser = argparse.ArgumentParser(description='Read a line of a file')
parser.add_argument('--filename', '-f', help='the file to read')
parser.add_argument('--linenumber', '-l', type=int, help='the line number to read')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 2.0')

