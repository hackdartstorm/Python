# 5. Write a program to find the sum of first n natural numbers using while loop.

limit = int(input("Enter the Number : "))
counter = 1
total_sum = 0
while counter < limit + 1:
    total_sum += counter
    counter += 1
print(total_sum)
