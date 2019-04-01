#!/bin/bash
# script to demonstrate error handling with exit

echo "Change to a directory and list the contents"
DIRECTORY=$1

cd $DIRECTORY 2>/dev/null

if [ "$?" = "0" ] ; then
  echo "We can change into the directory $DIRECTORY, and here are the contents"
  echo "`ls -l`"
else
  echo "Cannot change directories, exiting with an error and no listing"
  exit 1
fi
