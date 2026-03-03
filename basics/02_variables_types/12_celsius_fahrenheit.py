# Write a python program using function to convert Farenheit to Celsius.

def checktemp(c):
    f = (c * 9/5) + 32
    return f"{f}° Farenheit"


l = []
count = 0
while True:
    a = int(input("Enter the Temperature in Celcius : "))
    l.append(a)
    count += 1
    if(count==1):
        break
a = l[0]
print(f"Your Number :{a}")
faren = checktemp(a)
print(faren)
