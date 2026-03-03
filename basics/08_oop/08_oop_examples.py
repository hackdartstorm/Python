# Professional Coding
class Monster():  # Class definition
    def __init__(self, power, health, speed):  # Constructor to initialize object
        self._power = power    # Private variable for power
        self._health = health  # Private variable for health
        self._speed = speed    # Private variable for speed

    @property
    def Power(self):  # Getter 1 for power
        return self._power

    @property
    def Health(self):  # Getter 2 for health
        return self._health

    @property
    def Speed(self):  # Getter 3 for speed
        return self._speed

    @Speed.setter
    def Speed(self, value):  # Setter 1 for speed
        if 0 < value < 100:
            self._speed = value
        else:
            print("Values Must be between 0 and 100")

    @Power.setter
    def Power(self, value):  # Setter 2 for power
        if 0 < value < 100:
            self._power = value
        else:
            print("Values Must be between 0 and 100")

    @Health.setter
    def Health(self, value):  # Setter 3 for health
        if 0 < value < 100:
            self._health = value
        else:
            print("Values Must be between 0 and 100")


# Creating an object of Monster
devil = Monster(12, 90, 34)

# Accessing values using getters (like variables)
print(f"Here is Your Health : {devil.Health} Power : {devil.Power} & Speed : {devil.Speed}\nUpdated Data")

# Modifying values using setters (with validation)
devil.Speed = 90
devil.Health = 98
devil.Power = 89

# Accessing updated values using getters
print(f"Here is Your Health : {devil.Health} Power : {devil.Power} & Speed : {devil.Speed}\n")

devil = Monster(12,90,34)
print(f"Here is Your Health : {devil.Health} Power : {devil.Power} & Speed : {devil.Speed}\nUpdated Data")
devil.Speed = 90
devil.Health = 98
devil.Power = 89
print(f"Here is Your Health : {devil.Health} Power : {devil.Power} & Speed : {devil.Speed}\n")


# Normal Coding
"""class Monster():
    def __init__(self,Health,Power,Speed):
        self.health = Health
        self.power = Power
        self.speed = Speed
        print(f"Here is Your Health : {Health} Power : {Power} & Speed : {Speed}")
    
anvil = Monster(12,45,89)"""
