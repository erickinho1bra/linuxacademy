#!/bin/bash
# demo of functional parameter passing

#global variable
USERNAME=$1

# function definitions - start

# calculate age in days
funcAgeInDays () {
  echo "Hello $USERNAME, you are $1 years old."
  echo "That makes you approximately `expr $1 \* 365` days old"
}

# function definitions - stop

# script - start

clear

read -p "Enter your age: " USERAGE

# calculate age in days
funcAgeInDays $USERAGE

# script - stop
