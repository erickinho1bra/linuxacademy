#!/usr/bin/env python3.7
# This is a script to send emails to folks

import smtplib
from getpass import getpass
import signal
import sys


##### global variables - start

# create object that stores smtp server info and port number
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

# default variable for sender and recipient email address
defaultSenderEmailAddress = "erickdalima@gmail.com"
defaultRecipientEmailAddress = "erickdalima@gmail.com"
defaultEmailSubject = "Test"
defaultEmailBody = "This is a test"

# function that handles CTRL+C 
def signal_handler(signal, frame):
    # print a blank nothing to make prompt go to next line
    print("")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

##### global variable - stop



##### function declerations - start



##### function declerations - stop



##### script - start

print("This is a program used to send email from a gmail address to anyone else!")

smtpObj.ehlo()
smtpObj.starttls()

senderEmailAddress = input("What is your email address? (Default: erickdalima@gmail.com) ")
if senderEmailAddress == "":
    senderEmailAddress = f"{defaultSenderEmailAddress}"

while True:
    senderEmailPassword = getpass("What is your password? ")
    if senderEmailPassword == "":
        print("You must enter a password!")
    else:
        break


try:
    smtpObj.login(f'{senderEmailAddress}', f'{senderEmailPassword}')
    pass
except:
    print("Something went wrong and we couldn't log in! Check email address and password and try again.")
    sys.exit(1)



recipientEmailAddress = input("Who do you want to email? (Default: erickdalima@gmail.com) ")
if recipientEmailAddress == "":
    recipientEmailAddress = f"{defaultRecipientEmailAddress}"

emailSubject = input("What is the subject of your email? (Default: idk) ") + "\n"
#if emailSubject == "":
#    emailSubject = "WTH?"

emailBody = input("What is the body of your email? (Default: This is a test) ")
if emailBody == "":
    emailBody = f"{defaultEmailBody}"

trueEmail = "Subject: "f'{emailSubject}'"\n "f'{emailBody}'""

smtpObj.sendmail(f'{senderEmailAddress}', f'{recipientEmailAddress}', f'{trueEmail}')


##### script - stop
