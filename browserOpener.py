#!/usr/bin/env python3

#import webbrowser
import webbrowser

#sites = ["ellentube-mail.com","ellentube.com","ellentv-mail.com","ellentv.com","games.ellentv.com","m.ellentv.com","media.ellentv.com","new.ellentube.com","photos.ellen.warnerbros.com","share.ellentube.com","tpix-media.ellentv.com","viggle.ellentv.com","widgets.ellentube.com","www-2.ellentube.com","www-new.ellentube.com","www-v2.ellentube.com","www.ellen.warnerbros.com","www.ellentube-mail.com","www.ellentv-mail.com","www.ellentv.com"]

sites = ["ellentube-mail.com", "ellentube.com"]

#webbrowser.open('http://inventwithpython.com/')
for site in sites:
    website = "http://" + site
    webbrowser.open(website)