def divide_numbers(first_num: int, second_num: int) -> int:
    result = first_num / second_num
    return result


try:
    first_number = int(input("Enter the Number: "))
    second_number = int(input("Enter the Number: "))
    first_number = divide_numbers(first_number, second_number)
    print(f"\nOutput: {round(first_number, 2)}")

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
