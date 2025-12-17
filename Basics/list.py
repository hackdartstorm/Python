#Lists
isFoods = ["biriyani","Panner",200,False,12,True,439895487.54879954,23.222,90,"ramji-krishnaji"] #Lists are mutable 
print(isFoods[0]) #Print the first item from the list 

#Mutability Check 
isFoods[0] = "radheradhe"
print(isFoods)
"""                                           
                                            Lists vs Strings
                                                                                                                             """
# Strings
isFood = "ramji"
print(isFood[0]) #Print the first item from the String

#Immutability Check
isFood[0] = "radhe2radhe" #error 
print(isFood)
