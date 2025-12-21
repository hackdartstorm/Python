"""QuestionNo1. Write a program to find the greatest of four numbers entered by the user."""
num = input("Enter Four Number ")
a = num.split(" ").pop(0)
b = num.split(" ").pop(1)
c = num.split(" ").pop(2)
d = num.split(" ").pop(3)
print(f"Ok! I Found Your Numbers {a},{b},{c},{d}")
a = int(a)
b = int(b)
c = int(c)
d = int(d)
if(a>=b and a>=c and a>=d):
    print(f"{a}")
elif(b>=b and b>=c and c>=d):
    print(f"{b}")
elif(c>=b and c>=c and c>=d):
    print(f"{c}")
elif(d>=a and d>=c and d>=b):
    print(f"{d}")
else:
    print("Invalid Number ! Choose Any Valid Number")


"""QuestionNo2. Write a program to find out whether a student has passed or failed if it requires a
total of 40% and at least 33% in each subject to pass. Assume 3 subjects and
take marks as an input from the user."""


marks = input(f"Enter Your Mathematics Marks \nSocial Studies Marks And\nScience Marks : ")
maths = marks.split(" ").pop(0)
SocialSci = marks.split(" ").pop(1)
Science = marks.split(" ").pop(2)
print(f"Your Report")
tmarks = int(maths) + int(SocialSci) + int(Science)
if(tmarks>120):
    print(f"\tYour Marks {tmarks} Out of 300")
    if(int(maths)>=33 and int(SocialSci)>=33 and int(Science)>=33):
        print(f"You Passes\nMathematics : {maths}\nSocial Science : {SocialSci}\nScience : {Science}")
    else:
        print("Go and Study !")


"""QuestionNo3. A spam comment is defined as a text containing following keywords:
“Make a lot of money”, “buy now”, “subscribe this”, “click this”. Write a program
to detect these spams."""

Text = input("Enter Your Comments : ").lower()
new = Text.split(" ")
spam = Text.count("make a lot of money") + Text.count("buy now") + Text.count("subscribe this") + Text.count("click this")
print(f"Spam Comments {spam}")


"""QuestionNo4. Write a program to find whether a given username contains less than 10
characters or not."""

un = input("Enter your Username : ")
if(len(un)<10):
    print("Less than 10 characters ")
else:
    print("More than or Equals to 10 characters ")


"""QuestionNo5. Write a program which finds out whether a given name is present in a list or not."""

# type1
l1 = ["ram","radhe","kohli","7","Hitman","siu","messi","Ben10"]
user = input("Enter Your Name : ")
check = l1.count(user)
print(check)
if(check == 0):
    print("Not Present ")
elif(check != 0):
    print("Present")
else:
    print("Bla Bla Bla")

# type2
if(user in l1):
    print("Yes")
else:
    print("no")


"""QuestionNo6. Write a program to calculate the grade of a student from his marks from the
following scheme:
90 – 100 => Excellent
80 – 90 => Grade A
70 – 80 => Grade B
60 – 70 => Grade C
50 – 60 => Grade D
<=50 => Failed"""

marks = int(input("Enter your Marks : "))
if(marks>=90 and marks<=100):
    print(f"{marks}% Excellent")
elif(marks>=80 and marks<90):
    print(f"{marks}% Grade A")
elif(marks>=70 and marks<80):
    print(f"{marks}% Grade C")
elif(marks>=60 and marks<70):
    print(f"{marks}% Grade D")
elif(marks<=50):
    print(f"{marks}% You Failed")
else:
    print(" Invalid Try again")


"""QuestionNo6. Write a program to find out whether a given post is talking about “Harry” or not."""

post = input("Enter Your Post : ").split(" ")
if("harry".lower() in  post.lower()):
    y = "Yes Present"
else:
    y = "No Not-Present"
print(post)