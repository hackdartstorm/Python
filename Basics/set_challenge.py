'''Question1.What will be the length of following set s:
s = set()
s.add(20)
s.add(20.0)
s.add('20') # length of s after these operations?'''

s = set()
s.add(20)
s.add(20.0)
s.add('20')
print(len(s),s) #length will be 2 as both float and integer cant be assign (unique)
