#!/usr/bin/env python3.6

arr1 = [1, 2, 3, 4, 7, 9]
arr2= [0, 1, 2, 1, 1, 4]
new_list = []

count = 0
for n in arr1:
    for m in arr2:
        if n >= m:
            count += 1
    new_list.append(int(f'{count}'))
    count = 0

print(f'{new_list}')
