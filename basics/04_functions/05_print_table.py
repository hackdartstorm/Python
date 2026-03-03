# Write a python function to print multiplication table of a given number.
def print_table(number):
    multiplier = 1
    while multiplier < 11:
        print(f"{number} * {multiplier} = {number * multiplier} ")
        multiplier += 1


print_table(number=3)
