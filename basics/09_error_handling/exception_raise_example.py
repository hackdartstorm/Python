def divide_numbers(first_num: int, second_num: int) -> int:
    division_result = first_num / second_num
    return division_result


first_number = int(input("Enter the Number : "))
second_number = int(input("Enter the Number : "))
if second_number == 0:
    raise ZeroDivisionError("Hehe")
first_number = divide_numbers(first_number, second_number)
print(f"\nOutput : {round(first_number, 2)}")
