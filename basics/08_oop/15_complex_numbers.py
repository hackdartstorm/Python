"""
Question1.Write a class 'Complex' to represent complex numbers, along with overloaded
operators '+' and '*' which adds and multiplies them.
"""


class Complex():
    def __init__(self, real_part, imaginary_part):
        self.real_part = real_part
        self.imaginary_part = imaginary_part

    def __add__(self, other_complex):
        return Complex(self.real_part + other_complex.real_part, self.imaginary_part + other_complex.imaginary_part)

    def __str__(self):
        return f"{self.real_part} + {self.imaginary_part}i"


complex_number1 = Complex(1, 2)
complex_number2 = Complex(3, 4)
print(complex_number1 + complex_number2)
