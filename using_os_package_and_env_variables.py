#!/usr/bin/env python3.6

import math

pi = math.pi
floaty = input("What decimal place would you like to take pi to? ").strip()

if floaty:
    floaty = int(floaty)
else:
    floaty = 30

print(round(pi, floaty))
#print("%.*f" % (pi, floaty))
