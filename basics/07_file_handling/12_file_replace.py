"""
A file contains the word "Donkey" multiple times.
Replace this word with ##### by updating the same file.
"""

with open("donkey.txt") as input_file:
    file_text = input_file.read()

final_text = file_text.replace("donkey", "#####")

with open("donkey.txt", "w") as output_file:
    output_file.write(final_text)

"""
Sample Paragraph:

The donkey is a hardworking animal, and the donkey has been helping humans for centuries.
In villages, the donkey carries heavy loads where machines cannot go.
A donkey may look slow, but the donkey is patient and strong.
People often underestimate the donkey, yet the donkey continues to work quietly without complaint.
From farms to mountains, the donkey remains a loyal and useful animal.
"""
        