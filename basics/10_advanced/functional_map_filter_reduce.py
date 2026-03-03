"""🔁 map → "change every item"
🚫 filter → "keep some items"
➕ reduce → "collapse into one"""

from functools import reduce

numbers_list = [1, 2, 3, 4, 5, 6]

# Example of Map
square_function = lambda number: number * number
squared_result = map(square_function, numbers_list)
print(list(squared_result))


# Example of Filter
def is_even(number):
    if number % 2 == 0:
        return True
    return False


even_numbers = filter(is_even, numbers_list)
print(list(even_numbers))

# Example of Reduce
multiply_function = lambda num1, num2: num1 * num2
print(reduce(multiply_function, numbers_list))
