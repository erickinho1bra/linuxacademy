#/bin/bash
# script that creates the skeleton to a well formated script

##### function declerations - start

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

funcFormatFile () {
  read -p "Would you like to format the script? (Answer y or n) " FORMAT_RESPONSE
  if [ "$FORMAT_RESPONSE" = "y" ] ; then
    echo "Formatting script!"
    cat script_template.txt >> $FILE_TO_FORM
    chmod 777 $FILE_TO_FORM
  elif [ "$FORMAT_RESPONSE" == "n"] ; then
    echo "NOT formatting script!"
  fi
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
fi

##### script - stop
