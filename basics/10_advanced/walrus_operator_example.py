# Normal
while True:
    user_number = int(input("Enter the Number : "))
    if user_number == 3:
        print(user_number)
        break

# Using Walrus
while (user_number := int(input("Enter the Number : "))) != 3:
    continue
print(user_number)

# Using Walrus Operator
while (user_number := int(input("Enter the Number : "))) != 3:
    pass
print(user_number)
