#!/bin/bash
# script to install python 3 (and set up bash and vim the way it should be set up)

##### global variables - start

MENUBOX=${MENUBOX=dialog}

##### global variable - stop



##### function declerations - start

# function to download packages you will need to start working with python 3

funcInstallPy3Dep () {
  yum groupinstall -y "development tools"
  yum install -y lsof wget vim-enhanced words which libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel expat-devel
}

# function to set up your git environment
funcSetupGit () {
  git config --global user.name "Erick Lima"
  git config --global user.email "erickdalima@gmail.com"
}

# function to copy bashrc file since you are about to change it and set up console looks cooler and is easier to work with
funcSetupBashRC () {
  cp ~/.bashrc ~/.bashrc.original
  curl https://raw.githubusercontent.com/linuxacademy/content-python3-sysadmin/master/helpers/bashrc -o ~/.bashrc
}

# function to copy vimrc file since you are about to change it and set up vim so it is easier to work with
funcSetupVimRC () {
  cp ~/.vimrc ~/.vimrc.original
  curl https://raw.githubusercontent.com/linuxacademy/content-python3-sysadmin/master/helpers/vimrc -o ~/.vimrc
}

#function to install python 3
funcInstallPy3 () {
  cd /usr/src
  wget http://python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz
  tar xf Python-3.6.4.tar.xz
  cd Python-3.6.4
  ./configure --enable-optimizations
  make altinstall
  sudo pip3.6 install --upgrade pip
}

# function to display dialog menu
funcDisplayDialogMenu () {
  $MENUBOX --title "[ M A I N  M E N U ]" --menu "Use UP/DOWN arrows to Move and Select or the Number of Your Choice and Enter" 15 45 5 1 "Set up git user info" 2 "Set up bash rc file" 3 "Set up vm rc file" 4 "Install Python 3 and its dependencies" X "Exit" 2>/tmp/pychoice.txt
}

##### function declerations - stop



##### script - start

funcDisplayDialogMenu

case "`cat /tmp/pychoice.txt`" in
  1)
    echo "Setting up Erick\'s github user account info!"
    funcSetupGit ;;
  2)
    echo "Setting up bash.rc file"
    funcSetupBashRC ;;
  3)
    echo "Setting up vim.rc file"
    funcSetupVimRC ;;
  4)
    echo "Installing Python 3 and its dependencies"
    funcInstallPy3Dep
    funcInstallPy3;;
  X) echo "Exiting!"
esac

rm -rf /tmp/pychoice.txt

##### script - stop
