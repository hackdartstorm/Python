# Set Methods Example

set1 = {1, 2, 3, 4, 5, False, True, "Aman", 23.23, "rajesh", "Patel", "Sharma"}
set2 = {1, 2, 3, 4, 5, "rajesh", "Patel", "ranjit"}
set3 = {462, 3297}
set4 = {"freefire", "enormous"}

# Adding and removing elements
set1.add("ram chandra ")        # Add single element
set1.clear()                    # Remove all elements
print(set1.copy())              # Create a copy

# Set operations (return new set)
print(set1.difference(set2))            # Elements in set1 but not set2
print(set1.intersection(set2))          # Common elements
print(set1.union(set2))                 # All unique elements
print(set1.symmetric_difference(set2))  # Elements in either, not both

# Set operations (modify original)
set1.difference_update(set2)        # Remove elements found in set2
set1.intersection_update(set2)      # Keep only common elements
set1.symmetric_difference_update(set2)  # Keep elements in either, not both

# Set relationships
print(set1.isdisjoint(set2))    # True if no common elements
print(set2.issubset(set1))      # True if set2 is contained in set1
print(set1.issuperset(set2))    # True if set1 contains set2

# Other operations
set2.pop()          # Remove random element
set1.remove(False)  # Remove specific element (raises error if missing)
set1.update(set2, set3, set4)  # Add all elements from other sets

print(set1)  # Print the final set 




