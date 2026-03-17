# Addition of Two Numbers

while True:
    try:
        first_number = int(input("Enter the first number: "))
        break
    except ValueError:
        print("Invalid input! Please enter a valid integer (e.g., 10, -5)")

while True:
    try:
        second_number = int(input("Enter the second number: "))
        break
    except ValueError:
        print("Invalid input! Please enter a valid integer (e.g., 10, -5)")

sum = first_number + second_number

print(f"The sum of {first_number} and {second_number} is {sum}")