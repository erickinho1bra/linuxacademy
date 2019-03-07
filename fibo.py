#!/usr/bin/env python3.6

def fib (n, z):
    m = 1
    while n < z:
        print(n)
        n, m = m, m + n
z = int(input('what would you like the fibo sequence to go till? '))

fib(0, z)
