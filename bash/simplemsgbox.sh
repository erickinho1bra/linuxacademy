#!/bin/bash
# demo of a message box with an ok button

##### global variables - start

MSGBOX=${MSGBOX=dialog}
TITLE="Default"
MESSAGE="Some Message"
XCOORD=10
YCOORD=20

##### global variable - stop



##### function declerations - start

# display the message box with our message
funcDisplayMsgBox () {
  $MSGBOX --title "$1" --msgbox "$2" "$3" "$3"
}

##### function declerations - stop



##### script - start

if [ "$1" == "shutdown" ] ; then
  funcDisplayMsgBox "WARNING!" "Please press OK when you are ready to shutdown the system" "20" "20"
  echo "Shutting down now!"
else
  funcDisplayMsgBox "Boring..." "You are not asking for anything fun..." "10" "20"
fi

##### script - stop
