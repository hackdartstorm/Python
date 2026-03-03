# List Methods
string_list = ["ram", "gyan", 1111.222, 444, "33", "Ramit sioeo", "ram", "ram"]
string_list.append("sita gita")  # Append object to the end of the list.
count_result = string_list.count("ram")  # Return number of occurrences of value.
string_list.extend(
    "slice")  # Extend list by appending elements from the iterable.
index_result = string_list.index("ram")  # Return first index of value.
string_list.insert(1, "sita")  # Insert object before index.
popped_item = string_list.pop(2)  # Remove and return item at index (default last).
string_list.remove("ram")  # Remove first occurrence of value.
string_list.reverse()  # reverse the list
string_list.sort()  # Sort the list in ascending order and return None.
print(count_result, index_result, string_list, popped_item)  # print and return value (if possible)
