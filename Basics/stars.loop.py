"""Write a program to print the following star pattern.
* * *
*   *       for n = 3
* * *

"""

user = int(input("Enter the Number :"))
for i in range(1,user+1):
    if(i==1 or i==user):
        print(f"*"*user,end="")
    else:
        print(f"*",end="")
        print(f" "*(user-2),end="")
        print(f"*",end="")
    print("")