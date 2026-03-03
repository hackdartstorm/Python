"""Write a program to print the following star pattern.
* * *
*   *       for n = 3
* * *

"""

size = int(input("Enter the Number :"))
for row in range(1, size + 1):
    if row == 1 or row == size:
        print(f"*" * size, end="")
    else:
        print(f"*", end="")
        print(f" " * (size - 2), end="")
        print(f"*", end="")
    print("")
