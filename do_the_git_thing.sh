#!/bin/bash

git add .

read -p "What do you want your commit message to be? " COMMESS

if [ "$COMMESS" != "" ] ; then
  echo "Commiting with message: $COMMESS "
else
  COMMESS="Auto commit to github"
  echo "Using default commit message: $COMMESS"
fi

git commit -m "$COMMESS"
git push origin master
