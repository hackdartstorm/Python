# Lists
foods_list = ["biriyani", "Panner", 200, False, 12, True, 439895487.54879954,
              23.222, 90, "ramji-krishnaji"]  # Lists are mutable
print(foods_list[0])  # Print the first item from the list

# Mutability Check
foods_list[0] = "radheradhe"
print(foods_list)
"""
                                            Lists vs Strings
                                                                                                                             """
# Strings
food_string = "ramji"
print(food_string[0])  # Print the first item from the String

# Immutability Check
food_string[0] = "radhe2radhe"  # error
print(food_string)
