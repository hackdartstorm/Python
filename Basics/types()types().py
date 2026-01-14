#Maybe the Program not work but you just see the types like how union used in the program by import typing

from typing import List, Union, Tuple
def sum(a:Union[int,str],b:int) -> int:
    sum = a+b
    return sum
a = sum(2,3)
print(a)



n : int = 5
name: str = "Harry"
def  sum(a: int, b: int) -> int:
    return a+b