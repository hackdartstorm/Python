def good_substrings(s: str) -> int:
    """
    A substring is called good if all of the characters in the substring are different.

    Given a string s, return the number of good substrings of length three in s.

    Args:
        s (str): The input string.

    Returns: 
        int: The number of good substrings of length three in s. 

    Example: 
        Input: s = "smithech"
        Output: 6
        Explanation: The good substrings are "smi", "mit", "ith", "the", "hec", "ech".
    
    """
    count = 0

    # len(s) - 2 because the last 3-character substring starts at index len(s)-3
    for i in range(len(s) - 2):
        # The set() function removes duplicate characters, so if the length of the set is 3, it means all characters are different
        if len(set(s[i:i + 3])) == 3:
            count += 1
    return count

if __name__ == "__main__":
    example = "Smithech"
    result = good_substrings(example)
    print("Input: ", example)
    print("Output: ", result) 