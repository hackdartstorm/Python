#Write a program to accept marks of 6 students and display them in a sorted manner

s1 = int(input("Enter Your Marks  : "))
s2 = int(input("Enter Your Marks  : "))
s3 = int(input("Enter Your Marks  : "))
s4 = int(input("Enter Your Marks  : "))
s5 = int(input("Enter Your Marks  : "))
s6 = int(input("Enter Your Marks  : "))
l1 = []
l1.append(s1) 
l1.append(s2) 
l1.append(s3) 
l1.append(s4) 
l1.append(s5) 
l1.append(s6) 
l1.sort()
print(l1)
