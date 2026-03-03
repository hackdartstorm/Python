"""Write a program to print the following star pattern.
   *
  ***
 *****
for n = 3"""

rows = int(input("Enter the Number : "))
for row in range(1, rows + 1):
    print(" " * (rows - row), end="")
    print("*" * (2 * row - 1), end="")
    print(" ")
