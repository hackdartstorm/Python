"""Write a program to print the following star pattern.
   *
  ***
 ***** 
for n = 3"""

num = int(input("Enter the Number : "))
for i in range(1,num+1):
    print(" "* (num-i), end="")
    print("*"* (2*i-1), end="")
    print(" ")