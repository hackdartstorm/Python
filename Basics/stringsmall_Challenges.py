# Write a program to fill in a letter template given below with name and date.



#Technique One (Harder+fragile+Complex)
name = input("Enter Your Name : ")
date = input("Enter the Date like : DD/MM/YY ?\nUnderstand Enter :")
letter = '''
Dear <|Name|>,
You are selected!
<|Date|>
'''
vname = letter.replace("<|Name|>",name)
vdate = vname.replace("<|Date|>",date)
count = len(name) #Count for name length 
finalCount = 25 + count #Count for name 
out = vname[:finalCount]
fdate = vdate[finalCount:]
# print(fdate)
# print(out)
print(out,fdate)


#Simple And Easiest Way 
name = input("Enter Your Name: ")
date = input("Enter the Date (DD/MM/YY): ")

letter = '''
Dear <|Name|>,
You are selected!
<|Date|>
'''

lname = letter.replace("<|Name|>",name)
ldate = lname.replace("<|Date|>",date)
print(ldate)
