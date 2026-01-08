"""
Create a class ‘Employee’ and add salary and increment properties to it.
Write a method ‘salaryAfterIncrement’ method with a @property decorator with a setter
which changes the self.salary of increment based on the salary
"""

class Employee():
    def __init__(self,salary):
        self._salary = salary
        self._increment = 0

    @property
    def SalaryAfterIncrement(self):
        return self._salary + self._increment

    @SalaryAfterIncrement.setter
    def SalaryAfterIncrement(self,salary):
        if( salary == 0 ):
            self._increment = 10000
        
        elif( salary <= 10000 ):
            self._increment = 5000
        
        elif( salary >= 1000000 ):
            self._increment = int(salary * 0.01)

        else:
            self._increment = 1000
        self._salary = salary


Rajesh = Employee(0)
Rajesh.SalaryAfterIncrement = 100000
print(Rajesh.SalaryAfterIncrement)
Rajesh.SalaryAfterIncrement = 2100
print(Rajesh.SalaryAfterIncrement)

        


