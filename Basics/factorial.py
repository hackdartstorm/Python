# Write a program to calculate the factorial of a given number using for loop.
num = int(input("Enter a Number : "))
fact = 1
for i in range(1,num+1):
    fact =  fact * i
print(fact)
