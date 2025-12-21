# Write a program to print multiplication table of a given number using loops.

#Using ForLoops
user = int(input("Enter the number : ")) 
for i in range(10):
    print(f"{user} * {i+1} = {user*(i+1)} ")

i=1
#Using WhileLoops
user = int(input("Enter the number : ")) 
while(i<11):
    print(f"{user} * {i} = {user*i}")
    i = i+1
    
