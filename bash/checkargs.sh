#!/bin/bash
# script to check command line parameters

##### global variables - start



##### global variable - stop



##### function declerations - start



##### function declerations - stop



##### script - start

if [ "$#" != "3" ] ; then
  echo "USAGE: checkargs.sh [parm1] [parm2] [parm2]"
  exit 300
fi

echo "I live! I got what I needed!"

##### script - stop
