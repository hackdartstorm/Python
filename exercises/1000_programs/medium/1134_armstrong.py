""" Check if number is Armstrong number 
An Armstrong number is a number that equals the sum of its own digits 
each raised to the power of the total number of digits.  """


# we return the number of digits in n
def get_digits(n):
    digits_count = 0

    while n > 0:
        digits_count += 1
        n = n // 10

    return digits_count


n = int(input("Enter a number: ")) # we assume that the user is going to give an int 
total_of_digits = get_digits(n)  # we get the total of digits in n
aux = n  # we need to store the value to make the final comparation

sum = 0
while n > 0:
    digit = n % 10  # get the last digit
    sum += pow(digit, total_of_digits) 
    n //= 10

print(sum == aux)
