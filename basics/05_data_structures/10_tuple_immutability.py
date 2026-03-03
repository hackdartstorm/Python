# Check that a tuple type cannot be changed in python

immutable_tuple = ("ram", False, True, 222.222)
immutable_tuple[2] = 23  # Error of 'tuple' object does not support item assignment
