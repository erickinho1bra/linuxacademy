#!/bin/bash
# example of trapping events and limiting the shell stopping

clear

trap 'echo " - Please Press Q to Exit.."' SIGINT SIGTERM SIGTSTP

while [ "$CHOICE" != "Q" ] && [ "$CHOICE" != "q" ]; do
  echo "MAIN MENU"
  echo "========"
  echo "1) Choice One"
  echo "2) Chose Two"
  echo "Q) Quit/Exit"
  echo ""
  read CHOICE

  clear
done
