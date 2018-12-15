#!/bin/bash

git add .

read -p "What do you want your commit message to be? " COMMESS

if [ "$COMMESS" != "" ] ; then
  echo "Commiting with message: $COMMESS "
else
  COMMESS="Auto commit to github"
  echo "Using default commit message: $COMMESS"
fi

if [ "`git commit -m "$COMMESS" ; echo $?`" == "1" ] ; then
  echo "Nothing to commit!"
  exit 1
else
  echo "Committing files (not sins)"
  git commit -m "$COMMESS"
  git push origin master
fi

