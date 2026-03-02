"""  Tuple <Note that Tuple is Immutable !>  """

empty_tuple = () #Blank Tuple
print(type(empty_tuple)) #Check the type of the variable
print(empty_tuple) #Prints the Blank Tuple


tuple1 = ("Hello","12345",False,"ram","ram") #tuple1
tuple2 = (1222.22,False,24224.4224,"String") #tuple2
print(tuple1.count("Hello")) #--> Return number of occurrences of value.
print(tuple1.index("ram")) #-->Return first index of value.
print(len(tuple1)) #-->Return the number of items in a container.
print(tuple1 + tuple2) #-->Concatenation of two tuples