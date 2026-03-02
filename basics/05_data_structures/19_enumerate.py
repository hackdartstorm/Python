#Before Using emumerate
items_list = ["Hello",23,False,True,45,"ram"]
index = 0
for item in items_list:
    print(f"The item number at index {index} is {item}")
    index = index + 1

# Using Enumerate

for index, item in enumerate(items_list):
    print(f"The item number at index {index} is {item}")

