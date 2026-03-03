# Before
def add_numbers(first_num, second_num):
    total = first_num + second_num
    return total


result = add_numbers(2, 9)
print(result)


def calculate_square(number):
    squared_result = number * number
    return squared_result


result = calculate_square(9)
print(result)


# After
sum_function = lambda first_num, second_num: first_num + second_num
print(sum_function(1, 10))

square_function = lambda number: number * number
print(square_function(9))
