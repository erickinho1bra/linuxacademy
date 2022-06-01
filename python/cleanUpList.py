#!/usr/bin/env python

list1 = ['9    2021-12-24  18:32:01                                 /en-US/product/metallic-superman-funko       404']
newList = []
for element in list1[0].split(" "):
    if element:
        newList.append(element)

print(newList)