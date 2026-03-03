# Write a program to fill in a letter template given below with name and date.



# Technique One (Harder+fragile+Complex)
user_name = input("Enter Your Name : ")
date = input("Enter the Date like : DD/MM/YY ?\nUnderstand Enter :")
letter_template = '''
Dear <|Name|>,
You are selected!
<|Date|>
'''
name_replaced = letter_template.replace("<|Name|>", user_name)
date_replaced = name_replaced.replace("<|Date|>", date)
name_length = len(user_name)  # Count for name length
final_count = 25 + name_length  # Count for name
output_start = name_replaced[:final_count]
output_end = date_replaced[final_count:]
# print(output_end)
# print(output_start)
print(output_start, output_end)


# Simple And Easiest Way
user_name = input("Enter Your Name: ")
date = input("Enter the Date (DD/MM/YY): ")

letter_template = '''
Dear <|Name|>,
You are selected!
<|Date|>
'''

name_replaced = letter_template.replace("<|Name|>", user_name)
date_replaced = name_replaced.replace("<|Date|>", date)
print(date_replaced)
