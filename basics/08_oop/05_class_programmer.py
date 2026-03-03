"""
Create a class “Programmer” for storing information of few programmers
working at Microsoft.
"""

class Programmer:
    Company = "Microsoft"
    Salary = 200000

    def __init__(self, name):
        self.name = name

Rajvir = Programmer("Rajvir")
print(f"\nProgrammer name : {Rajvir.name}  Programmer Salary : {Rajvir.Salary + 10000} \t Working at {Rajvir.Company}\n")

Raju = Programmer("Raju")
print(f"Programmer name : {Raju.name} \t Programmer Salary : {Raju.Salary + 800} \t Working at {Raju.Company}\n")
