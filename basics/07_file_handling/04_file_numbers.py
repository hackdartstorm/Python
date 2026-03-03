"""
Store the multiplication tables in a file named Tables.txt.
"""
even_numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
with open("Tables.py", "w") as output_file:
    for number in even_numbers:
        output_file.write(f"{number}\t")

with open("Tables.py") as read_file:
    print(read_file.read())
