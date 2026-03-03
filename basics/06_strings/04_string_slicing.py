# String-Slicing

text_string = "Hello World"
print(text_string[-5:-1])  # Worl
print(text_string[6:10])  # Worl



print(text_string[:])  # Prints the Whole String
print(text_string[:10])  # If in the beginning there is blank then consider as Zero
print(text_string[0:])  # If in the end there is blank then consider as len-1

# With Skip
print(text_string[::2])  # HloWrd
print(text_string[2:-1:-3])  # Blank
print(text_string[::4])  # Hor
