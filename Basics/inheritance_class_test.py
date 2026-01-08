"""
Create a class (Vector2d) and use it to create another class representing a Vector3d.
"""
class Vector2d:
    def __init__(self,num,value):
        self.num = num
        self._value = value

    @property
    def value(self):
        if self._value > 0 :
            return self._value
        else:
            print(f"------> None Value! \"Your Value Must be greater than 0\"")
             
             
    
    @value.setter
    def value(self,Nvalue):
        if Nvalue <= 0 :
            print(f"------> Value Must be greater than 0 ")
        else:
            self._value = Nvalue
            

    
class Vector3d(Vector2d):
        def __init__(self, num, value):
            super().__init__(num, value)
            if value < 0:
                value = 0
                self.add = num + value
            print(f"Addition of {num} and {value} is {self.add}")
            



f = Vector3d(12,-99)
print("Value : ",f.value)
f.value = 32
print("Updated Value : ",f.value)
f.value = -9
print("Value : " ,f.value)


    
        
