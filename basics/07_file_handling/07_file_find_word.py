"""
Read text from 'poems.txt' and find if it contains the word 'twinkle'.
Count occurrences if found.
"""

with open("poems.txt") as file_handle:
    file_data = file_handle.read().lower()
    word_count = file_data.count("twinkle")
    if "twinkle" in file_data:
        print(f"Twinkle Found {word_count} times")
    else:
        print("Twinkle not Found")
