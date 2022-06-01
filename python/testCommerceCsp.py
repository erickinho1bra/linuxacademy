#!/usr/bin/env python3

import requests, signal, sys

# function that handles CTRL+C
def signal_handler(signal, frame):
    # print a blank nothing to make prompt go to next line
    print("")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)




domains=["looneytunes.com", "dccomics.com"]
subdomains=["shop", "cms"]
environments=["", "-staging", "-dev"]

searchString = input("What string do you want to search for from the CSP headers on all Commerce shops and environments? ")

successSites = []
errorSites = []

for domain in domains:
    for subdomain in subdomains:
        for environment in environments:
            site = "https://" + subdomain + environment + "." + domain
            if "cms-dev" in site:
                pass
            else:
                print("Testing site: " + site)
                r = requests.get(site, stream=True)
                headers = r.headers.get('Content-Security-Policy', default=None)
                if searchString in headers:
                    successSites.append(site)
                else:
                    errorSites.append(site)


print("\n\n***RESULTS***") 
print("\nSites WITH the string \'" + searchString + "\'.")
for site in successSites:
    print(site)
print("\nSites WITHOUT the string \'" + searchString + "\'.")
for site in errorSites:
    print(site)
