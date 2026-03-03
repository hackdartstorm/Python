# Write a program using functions to find greatest of three numbers.

def greatest(first_num, second_num, third_num):
    if(first_num >= second_num and first_num > third_num):
        return f"{first_num} is Greater among {second_num} and {third_num}"
    elif(second_num >= third_num and second_num >= first_num):
        return f"{second_num} is Greater among {first_num} and {third_num}"
    elif(third_num >= first_num and third_num >= second_num):
        return f"{third_num} is Greater among {first_num} and {second_num}"
    else:
        return f"Invalid Numbers : {first_num}{second_num}{third_num} "


count = 0
numbers_list = []
while True:
    number = int(input("Enter the Numbers : "))
    numbers_list.append(number)
    count += 1
    if count == 3:
        break
print(f"ok! I Found Your Numbers : {numbers_list}")
first_num = numbers_list[0]
second_num = numbers_list[1]
third_num = numbers_list[2]
result = greatest(first_num, second_num, third_num)
print(f"{result}")
