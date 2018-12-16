#!/bin/bash

read -p "What do you want your commit message to be? " COMMESS

# Prompt user for git commit message
if [ "$COMMESS" != "" ] ; then
  echo "Commiting with message: $COMMESS "
else
  COMMESS="Auto commit to github"
  echo "Using default commit message: $COMMESS"
fi

# Commit changes (if any)
git commit -a -m "$COMMESS"

# Record exit code
COMSTATUS=`echo $?`

# Commit depending on whether there are changes to the repository
if [ "$COMSTATUS" == "1" ] ; then
  echo "Nothing to commit!"
  exit 1
else
  echo "Committing files (not sins)"
  git commit -a -m "$COMMESS"
  git push origin master
fi

echo hi
