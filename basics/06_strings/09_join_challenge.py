"""
A list contains the multiplication table of 7. write a program to convert it to vertical
string of same numbers.
"""

multiplication_table = [str(7 * multiplier) for multiplier in range(1, 11)]
vertical_string = f"\n".join(multiplication_table)
print(vertical_string)
