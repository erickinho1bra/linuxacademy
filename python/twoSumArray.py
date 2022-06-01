#!/usr/bin/env python
myArray = [1, 3, 5, 63, 11, 23, 32, 2, 4]
desiredSum = 9

for element in myArray:
    for secondElement in myArray:
        if element + secondElement == 9:
            elementIndex = myArray.index(element)
            secondElementIndex = myArray.index(secondElement)
            print(str(element) + " + " + str(secondElement) + " = " + str(desiredSum))
            print("' " + str(element) +"' and ' " + str(secondElement) + "' are in these spots respectively: myArray[" + str(elementIndex) + "] and myArray[" + str(secondElementIndex) + "]")
            exit()
