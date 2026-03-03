""" This program generates a fun story by asking the user for different types of words"""


def mad_libs_story():
    # Ask the user for words
    name = input("Enter a name: ")
    animal = input("Enter an animal: ")
    adjective1 = input("Enter an adjective: ")
    adjective2 = input("Enter another adjective: ")
    place = input("Enter a place: ")
    verb1 = input("Enter a verb (present tense): ")
    verb2 = input("Enter another verb (present tense): ")
    food = input("Enter a type of food: ")
    color = input("Enter a color: ")
    
    # Story template with placeholders
    story = f"""
    Once upon a time, in the {adjective1} land of {place}, there lived a {adjective2} {animal} named {name}.
    Every morning, {name} would {verb1} happily around the {color} fields, dreaming of {food}.
    One day, {name} decided to {verb2} beyond the mountains to discover new adventures.
    Along the way, {name} met many strange creatures, some friendly and some {adjective1}.
    Finally, after a long journey, {name} returned home with amazing stories to share, feeling proud and {adjective2}.
    And from that day on, {name} became known as the bravest {animal} in all of {place}.
    """

    # Print the story
    print(story)


# Run the story generator
if __name__ == "__main__":
    mad_libs_story()
