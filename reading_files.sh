#!/bin/bash
# this is a script that looks for a file called "superheroes.txt", asks if you want to read that file, if not, asks what file you want to read, and then prints out each line seperately

line_num=1

if [ -f superheroes.txt ] ; then
  read -p "Would you like to print out the lines of 'superheroes.txt'? (y or n) " read_response
  if [ "$read_response" == "y" -o "$read_response" == "yes" ] ; then
    printf "Reading 'superheroes.txt'\n"
    file_to_read="superheroes.txt"
    while read line ; do
      printf "%s\n" "Line $line_num: $line"
      let "line_num++"
    done < "$file_to_read"
  elif [ "$read_response" == "n" -o "$read_response" == "no" ] ; then
    read -p "What file would you like to read?  " file_to_read
    echo "Reading $file_to_read"
    while read line ; do
      printf "%s\n" "Line $line_num: $line"
      let "line_num++"
    done < "$file_to_read"
  fi
fi

