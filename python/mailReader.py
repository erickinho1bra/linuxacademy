#!/usr/bin/env python
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
FROM_EMAIL  = "erickdalima" + ORG_EMAIL
while True:
    FROM_PWD = getpass("What is your password? ")
    if FROM_PWD == "":
        print("You must enter a password!")
    else:
        break
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993


##### global variable - stop



##### function declerations - start

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[-2])
        latest_email_id = int(id_list[-1])


        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
    except Exception, e:
        print str(e)

##### function declerations - stop



##### script - start

read_email_from_gmail()

##### script - stop
