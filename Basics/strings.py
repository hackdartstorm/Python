# String-Slicing

c = "Hello World"
print(c[-5:-1]) #Worl
print(c[6:10]) #Worl



print(c[:]) #Prints the Whole String
print(c[:10]) #If in the beginning there is blank then consider as Zero
print(c[0:]) #If in the end there is blank then consider as len-1

#With Skip
print(c[::2]) #HloWrd
print(c[2:-1:-3]) #Blank
print(c[::4]) #Hor
