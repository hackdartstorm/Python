# Write a program to create a dictionary of Hindi words with values as their English translation.
# Provide user with an option to look it up!


# Concept 1 to do : (easy to understand) " Takes two input() from user "
hindi_english_dict = {"Bhagwaan": "God", "Kalyan": "Growth", "Seb": "Apple", "Kela": "Banana", "Tufan ka Devta": "God of Thunder ? Thor"}
hindi_word = input("Enter a Hindi Word : ")
english_word = input("Enter the English word for that hindi Word : ")
hindi_english_dict.update({hindi_word: english_word})
print(hindi_english_dict)

# Concept 2 to do :(complex) " Takes Single input but takes both hindi-english translation words"
hindi_english_dict = {"Bhagwaan": "God", "Kalyan": "Growth", "Seb": "Apple", "Kela": "Banana", "Tufan ka Devta": "God of Thunder ? Thor"}  # A Dictionary
user_input = input("Enter a Hindi Word and also give its English translation : ") #Takes input() from user
hindi_word = user_input.split(" ").pop(0)  # if the user gives "ram" and "shyam" then this split make it list of strings then the pop() delete the first element and return it and we just capture that return value and store it in a variable
english_word = user_input.split(" ").pop(1)  # same for second variable
hindi_english_dict.update({hindi_word: english_word})  # Just put the stored values in the update position
print(hindi_english_dict)  # Print the dictionary
