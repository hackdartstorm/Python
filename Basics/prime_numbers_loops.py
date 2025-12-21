# Write a program to find whether a given number is prime or not.
num = int(input("Enter a Number : "))
if(num <=0):
    prime = False
elif(num==2):
    prime = True
else:
    prime = True
    for i in range(2,int(num*0.5)+1):
        if((num%i)==0):
            prime = False
            break
    if(prime):
        prime = False
    else:
        prime = True
print(f"Is Prime Number :{prime}")
