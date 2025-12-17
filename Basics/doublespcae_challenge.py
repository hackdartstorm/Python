# 1.Write a program to detect double space in a string.
string = input("Enter a String : ")  #UserInput


"""if it returns -1 means there is no double space in the given string but,
                                                           if there is double space it returns teh index of the double space"""
print(string.find("  ")) 


#2.Write a program to Detect and Count double space in a string.

string1 = input("Enter a String : ")  #UserInput
finaloutput = string1.count("  ") #Counts the Spaces


#Print how many double-spaces occur's in the user-defined string1.
print(f"In Your String there is {finaloutput} double Spaces !") 


#3.Replace the double space from problem 3 with single spaces.

string1 = input("Enter a String : ")  #UserInput
finaloutput = string1.replace("  "," ") #Counts the double spaces and replace with single Spaces
print(finaloutput) #Prints the output 