"""
1. Write a class "Calculator" capable of finding square, cube and square root of a number.
"""

class Calculator:
    def __init__(self, choose, num):
        self.choose = choose
        self.num = num

    def square(self, num):
        self.num = num
        num = num ** 2  # For Square
        result = round(num, 2)
        print(f"Here is Your Square: {result}")

    def cube(self, num):
        self.num = num
        num = num ** 3  # For Cube
        result = round(num, 2)
        print(f"Here is Your Cube: {result}")

    def square_root(self, num):
        self.num = num
        num = num ** 0.5  # For Square Root
        result = round(num, 2)
        print(f"Here is Your SquareRoot: {result}")

    @staticmethod
    def wrong():
        print("Wrong Number!")


choose = int(input("\n\t\tYour Calculator!\nType 1 for Square\nType 2 for Cube\nType 3 for SquareRoot\n\nType Your Choice: "))
Number = int(input("Enter the Number: "))
num = Calculator(choose, Number)

if choose == 1:
    num.square(Number)
elif choose == 2:
    num.cube(Number)
elif choose == 3:
    num.square_root(Number)
else:
    num.wrong()
