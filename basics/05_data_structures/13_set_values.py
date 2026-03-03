"""Question1.What will be the length of following set s:
s = set()
s.add(20)
s.add(20.0)
s.add('20') # length of s after these operations?"""

unique_set = set()
unique_set.add(20)
unique_set.add(20.0)
unique_set.add('20')
print(len(unique_set), unique_set)  # length will be 2 as both float and integer cant be assign (unique)
