# For Loops
for i in range(1,11):
    print("Hello World",i)
print(f"Start of For Loop_____________________________\n")


l1 = ["ram",False,True,"Radhe","Gather",222222]
#For Lists
i=0
for i in l1:
    print(i)

for i in range(len(l1)):
    print(l1[i])
print(f"End of For Loop_____________________________Lists\n")


l2 = ("ram",False,True,"Radhe","Gather",222222)
#For Tuple
for i in range(len(l2)):
    print(l2[i])

for i in l2:
    print(i)
print(f"End of For Loop_____________________________Tuples\n")


l3 = "ram","Radhe","Gather"
# For Strings
for i in range(len(l3)):
    print(l3[i])

for i in l3:
    print(i)
print(f"End of For Loop_____________________________Strings\n")

#Using of Break , Continue and Pass
for i in range(11):
    if(i==5):
        break
    print(i)
print(f"End of For Loop_____________________________Break\n")
"""‘Continue’ is used to stop the current iteration of the loop and continue with the next
one. It instructs the Program to “skip this iteration”."""

for i in range(11):
    if(i==5):
        continue
    print(i)
print(f"End of For Loop_____________________________Continue\n")
"""‘Continue’ is used to stop the current iteration of the loop and continue with the next
one. It instructs the Program to “skip this iteration”."""

for i in range(11):
    if(i==5):
        pass   #pass is a null statement in python
print(f"End of For Loop_____________________________Pass\n")

# Else in forloop
for i in range(21):
    print(i)
else:
    print(" Printed till 21")
print(f"End of For Loop_____________________________Else\n")



# While Loops
i=1
while i<11:
    print("Hello World",i)
    i=i+1
print(f"End of While Loop_____________________________\n")



