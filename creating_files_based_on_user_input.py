<<<<<<< HEAD
#!/usr/bin/env python3.6
=======
#!/usr/bin/env python3.7
>>>>>>> e9ce1554c7cb8ee68498265c8f28104c05af85a3

import os, sys

newFile = input("What do you want to call your new file (e.g. cars.txt)? ")

message = " "

while message != "":
    message = input('Give me da message: ')
    f = open(f'{newFile}', 'a+')
    f.write(f'{message}\n')
else:
<<<<<<< HEAD
    print(f'I finished writing your file ', '{newFile}')
=======
    print('I finished writing your file: ', f'{newFile}')
>>>>>>> e9ce1554c7cb8ee68498265c8f28104c05af85a3
