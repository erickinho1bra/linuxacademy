#!/bin/bash
# demo of a dialog box that will display a menu

##### global variables - start

MENUBOX=${MENUBOX=dialog}

##### global variable - stop



##### function declerations - start

# function to display a simple menu
funcDisplayDialogMenu () {
  $MENUBOX --title "[ M A I N  M E N U ]" --menu "Use UP/DOWN Arrow to Move and Select or the Number of Your Choice and Enter" 15 45 4 1 "Display Hello World" 2 "Display Goodbye World" 3 "Display Nothing" X "Exit" 2>choice.txt
}

##### function declerations - stop



##### script - start

funcDisplayDialogMenu

case "`cat choice.txt`" in
  1) echo "Hello World" ;;
  2) echo "Goodbye World" ;;
  3) echo "Nothing" ;;
  X) echo "Exit" ;;
esac

##### script - stop
