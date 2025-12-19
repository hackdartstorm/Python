'''Question1.Create an empty dictionary. Allow 4 friends to enter their favorite language as
value and use key as their names. Assume that the names are unique.'''

# Answer Type 1
d1 = {}
Ram = input("""Syntax :-
            --Name-- --xxProgrammingLanguage--
Enter your Name with Your Favourite Programming Language : """).split(" ")
key = Ram[0]
val = Ram[1]
d1.update({key:val})
Shyam = input("""Syntax :-
            --Name-- --xxProgrammingLanguage--
Enter your Name with Your Favourite Programming Language : """).split(" ")
key = Shyam[0]
val = Shyam[1]
d1.update({key:val})
Gita = input("""Syntax :-
            --Name-- --xxProgrammingLanguage--
Enter your Name with Your Favourite Programming Language : """).split(" ")
key = Gita[0]
val = Gita[1]
d1.update({key:val})
Ritu = input("""Syntax :-
            --Name-- --xxProgrammingLanguage--
Enter your Name with Your Favourite Programming Language : """).split(" ")
key = Ritu[0]
val = Ritu[1]
d1.update({key:val})
print(d1)

# Answer Type 2

Ram = input("Enter your Favourite Programming Language : ")
Shyam = input("Enter your Favourite Programming Language : ")
Gita = input("Enter your Favourite Programming Language : ")
Ritu = input("Enter your Favourite Programming Language : ")
d1 = {"Ram":None,"Shyam":None,"Gita":None,"Ritu":None}
d1.update({'Ram':Ram})
d1.update({'Shyam':Shyam})
d1.update({'Gita':Gita})
d1.update({'Ritu':Ritu})
print(d1)