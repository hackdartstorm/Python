"""  Tuple <Note that Tuple is Immutable !>  """

trytup = () #Blank Tuple
print(type(trytup)) #Check the type of the variable 
print(trytup) #Prints the Blank Tuple


t1 = ("Hello","12345",False,"Ram","Ram") #tuple1
t2 = (1222.22,False,24224.4224,"String") #tuple2
print(t1.count("Hello")) #--> Return number of occurrences of value.
print(t1.index("Ram")) #-->Return first index of value.
print(len(t1)) #-->Return the number of items in a container.
print(t1 + t2) #-->Concatenation of two tuples 