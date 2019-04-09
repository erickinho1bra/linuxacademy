#!/usr/bin/env python3.7
# this is a script that can read my emails

from getpass import getpass
import smtplib
import time
import imaplib
import email
import sys, signal

##### global variables - start

ORG_EMAIL   = "@gmail.com"
user  = "erickdalima" + ORG_EMAIL
imap_url = "imap.gmail.com"
SMTP_PORT   = 993

##### global variable - stop



##### function declerations - start

def get_body(msg):
  if msg.is_multipart():
    return get_body(msg.get_payload(0))
  else:
    return msg.get_payload(None,True)

def main(palavra):
 con = imaplib.IMAP4_SSL(imap_url)
 password = palavra
 con.login(user,password)
 con.select('INBOX')
 result, data = con.fetch(b'3','(RFC822)')
 raw = email.message_from_bytes(data[0][1])
 print(get_body(raw))

##### function declerations - stop



##### script - start


##### script - stop
