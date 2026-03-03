a = 1000


def code():
    global a  # The global keyword allows a function to modify a global variable.
    a = 12
    print(a) 


code()
print(a)
