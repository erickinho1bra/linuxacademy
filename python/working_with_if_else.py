#!/usr/bin/env python3.6

user = {'admin': True, 'active': False, 'name': 'Erick'}
prefix = ""

if user['admin'] == True and user['active'] == True:
    prefix = "ACTIVE - (ADMIN) "
elif user['admin'] == True and user['active'] == False:
    prefix = "(ADMIN) - NOT ACTIVE"
elif user['admin'] == False and user['active'] == True:
    prefix = "NOT (ADMIN) - ACTIVE"
elif user['admin'] == False and user['active'] == False:
    prefix = "NOT (ADMIN) - NOT ACTIVE"

print(f"{prefix} {user['name']}")
