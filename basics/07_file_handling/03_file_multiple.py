"""
Write a program to open three files 1.txt, 2.txt and 3.txt.
If any of these files are not present, print a message without exiting.
"""

try:
    with (open("1.txt") as file1,
          open("2.txt") as file2,
          open("3.txt") as file3):
        pass
except FileNotFoundError:
    print("\n\t\t\t\t\tFile Not Found\n")
