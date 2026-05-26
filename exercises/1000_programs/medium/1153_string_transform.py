def can_transform(str1: str, str2: str) -> bool:
    """
    Check if str1 can transform into str2 by replacing each character in str1
    with another character (or the same character).

    Args:
        str1 (str): The source string.
        str2 (str): The target string.

    Returns:
        bool: True if str1 can be transformed into str2, False otherwise.

    Examples:
        Input: str1 = "aabcc", str2 = "ccdee"
        Output: True
        Explanation: 'a'->'c', 'b'->'d', 'c'->'e'

        Input: str1 = "leetcode", str2 = "codeleet"
        Output: False
        Explanation: There's no way to map 'l' and 'e' to satisfy both positions.
    """
    if len(str1) != len(str2):
        return False
    
    if str1 == str2:
        return True
    
    char_map = {}
    for c1, c2 in zip(str1, str2):
        if c1 in char_map:
            if char_map[c1] != c2:
                return False
        else:
            char_map[c1] = c2
    
    if len(set(str2)) == 26:
        return str1 == str2
    
    return True


if __name__ == "__main__":
    example1_str1 = "aabcc"
    example1_str2 = "ccdee"
    result1 = can_transform(example1_str1, example1_str2)
    print(f"Input: str1 = '{example1_str1}', str2 = '{example1_str2}'")
    print(f"Output: {result1}")
    
    example2_str1 = "leetcode"
    example2_str2 = "codeleet"
    result2 = can_transform(example2_str1, example2_str2)
    print(f"\nInput: str1 = '{example2_str1}', str2 = '{example2_str2}'")
    print(f"Output: {result2}")