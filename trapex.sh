#!/bin/bash
# script to demonstrate trap signals

clear

<<<<<<< HEAD
trap 'echo " - Please Typte Q to Exit"' SIGTERM SIGINT
=======
trap 'echo " - Please Type Q to Exit"' SIGTERM SIGINT
>>>>>>> e9ce1554c7cb8ee68498265c8f28104c05af85a3

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
