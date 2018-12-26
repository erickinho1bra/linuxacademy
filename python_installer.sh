#!/bin/bash
# script to install python 3 (and set up bash and vim the way it should be set up)

##### global variables - start



##### global variable - stop



##### function declerations - start

# function to download packages you will need to start working with python 3

funcInstallPy3Dep () {
  yum groupinstall -y "development tools"
  yum install -y lsof wget vim-enhanced words which libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel expat-devel
}

# function to set up your git environment
funcGitSetup () {
  git config --global user.name "Erick Lima"
  git config --global user.email "erickdalima@gmail.com"
}

# function to copy bashrc file since you are about to change it and set up console looks cooler and is easier to work with
funcBashRCSetup () {
  cp ~/.bashrc ~/.bashrc.original
  curl https://raw.githubusercontent.com/linuxacademy/content-python3-sysadmin/master/helpers/bashrc -o ~/.bashrc
}

# function to copy vimrc file since you are about to change it and set up vim so it is easier to work with
funcVimRCSetup () {
  cp ~/.vimrc ~/.vimrc.original
  curl https://raw.githubusercontent.com/linuxacademy/content-python3-sysadmin/master/helpers/vimrc -o ~/.vimrc
}

#function to install python 3
funcPy3Install () {
  cd /usr/src
  wget http://python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz
  tar xf Python-3.6.4.tar.xz
  cd Python-3.6.4
  ./configure --enable-optimizations
  make altinstall
  sudo pip3.6 install --upgrade pip
}

##### function declerations - stop



##### script - start

funcInstallPy3Dep
funcGitSetup
funcBashRCSetup
funcVimRCSetup
funcPy3Install

##### script - stop
