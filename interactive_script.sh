#!/bin/bash

clear

read -p "Hello, what is your first name? " FIRSTNAME
read -p "$FIRSTNAME, what a lovely name! What is your last name? " LASTNAME
read -p "Oh, the $LASTNAME family. Powerful people. And, lastly, how old are you? " USERAGE
RESPONSETOAGE=`expr "$USERAGE" - 5`
echo "Wow, you don't look a day under $RESPONSETOAGE!"

NEWAGE=`expr "$USERAGE" + 10`
echo "Well, $FIRSTNAME $LASTNAME, it looks like in 10 years you will be a whopping $NEWAGE years old!!"
