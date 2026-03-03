# Write a program to sum a list with 4 numbers.

# Complex Method

numbers_list = [12, 12, 12, 34]  # Empty List
"""
Pop each element and return its value & simultaneouly store for all four numbers and store in addlist Variable
"""
sum_result = numbers_list.pop() + numbers_list.pop() + numbers_list.pop() + numbers_list.pop()
print(f"Sum of Elements : {sum_result}")  # Print Addlist Variable
print(numbers_list)  # Print the Original List



#                                            Or

# Simple Build-In-Method

numbers_list = [12, 12, 12, 12, 12]
print(sum(numbers_list))
