def divide_numbers(numerator: int, denominator: int) -> float:
    division_result = numerator / denominator
    return division_result


num1 = int(input("Enter the Number : "))
num2 = int(input("Enter the Number : "))
if num2 == 0:
    raise ZeroDivisionError("Hehe")
division_result = divide_numbers(num1, num2)
print(f"\nOutput : {round(division_result, 2)}")
