print("1.")
a = "12.009"  # String
b = float(a)  # String to Float
print(type(b))

print("2.")
a = "12b"  # String
"""b = float(a) """  # Error-Occured @TypeError
print(type(b))

print("3.")
z = "123"
b = int(z)
print(type(b))
