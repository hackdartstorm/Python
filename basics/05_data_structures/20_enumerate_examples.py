"""
Write a program to print third, fifth and seventh element from a list using enumerate
function.
"""

items_list = [12, 23, 45, "Hello", "Raj Shamani", "Mr Beast", "Virat kohli", "Dhoni", "Ben 10"]
for index, item in enumerate(items_list):
    if index == 2 or index == 4 or index == 6:
        print(f"Index : {index}, Values : {item}")
