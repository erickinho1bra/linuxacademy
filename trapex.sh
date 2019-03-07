#!/bin/bash
# script to demonstrate trap signals

clear

trap 'echo " - Please Type Q to Exit"' SIGTERM SIGINT

while [ "$CHOICE" != "Q" ] && [ "$CHOICE" != "q" ] ; do
  clear
  echo "Main Menu"
  echo "====="
  echo "1) Choice One"
  echo "2) Choce Two"
  echo "Q) Quit"
  echo
  read CHOICE
done
