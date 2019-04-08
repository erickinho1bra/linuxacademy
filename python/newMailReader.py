#!/usr/bin/env python3.7
# this is a script that can read my emails

from getpass import getpass
import smtplib
import time
import imaplib
import email
import sys, signal

##### global variables - start

# function that handles CTRL+C
def signal_handler(signal, frame):
    # print a blank nothing to make prompt go to next line
    print("")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

ORG_EMAIL   = "@gmail.com"
user  = "erickdalima" + ORG_EMAIL
while True:
    password = getpass("What is your password? ")
    if password == "":
        print("You must enter a password!")
    else:
        break
imap_url = "imap.gmail.com"
SMTP_PORT   = 993

##### global variable - stop



##### function declerations - start

def get_body(msg):
  if msg.is_multipart():
    return get_body(msg.get_payload(0))
  else:
    return msg.get_payload(None,True)

con = imaplib.IMAP4_SSL(imap_url)
con.login(user,password)
con.select('INBOX')

result, data = con.fetch(b'3','(RFC822)')
raw = email.message_from_bytes(data[0][1])
print(get_body(raw))

##### function declerations - stop



##### script - start


##### script - stop
