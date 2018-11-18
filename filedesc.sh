#!/bin/bash
# script to show how file descriptors work

read -p "What file would you like to read? " FILENAME

exec 5<>$FILENAME

while read -r SUPERHERO; do
  echo "Superhero Name: $SUPERHERO"
done <&5

echo "File read on `date`" >&5

exec 5>&-
