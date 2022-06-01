#!/usr/bin/env python

import sys
def youSuck(num1, num2):
  sum = num1 + num2
  num1 = str(num1)
  num2 = str(num2)
  sum = str(sum)
  return("You suck! Also, " + num1 + " plus " + num2 + " equals " + sum)

def youSuck2(num1, num2):
  difference = num1 - num2
  num1 = str(num1)
  num2 = str(num2)
  difference = str(difference)
  return("You suck! Also, " + num1 + " minus " + num2 + " equals " + difference)

def youSuck3(num1, num2):
  product = num1 * num2
  num1 = str(num1)
  num2 = str(num2)
  product = str(product)
  return("You suck! Also, " + num1 + " times " + num2 + " equals " + product)

def youSuck4(num1, num2):
  if num2 == 0:
    return("Error: cannot divide by zero! That's how bad you suck at math, btdubs")
  else:
    dividend = num1 / num2
    num1 = str(num1)
    num2 = str(num2)
    dividend = str(dividend)
    return("You suck! Also, " + num1 + " divided by " + num2 + " equals " + dividend)

tellMeISuck = youSuck(float(sys.argv[1]), float(sys.argv[2]))
print(tellMeISuck)

tellMeISuck2 = youSuck2(float(sys.argv[1]), float(sys.argv[2]))
print(tellMeISuck2)

tellMeISuck3 = youSuck3(float(sys.argv[1]), float(sys.argv[2]))
print(tellMeISuck3)

tellMeISuck4 = youSuck4(float(sys.argv[1]), float(sys.argv[2]))
print(tellMeISuck4)