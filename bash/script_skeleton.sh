#/bin/bash
# script that creates the skeleton to a well formated script

##### function declerations - start

# function to check if the file the user want to format is a new file or is an existing file, if not existing, it creates the file
# sets "exit status" to be used later
funcCheckFileExists () {
if [ -f $FILE_TO_FORM ] ; then
  echo "File \"$FILE_TO_FORM\" exists!"
  fCheck_File_Exists_Status="file_exists"
else
  echo "Creating file: $FILE_TO_FORM"
  touch "$FILE_TO_FORM"
  fCheck_File_Exists_Status="file_created"
fi
}

# function to check what content is in the file and display it to the user if they want to see it
funcCheckFileContent () {
  FILE_LINES=`wc -l "$FILE_TO_FORM"`

  echo "File $FILE_TO_FORM has $FILE_LINES lines"
  read -p "Would you like to see the first 10 lines of the file? " HEAD_RESPONSE
  if [ "$HEAD_RESPONSE" == "y" ] ; then
    echo ""
    echo "Below are the first 10 lines of $FILE_TO_FORM"
    head $FILE_TO_FORM
  elif [ "$HEAD_RESPONSE" == "n" ] ; then
    echo "Okaaay... moving onnn!"
  fi

}

#function to check if user wants to format file, then format it and make the file executable
funcFormatFile () {
  read -p "Would you like to format the script? (Answer y or n) " FORMAT_RESPONSE
  if [ "$FORMAT_RESPONSE" = "y" ] ; then
    echo "Formatting script!"
    cat ../text/script_template.txt >> $FILE_TO_FORM
    chmod 777 $FILE_TO_FORM
  elif [ "$FORMAT_RESPONSE" == "n"] ; then
    echo "NOT formatting script!"
  fi
}

# function to vim into the newly formatted file
funcVimFileToFormat () {
  echo "Vimming newly formatted file now!"
  sleep 2
  vim $FILE_TO_FORM
}

##### function declerations - stop

##### script - start

clear

read -p "What script would you like to format? " FILE_TO_FORM

funcCheckFileExists

if [ "$fCheck_File_Exists_Status" == "file_exists" ] ; then
  funcCheckFileContent
elif [ "$fCheck_File_Exists_Status" == "file_created" ] ; then
  echo "Created $FILE_TO_FORM"
  # call function that sees if they want to format the file and then formats it
  funcFormatFile
  funcVimFileToFormat
fi

##### script - stop
