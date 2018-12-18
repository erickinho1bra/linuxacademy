#!/bin/bash
# script to install browsh cli based web browser

clear

###### Variable definitions - start

CPU_ARCH=`lscpu | grep Architecture | gawk '{print $2}'`
FIREFOX_EXIST=`hash firefox 2>/dev/null ; echo $?`
BROWSH_URL_32BIT="https://github.com/browsh-org/browsh/releases/download/v1.4.12/browsh_1.4.12_linux_386.rpm"
BROWSH_URL_64BIT="https://github.com/browsh-org/browsh/releases/download/v1.4.12/browsh_1.4.12_linux_amd64.rpm"
BROWSH_RPM_32BIT="browsh_1.4.12_linux_386.rpm"
BROWSH_RPM_64BIT="browsh_1.4.12_linux_amd64.rpm"

###### Variable definitions - end



##### Fuction definitions- start

echo ""
echo "Welcome to the browsh installation script! (Script needs to be run as ROOT!)"
echo ""

# Function that checks if the necessary prerequisites are installed for browsh
funcCheckPreReq () {
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
  echo "Aborting script!"
  return 500
fi
}

# Funciton to install Firefox
funcFFInstall () {
  read -p "Would you like to install Firefox? (Answer Y or N - default is Y) " INSTALL_FF_RESP
  if [ "$INSTALL_FF_RESP" == "Y" ] || [ "$INSTALL_FF_RESP" == "y" ] || [ "$INSTALL_FF_RESP" == "" ] ; then
    echo "Installing Firefox!"
    yum install firefox -y   1>/dev/null
    FF_INSTALL_STATUS="`echo $?`"
    if [ "$FF_INSTALL_STATUS" == "0" ] ; then
      echo "Firefox has been successfully installed!"
    else
      echo "Firefox has NOT been successfully installed! Aborting script!"
      exit 1
    fi
  elif [ "$INSTALL_FF_RESP" == "N" ] || [ "$INSTALL_FF_RESP" == "n" ] ; then
    echo "NOT installing Firefox dependency. Aborting script!"
  fi
}

# Function to pull browh install and install it with RPM
funcBrInstall () {
if [ $CPU_ARCH == "x86_64" ] ; then
  echo "Pulling 64 bit browsh install file from browsh website!"
  wget $BROWSH_URL_64BIT
  echo "Installing RPM"
  rpm -Uvh $BROWSH_RPM_64BIT
elif [ $CPU_ARCH == "x86" ] ; then
  echo "Pulling 32 bit browsh install file from browsh website!"
  wget $BROWSH_URL_32BIT
  echo "Installing RPM"
  rpm -Uvh $BROWSH_RPM_32BIT
fi
}

# Function to handle error of Firefox not being installed, call function to install Firefox (if necessary), and call function to install browsh
funcPreReqAndBrInstall () {
fPRStatus="`echo $?`"
if [ "$fPRStatus" == "100" ] ; then
  echo "Firefox is installed already! Proceeding with browsh installation"
elif [ "$fPRStatus" == "101" ] ; then
  funcFFInstall
  funcBrInstall
elif [ "$fPRStatus" == "110" ] ; then
  echo "Firefox is installed already! Proceeding with browsh installation"
elif [ "$fPRStatus" == "111" ] ; then
  funcFFInstall
else
  echo "Something went wrong"
fi
}

###### Function definitions - stop


###### Script - start

# Function that checks if the necessary prerequisites are installed for browsh
funcCheckPreReq

# Function that installs browsh
funcPreReqAndBrInstall

###### Script - end


# wget https://github.com/browsh-org/browsh/releases/download/v1.4.12/browsh_1.4.12_linux_amd64.rpm
# rpm -Uvh browsh_1.4.12_linux_amd64.rpm


# wget
# rpm -Uvh browsh_1.4.12_linux_386.rpm
