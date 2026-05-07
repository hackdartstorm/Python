# Average of Two Numbers

while True:
    try:
        num1 = int(input("Enter first number: "))
        break
    except ValueError:
        print("Invalid input! Please enter a valid integer (e.g., 10, -5)")

while True:
    try:
        num2 = int(input("Enter second number: "))
        break
    except ValueError:
        print("Invalid input! Please enter a valid integer (e.g., 10, -5)")

average = (num1 + num2) / 2

print(f"The average of {num1} and {num2} is {average}")