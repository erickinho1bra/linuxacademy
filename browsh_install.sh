#!/bin/bash
# script to install browsh cli based web browser

clear

# Variable definitions - start

CPU_ARCH=`lscpu | grep Architecture | gawk '{print $2}'`
FIREFOX_EXIST=`hash firefox 2>/dev/null ; echo $?`

# Variable definitions - end

# Script - start

echo ""
echo "Welcome to the browsh installation script!"
echo ""

if [ $CPU_ARCH == "x86_64" ] ; then
  echo "CPU Architecture is 64bit ($CPU_ARCH)"
  if [ $FIREFOX_EXIST == "0" ] ; then
    echo "Firefox is installed"
  else
    echo "Firefox is not installed"
  fi
elif [ $FIREFOX_EXIST == "x86" ] ; then
  echo "CPU Architecture is 32bit ($CPU_ARCH)"
else
  echo "Could not determine CPU Architecture"
fi

# Script - end


# wget https://github.com/browsh-org/browsh/releases/download/v1.4.12/browsh_1.4.12_linux_amd64.rpm
# rpm -Uvh browsh_1.4.12_linux_amd64.rpm


# wget https://github.com/browsh-org/browsh/releases/download/v1.4.12/browsh_1.4.12_linux_386.rpm
# rpm -Uvh browsh_1.4.12_linux_386.rpm
