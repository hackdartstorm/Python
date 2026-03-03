# Write a python function which converts inches to cms


def inch_cm(n):
    inch = n * 2.54
    return inch


n = int(input("Enter the Number : "))
ch = inch_cm(n)
print(ch)
