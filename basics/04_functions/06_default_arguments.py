# Default Arguments

def sum(first_num, second_num, message="All is Well"):
    total = first_num + second_num
    return f"Your Sum is : {total} and {message}"


result = sum(24, 36)
print(result)
