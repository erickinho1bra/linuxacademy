#!/bin/bash
# delimiter example using IFS

read -p "Enter the filename you want to parse: " FILE
read -p "Enter the Delimiter: " DELIM

IFS="$DELIM"

while read -r CPU MEMORY DISK; do
  echo "CPU: $CPU"
  echo "Memory: $MEMORY"
  echo "Disk: $DISK"
done <"$FILE"
