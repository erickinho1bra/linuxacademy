#/bin/bash
# demo of variable scop

# global variable declaration
GLOBALVAR="Globally Visible"

# function definition - start

# sample function for the function variable scope
funcExample () {
  # local variable
  LOCALVAR="Locally Visible"

  echo "From within the function, the variable is $LOCALVAR..."
}

# function definitions - stop

# script - start
clear

echo "This step happens first..."
echo
echo "GLOBAL variable = $GLOBALVAR (before the function call)"
echo "LOCAL variable = $LOCALVAR (before the function call)"
echo
echo "Calling Function - funcExample()"
echo

funcExample

echo
echo "Function has been called.."
echo

echo
echo "GLOBAL variable = $GLOBALVAR (after the function call)"
echo "LOCAL variable = $LOCALVAR (after the function call)"
echo
