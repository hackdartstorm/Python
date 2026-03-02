# Dictionary Methods Example

dictionary_data = {
    "ram": 100,
    "Kiran": 90,
    "Sneha": 99.999,
    "String": 33.33,
    "l1": [12, 22],
    "t1": ("ram", "Sita")
}

print(dictionary_data.items())  # View all key-value pairs
print(dictionary_data["l1"])    # Access value by key
print(dictionary_data.keys())   # Get all keys
print(dictionary_data.values()) # Get all values
print(dictionary_data.get("Rama"))  # Safe access (returns None if key missing)

dictionary_data.update({"ram": 33.333})  # Update existing key
print(dictionary_data.copy())       # Create a shallow copy
print(dictionary_data.pop("ram"))   # Remove key and return value

# Create new dict from keys
print(dictionary_data.fromkeys({"Rakesh", "Prasant"}))  

# Get value or add key with default
print(dictionary_data.setdefault(("Stunt", 12422)))  

print(dictionary_data.clear())  # Remove all items
print(dictionary_data)          # Print the dictionary