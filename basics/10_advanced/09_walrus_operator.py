# Normal
while True:
    x = int(input("Enter the Number : "))
    if x == 3:
        print(x)
        break


# Using Walrus
while (x := int(input("Enter the Number : "))) != 3:
    continue
print(x)

# Using Walrus Operator
while (x := int(input("Enter the Number : "))) != 3:
    pass
print(x)
