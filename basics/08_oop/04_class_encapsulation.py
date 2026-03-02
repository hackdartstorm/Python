"""
Problem: GameCharacter class
Create a class called GameCharacter with:
🔒 Private variables: _name, _level, _health
✅ Rules:
   - Level: Must be between 1 and 50
   - Health: Must be between 0 and 100
   - Name: Cannot be empty
🧠 What you must implement:
   - __init__ method
   - Getter for all three
   - Setter for all three with validation
   - Print values using getters
   - Update values using setters
"""


class GameCharacter:
    def __init__(self, name, level, health):
        self._name = name      # Private variable for name
        self._level = level    # Private variable for level
        self._health = health  # Private variable for health

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def health(self):
        return self._health

    @name.setter
    def name(self, value):
        if value != "":
            self._name = value
        else:
            print("Name Can't be Blank!")

    @level.setter
    def level(self, value):
        if 1 <= value <= 50:
            self._level = value
        else:
            print("Level Must be between 1 and 50")

    @health.setter
    def health(self, value):
        if 0 <= value <= 100:
            self._health = value
        else:
            print("Health Must be between 0 and 100")


# Creating an object
Adam = GameCharacter("Adam", 45, 98)

print("Output")
print(f"\tName: {Adam.name}\n\tLevel: {Adam.level}\n\tHealth: {Adam.health}\n")

print("Updated Output:\n")
# Trying to set invalid values
Adam.name = ""
Adam.level = -51
Adam.health = -101

print(f"\tName: {Adam.name}\n\tLevel: {Adam.level}\n\tHealth: {Adam.health}\n")
