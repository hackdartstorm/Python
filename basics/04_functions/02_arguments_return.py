# Function With Arguments and Using of Return

def avg(first_num, second_num, message):
    total = first_num + second_num
    return f"{total} {message}"


result = avg(message="kidding", first_num=3, second_num=4)
print(result)
