class Animal:
    legs = 2
    hand = 2
    power = 100

    def __init__(self, strength, health, attack):  # Dunder Method in Python Which is automatically Called
        self.strength = strength
        self.health = health
        self.attack = attack
        print(f"\n\tLoading ...")
        print(f"Strength is : {strength}\nHealth is : {health}\nAttack is : {attack}")


Kangaroo = Animal(100, 12, "100x")
"""
a = int(input("Enter Your Strength ?/100 : "))  
b = int(input("Enter Your Health ?/100 : "))  
c = input("Enter Your Attack Name  : ")
"""
