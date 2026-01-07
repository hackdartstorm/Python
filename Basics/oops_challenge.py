"""
Problem: GameCharacter-class
Create a class called GameCharacter with:
🔒 Private variables
_name
_level
_health
✅ Rules (very important)
Level
Must be between 1 and 50
Health
Must be between 0 and 100
Name
Cannot be empty
🧠 What you must implement
__init__ method
Getter for all three
Setter for all three with validation
Print values using getters
Update values using setters
"""
class GameCharacter():  
    # Class definition for a game character

    def __init__(self, name, level, health):
        # Constructor: runs when object is created
        # Initializes private variables
        self._name = name        # Private variable for name
        self._level = level      # Private variable for level
        self._health = health    # Private variable for health
    
    @property
    def Name(self):
        # Getter for name
        # Called when we access: object.Name
        return self._name
    
    @property
    def Level(self):
        # Getter for level
        # Returns current level
        return self._level
    
    @property
    def Health(self):
        # Getter for health
        # Returns current health
        return self._health
    
    @Name.setter
    def Name(self, value):
        # Setter for name
        # Called when we assign: object.Name = value
        if value != "":
            self._name = value   # Update name if valid
        else:
            print("Name Can't be Blank ! ")
    
    @Level.setter
    def Level(self, value):
        # Setter for level
        # Ensures level stays between 1 and 50
        if value >= 1 and value <= 50:
            self._level = value
        else:
            print("Level Must be between 1 and 50")

    @Health.setter
    def Health(self, value):
        # Setter for health
        # Ensures health stays between 0 and 100
        if value >= 0 and value <= 100:
            self._health = value
        else:
            print("Health Must be between 0 and 100")


# Creating an object of GameCharacter
Adam = GameCharacter("Adam", 45, 98)

print("Output")
# Accessing values using getters (no parentheses)
print(f"\tName : {Adam.Name}\n\tLevel : {Adam.Level}\n\tHealth : {Adam.Health}\n")

print("Updated Output:\n")
# Trying to set invalid values (setters will reject them)
Adam.Name = ""
Adam.Level = -51
Adam.Health = -101

# Values remain unchanged because setters blocked invalid input
print(f"\tName : {Adam.Name}\n\tLevel : {Adam.Level}\n\tHealth : {Adam.Health}\n")






        

