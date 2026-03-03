"""
Create a class (Vector2d) and use it to create another class representing a Vector3d.
"""


class Vector2d:
    def __init__(self, number, value):
        self.number = number
        self._value = value

    @property
    def value(self):
        if self._value > 0:
            return self._value
        else:
            print(f"------> None Value! \"Your Value Must be greater than 0\"")

    @value.setter
    def value(self, new_value):
        if new_value <= 0:
            print(f"------> Value Must be greater than 0 ")
        else:
            self._value = new_value


class Vector3d(Vector2d):
    def __init__(self, number, value):
        super().__init__(number, value)
        if value < 0:
            value = 0
            self.addition_result = number + value
        print(f"Addition of {number} and {value} is {self.addition_result}")


vector_instance = Vector3d(12, -99)
print("Value : ", vector_instance.value)
vector_instance.value = 32
print("Updated Value : ", vector_instance.value)
vector_instance.value = -9
print("Value : ", vector_instance.value)
