#!/bin/bash
# delimter example script

read -p "What file would you like to read? " FILE
read -p "What delimiter would you like to use? " DELIM

IFS="$DELIM"

while read -r CPU MEMORY DISK;
do
  printf "CPU: $CPU \n"
  printf "Memory: $MEMORY \n"
  printf "Disk: $DISK \n"
done < "$FILE"
