#!/usr/bin/env python3.6

print("")

company = [
        { 'name': 'Erick', 'active': True, 'admin': True },
        { 'name': 'Carol', 'active': True, 'admin': False },
        { 'name': 'Mom', 'active': False, 'admin': True }
]

print('print(f"company")')
print(company)
print('print(company[1]["name"])')
print(company[1]['name'])
print()


for user in company:
#    print("User: ", user['name'],'\n',"  User is admin? ", user['admin'],'\n',"  Account is active? ", user['active'])
    print(user['name'])
    if user['admin'] == True:
        print('(ADMIN)')
