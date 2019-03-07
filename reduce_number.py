#!/usr/bin/env python3.6

def reducenumber(x):
    while x != 1:
        if x % 2 == 0:
            print('good job')
            pass
        else:
            x -= 1


number = int(input("What number? "))
reducenumber(number)
