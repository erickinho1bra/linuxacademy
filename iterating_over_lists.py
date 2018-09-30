#!/usr/bin/env python3.6

print("")

count = 1
company = [
        { 'name': 'Erick', 'active': True, 'admin': True },
        { 'name': 'Carol', 'active': True, 'admin': False },
        { 'name': 'Mom', 'active': False, 'admin': True }
]

for user in company:
    print(count, user['name'])
    if user['admin'] == True:
        if user['active'] == True:
            print('\t', '(ADMIN) - Active')
        elif user['active'] == False:
            print('\t', '(ADMIN) - NOT Active')
    elif user['admin'] == False:
        if user['active'] == True:
            print('\t', 'NOT (ADMIN) - Active')
        elif user['active'] == False:
            print('\t', 'NOT (ADMIN) - NOT Active')
    count = count + 1


