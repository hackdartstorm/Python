"""QuestionNo1. Write a program to find the greatest of four numbers entered by the user."""

user_input = input("Enter Four Number ")
first_num = user_input.split(" ").pop(0)
second_num = user_input.split(" ").pop(1)
third_num = user_input.split(" ").pop(2)
fourth_num = user_input.split(" ").pop(3)
print(f"Ok! I Found Your Numbers {first_num},{second_num},{third_num},{fourth_num}")
first_num = int(first_num)
second_num = int(second_num)
third_num = int(third_num)
fourth_num = int(fourth_num)
if first_num >= second_num and first_num >= third_num and first_num >= fourth_num:
    print(f"{first_num}")
elif second_num >= second_num and second_num >= third_num and third_num >= fourth_num:
    print(f"{second_num}")
elif third_num >= second_num and third_num >= third_num and third_num >= fourth_num:
    print(f"{third_num}")
elif fourth_num >= first_num and fourth_num >= third_num and fourth_num >= second_num:
    print(f"{fourth_num}")
else:
    print("Invalid Number ! Choose Any Valid Number")


"""QuestionNo2. Write a program to find out whether a student has passed or failed if it requires a
total of 40% and at least 33% in each subject to pass. Assume 3 subjects and
take marks as an input from the user."""


marks_input = input(f"Enter Your Mathematics Marks \nSocial Studies Marks And\nScience Marks : ")
maths_marks = marks_input.split(" ").pop(0)
social_science_marks = marks_input.split(" ").pop(1)
science_marks = marks_input.split(" ").pop(2)
print(f"Your Report")
total_marks = int(maths_marks) + int(social_science_marks) + int(science_marks)
if total_marks > 120:
    print(f"\tYour Marks {total_marks} Out of 300")
    if int(maths_marks) >= 33 and int(social_science_marks) >= 33 and int(science_marks) >= 33:
        print(f"You Passes\nMathematics : {maths_marks}\nSocial Science : {social_science_marks}\nScience : {science_marks}")
    else:
        print("Go and Study !")


"""QuestionNo3. A spam comment is defined as a text containing following keywords:
"Make a lot of money", "buy now", "subscribe this", "click this". Write a program
to detect these spams."""

comment_text = input("Enter Your Comments : ").lower()
words_list = comment_text.split(" ")
spam_count = comment_text.count("make a lot of money") + comment_text.count("buy now") + comment_text.count("subscribe this") + comment_text.count("click this")
print(f"Spam Comments {spam_count}")


"""QuestionNo4. Write a program to find whether a given username contains less than 10
characters or not."""

username = input("Enter your Username : ")
if len(username) < 10:
    print("Less than 10 characters ")
else:
    print("More than or Equals to 10 characters ")


"""QuestionNo5. Write a program which finds out whether a given name is present in a list or not."""

# type1
names_list = ["ram","radhe","kohli","7","Hitman","siu","messi","Ben10"]
user_name = input("Enter Your Name : ")
name_count = names_list.count(user_name)
print(name_count)
if name_count == 0:
    print("Not Present ")
elif name_count != 0:
    print("Present")
else:
    print("Bla Bla Bla")

# type2
if user_name in names_list:
    print("Yes")
else:
    print("no")


"""QuestionNo6. Write a program to calculate the grade of a student from his marks from the
following scheme:
90 - 100 => Excellent
80 - 90 => Grade A
70 - 80 => Grade B
60 - 70 => Grade C
50 - 60 => Grade D
<=50 => Failed"""

student_marks = int(input("Enter your Marks : "))
if student_marks >= 90 and student_marks <= 100:
    print(f"{student_marks}% Excellent")
elif student_marks >= 80 and student_marks < 90:
    print(f"{student_marks}% Grade A")
elif student_marks >= 70 and student_marks < 80:
    print(f"{student_marks}% Grade C")
elif student_marks >= 60 and student_marks < 70:
    print(f"{student_marks}% Grade D")
elif student_marks <= 50:
    print(f"{student_marks}% You Failed")
else:
    print(" Invalid Try again")


"""QuestionNo6. Write a program to find out whether a given post is talking about "Harry" or not."""

post_content = input("Enter Your Post : ").split(" ")
if "harry".lower() in post_content.lower():
    result = "Yes Present"
else:
    result = "No Not-Present"
print(post_content)
