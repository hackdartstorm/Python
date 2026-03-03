def divide_numbers(numerator: int, denominator: int) -> float:
    result = numerator / denominator
    return result


try:
    num1 = int(input("Enter the Number: "))
    num2 = int(input("Enter the Number: "))
    division_result = divide_numbers(num1, num2)
    print(f"\nOutput: {round(division_result, 2)}")

except ZeroDivisionError:
    print("A Number Can't be Divide by Zero")

except ValueError:
    print("Enter a Valid Number!")

except Exception as error:
    print(error)

else:
    print("Else: Program Worked")

finally:
    print("Finally: I work all time")
