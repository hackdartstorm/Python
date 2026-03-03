# List Slicing Questions

numbers_list = [10, 20, 30, 40, 50, 60, 70]  # QuestionNo1
print(numbers_list[5:1:-1])  # [60, 50, 40, 30]
print(numbers_list[-2:2:-2])  # [60, 40]
print(numbers_list[100:])  # Blank

numbers_list = [1, 2, 3, 4, 5]  # QuestionNo2
numbers_list[1:4] = [20, 30]  # SubQuestion1
print(numbers_list)  # [1, 20, 30, 5]
numbers_list[::2] = [100, 200, 300]  # SubQuestion2
print(numbers_list)  # [100, 200, 300, 4, 5]
