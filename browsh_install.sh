#!/bin/bash
# script to install browsh cli based web browser

clear

# Variable definitions - start

CPU_ARCH=`lscpu | grep Architecture | gawk '{print $2}'`
FIREFOX_EXIST=`hash firefox 2>/dev/null ; echo $?`

# Variable definitions - end

# Fuction definitions- start

echo ""
echo "Welcome to the browsh installation script!"
echo ""

# Function that checks if the necessary prerequisites are installed for browsh
funcPreReq () {
if [ $CPU_ARCH == "x86_64" ] ; then
  echo "CPU Architecture is 64bit ($CPU_ARCH)"
  if [ $FIREFOX_EXIST == "0" ] ; then
    echo "Firefox is installed"
    return 100
  else
    echo "Firefox is not installed"
    return 101
  fi
elif [ $FIREFOX_EXIST == "x86" ] ; then
  echo "CPU Architecture is 32bit ($CPU_ARCH)"
  if [ $FIREFOX_EXIST == "0" ] ; then
    echo "Firefox is installed"
    return 110
  else
    echo "Firefox is not installed"
    return 111
  fi
else
  echo "Could not determine CPU Architecture"
fi
}

# Function to insatll browsh
funcInstall () {
if [[ $fPRStatus == 101 ]] ; then
  echo "All good here"
else
  echo "Something went wrong"
fi
}

# Function definitions - stop

# Script - start

# Function that checks if the necessary prerequisites are installed for browsh
funcPreReq
fPRStatus=$?

funcInstall

# Script - end


# wget https://github.com/browsh-org/browsh/releases/download/v1.4.12/browsh_1.4.12_linux_amd64.rpm
# rpm -Uvh browsh_1.4.12_linux_amd64.rpm


# wget https://github.com/browsh-org/browsh/releases/download/v1.4.12/browsh_1.4.12_linux_386.rpm
# rpm -Uvh browsh_1.4.12_linux_386.rpm
