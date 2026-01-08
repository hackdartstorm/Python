"""
Create a class ‘Pets’ from a class ‘Animals’ and further create a class ‘Dog’ from
‘Pets’. Add a method ‘bark’ to class ‘Dog’.
"""

class Animals():
    pass

class Pets(Animals):
    pass


class Dog(Pets):
    # We don't use @staticmethod As we use Self
    def Bark(self):
        self.bark = True
        print(self.bark)


simbu = Dog()
simbu.Bark()
