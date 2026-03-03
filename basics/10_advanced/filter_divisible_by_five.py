"""
Write a program to filter a list of numbers which are divisible by 5.
"""

numbers_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def is_divisible_by_five(number):
    if (number % 5) == 0:
        return True
    return False


filtered_numbers = filter(is_divisible_by_five, numbers_list)
print(list(filtered_numbers))
