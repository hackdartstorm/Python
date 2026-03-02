"""Write a program to greet all the person names stored in a list 'l' and which starts
with S.
l = ["Harry", "Soham", "Sachin", "Rahul","Harish","Hetbe","rajesh","Harish Meheta"]"""


names_list = ["Harry", "Soham", "Sachin", "Rahul","Harish","Hetbe","rajesh","Harish Meheta"]
for name in names_list:
    if(name.startswith("H")):
        print(f"Greet Sended to {name}")
