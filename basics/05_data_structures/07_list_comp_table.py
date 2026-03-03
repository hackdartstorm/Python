"""
Write a list comprehension to print a list which contains the multiplication table of a
user entered number.
"""

number = int(input("Enter the n : "))
multiplication_table = [multiplier * number for multiplier in range(11)]
print(f"{multiplication_table}")
