"""Write a program to greet all the person names stored in a list ‘l’ and which starts
with S.
l = ["Harry", "Soham", "Sachin", "Rahul","Harish","Hetbe","Rajesh","Harish Meheta"]"""


l = ["Harry", "Soham", "Sachin", "Rahul","Harish","Hetbe","Rajesh","Harish Meheta"]
for i in l:
    if(i.startswith("H")):
        print(f"Greet Sended to {i}")
