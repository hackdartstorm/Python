"""
Create a class ‘Employee’ and add salary and increment properties to it.
Write a method ‘salaryAfterIncrement’ method with a @property decorator with a setter
which changes the self.salary of increment based on the salary
"""


class Employee():
    def __init__(self,salary=0,increment=0):
        self._salary = salary 
        self.increment = increment
    
    @property
    def salary_after_increment(self):
        return self._salary + (self._salary * (self.increment/100))
    
    @salary_after_increment.setter
    def salary_after_increment(self, real_salary):
        if real_salary <= 5000:
            self.increment = 10

        elif real_salary >= 20000 and real_salary < 50000:
            self.increment = 5

        elif real_salary >=50000:
            self.increment = 2
        
        else:
            self.increment = 1
        
        self._salary = real_salary


#Output 
rajesh = Employee()
rajesh.salary_after_increment = 50000
print(rajesh.salary_after_increment) #Output 51000

rajesh.salary_after_increment = 5000
print(rajesh.salary_after_increment) #Output 5500



        


