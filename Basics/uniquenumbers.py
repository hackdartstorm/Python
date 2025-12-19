#Write a program to input eight numbers from the user and display all the unique numbers (once).

s = set() #Empty Set 
i = input("Enter 8 Numbers :") #Takes Input 
num = i.split(" ").pop(0) 
s.add(num)
num = i.split(" ").pop(1) 
s.add(num)
num = i.split(" ").pop(2) 
s.add(num)
num = i.split(" ").pop(3) 
s.add(num)
num = i.split(" ").pop(4) 
s.add(num)
num = i.split(" ").pop(5) 
s.add(num)
num = i.split(" ").pop(6) 
s.add(num)
num = i.split(" ").pop(7) 
s.add(num) 
print(s) #print the Updated Set


