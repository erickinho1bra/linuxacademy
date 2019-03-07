#/bin/bash
# demo of functions within a shell script structure

# script or global variable
CMDLINE=$1

#  function definitions - start

# displays a message
funcExample () {
  echo "This is an example"
}

# function definitions - stop

# beginning of the script
echo "This is the start.. "

funcExample

# end of the script
