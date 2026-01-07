"""Operators in Python can be overloaded using the following methods:
p1+p2 # p1.__add__(p2)
p1-p2 # p1.__sub__(p2)
p1*p2 # p1.__mul__(p2)
p1/p2 # p1.__truediv__(p2)
p1//p2 # p1.__floordiv__(p2)
Other dunder/magic methods in Python:
str__() # used to set what gets displayed upon calling str(obj)
__len__() # used to set what gets displayed upon calling.__len__() or len(obj)
"""

class Addition():
    def __init__(self,val):
        self.val = val

    def __add__(self,num):
        return self.val + num.val
    
i = Addition(1)
j = Addition(9)
print(i+j)
