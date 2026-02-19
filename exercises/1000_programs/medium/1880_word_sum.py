def word_to_number(word: str) -> int:
    num_str = ""
    for ch in word:
        num_str += str(ord(ch) - ord("a"))
    return int(num_str)


def is_sum_equal(firstWord: str, secondWord: str, targetWord: str) -> bool:
    return word_to_number(firstWord) + word_to_number(secondWord) == word_to_number(
        targetWord
    )


if __name__ == "__main__":
    # Exemplos básicos para teste manual
    print(is_sum_equal("acb", "cba", "cdb"))  # True
    print(is_sum_equal("aaa", "a", "aaaa"))  # True
    print(is_sum_equal("a", "b", "c"))  # False
