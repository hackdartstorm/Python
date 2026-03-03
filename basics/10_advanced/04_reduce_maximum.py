"""
 Write a program to find the maximum of the numbers in a list using the reduce
function.
"""
from functools import reduce

numbers_list = [23, 23, 56, 87, 34, 776, 4443, 3, 33, 222, 533, 2, 22, 2]


def find_maximum(num1, num2):
    if num1 > num2:
        return num1
    elif num1 < num2:
        return num2
    elif num1 == num2:
        return num1
    else:
        pass


maximum_value = reduce(find_maximum, numbers_list)
print(maximum_value)

