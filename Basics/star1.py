"""Write a program to print the following star pattern:
*
**
*** for n = 3"""

user = int(input("Enter the Number :"))
for i in range(1,user+1):
    print("*" * i,end="")
    print("")
