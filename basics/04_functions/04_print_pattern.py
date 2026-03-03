"""
Write a python function to print first n lines of the following pattern:
***
**               --> for n = 3
*

"""


# Type1
def pattern_recursive(rows):
    if rows == 0:
        return
    else:
        print("*" * rows)
        pattern_recursive(rows - 1)


result = pattern_recursive(3)


# Type2
def pattern_iterative(total_rows):
    for row in range(1, total_rows + 1):
        print(f"*" * ((total_rows + 1) - row))


total_rows = int(input("Enter the 'n' : "))
pattern_iterative(total_rows)
        