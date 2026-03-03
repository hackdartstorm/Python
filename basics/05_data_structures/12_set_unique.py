# Write a program to input eight numbers from the user and display all the unique numbers (once).

unique_numbers_set = set()  # Empty Set
user_input = input("Enter 8 Numbers :")  # Takes Input
number = user_input.split(" ").pop(0)
unique_numbers_set.add(number)
number = user_input.split(" ").pop(1)
unique_numbers_set.add(number)
number = user_input.split(" ").pop(2)
unique_numbers_set.add(number)
number = user_input.split(" ").pop(3)
unique_numbers_set.add(number)
number = user_input.split(" ").pop(4)
unique_numbers_set.add(number)
number = user_input.split(" ").pop(5)
unique_numbers_set.add(number)
number = user_input.split(" ").pop(6)
unique_numbers_set.add(number)
number = user_input.split(" ").pop(7)
unique_numbers_set.add(number)
print(unique_numbers_set)  # print the Updated Set


