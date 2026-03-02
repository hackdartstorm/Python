"""
Write a python function to remove a given word from a list ad strip it at the same
time.
"""

def remove_and_strip(string_list, word):
    cleaned_list = []
    for item in string_list:
        if not(item == word):
            cleaned_list.append(item.strip(word))
    return cleaned_list


string_list = ["ram","Shyam","Gyan",'Pyan',"Myan","an"]
print(remove_and_strip(string_list, "an"))