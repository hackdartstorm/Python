#List Methods 
mylist = ["ram","gyan",1111.222,444,"33","Ramit sioeo","ram","ram"]
mylist.append("sita gita") #Append object to the end of the list.
b = mylist.count("ram")#Return number of occurrences of value.
c = mylist.extend("slice")#Extend list by appending elements from the iterable.
d = mylist.index("ram") #Return first index of value.
e = mylist.insert(1,"sita")#Insert object before index.
f = mylist.pop(2)#Remove and return item at index (default last).
g = mylist.remove("ram") #Remove first occurrence of value.
z = mylist.reverse() #reverse the list
abcd = mylist.sort() #Sort the list in ascending order and return None.
print(b,d,mylist,f) #print and return value (if possible)