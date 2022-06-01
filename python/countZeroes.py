#!/usr/bin/env python
string1 = "01000000000000000000000000010101011000000000000010"


def zeroCounter(stringToCheck):
    indexCount = 0
    zeroCountArray = []
    list1 = list((stringToCheck))
    for l in list1:
        #print(l)
        if l == '0':
            #print(l)
            #print(list1[indexCount + 1])
            zeroCount = 0
            try:
                while l == list1[indexCount + 1]:
                    #print("list1[", indexCount, "]")
                    zeroCount += 1
                    indexCount +=1
                    #print(zeroCount)
                indexCount += 1
                zeroCountArray.append(zeroCount)
            except IndexError:
                pass

    mostZerosInARaow = sorted(zeroCountArray)[-1]
    print("The most zeroes in a row is: ", mostZerosInARaow)

zeroCounter(string1)