#!/bin/bash

##### Variable definition - start

# function to commit changes and push to master git branch
funcComAndPush () {
  git commit -a -m "$COMMESS" 1>/dev/null
  git push origin master
}

##### Variable definitions - stop


##### Script - start

# Stage changes you want to commit
git add .

read -p "What do you want your commit message to be? " COMMESS

# Prompt user for git commit message
if [ "$COMMESS" != "" ] ; then
  echo "Commiting with message: $COMMESS "
else
  COMMESS="Auto commit to github"
  echo "Using default commit message: $COMMESS"
fi

# Commit changes (if any)
git commit -a -m "$COMMESS" 1>/dev/null

# Record exit code
COMSTATUS=`echo $?`

# Commit depending on whether there are changes to the repository
if [ "$COMSTATUS" == "1" ] ; then
  echo "Nothing to commit!"
  while [ "$COMDECISION" == "" ] ; do
    read -p "Would you like to force a commit? (Y or N) " COMDECISION
    if [ "$COMDECISION" == "Y" ] || [ "$COMDECISION" == "y" ] ; then
      echo "Forcing commit"
      funcComAndPush
    elif [ "$COMDECISION" == "N" ] || [ "$COMDECISION" == "n" ] ; then
      echo "Not forcing commit"
      exit 1
    fi
  done
else
  echo "Committing files (not sins)"
  funcComAndPush
fi
