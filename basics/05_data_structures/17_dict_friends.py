'''Question1.Create an empty dictionary. Allow 4 friends to enter their favorite language as
value and use key as their names. Assume that the names are unique.'''

# Answer Type 1
friends_languages = {}
ram_input = input("""Syntax :-
            --Name-- --xxProgrammingLanguage--
Enter your Name with Your Favourite Programming Language : """).split(" ")
key = ram_input[0]
value = ram_input[1]
friends_languages.update({key:value})
shyam_input = input("""Syntax :-
            --Name-- --xxProgrammingLanguage--
Enter your Name with Your Favourite Programming Language : """).split(" ")
key = shyam_input[0]
value = shyam_input[1]
friends_languages.update({key:value})
gita_input = input("""Syntax :-
            --Name-- --xxProgrammingLanguage--
Enter your Name with Your Favourite Programming Language : """).split(" ")
key = gita_input[0]
value = gita_input[1]
friends_languages.update({key:value})
ritu_input = input("""Syntax :-
            --Name-- --xxProgrammingLanguage--
Enter your Name with Your Favourite Programming Language : """).split(" ")
key = ritu_input[0]
value = ritu_input[1]
friends_languages.update({key:value})
print(friends_languages)

# Answer Type 2

ram_language = input("Enter your Favourite Programming Language : ")
shyam_language = input("Enter your Favourite Programming Language : ")
gita_language = input("Enter your Favourite Programming Language : ")
ritu_language = input("Enter your Favourite Programming Language : ")
friends_languages = {"ram":None,"Shyam":None,"Gita":None,"Ritu":None}
friends_languages.update({'ram':ram_language})
friends_languages.update({'Shyam':shyam_language})
friends_languages.update({'Gita':gita_language})
friends_languages.update({'Ritu':ritu_language})
print(friends_languages)