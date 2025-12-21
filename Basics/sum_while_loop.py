# 5. Write a program to find the sum of first n natural numbers using while loop.

user = int(input("Enter the Number : "))
i = 1
sum = 0
while(i<user+1):
    sum += i
    i+=1
print(sum)