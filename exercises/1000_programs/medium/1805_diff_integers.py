def diff_integers_in_string(phrase: str) -> int:
    """
    Given a string phrase, return the number of different integers that appear in phrase. 

    Args:
        phrase (str): The input string.

    Returns: 
        int: The number of different integers that appear in phrase.

    Example: 
        Input: "Smithech ha resuelto el issue #2595"
        Output: 3    
    """
    list_of_integers = set()

    for char in phrase:
        if char.isdigit():
            list_of_integers.add(char)

    return len(list_of_integers)

if __name__ == "__main__":
    example = "Smithech ha resuelto el issue #2595"
    result = diff_integers_in_string(example)
    print("Input: ", example)
    print("Output: ", result) 