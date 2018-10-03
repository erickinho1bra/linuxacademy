#!/usr/bin/env python3.6

import argparse

parser = argparse.ArgumentParser(description='Search for words including partiona word')
parser.add_argument('snippet', help='partial (or complete) string to search for in words')

args = parser.parse_args()
snippet = args.snippet.lower()

with open('/usr/share/dict/words') as f:
    words = f.readlines()

print([word.strip() for word in words if snippet in word.lower()])
