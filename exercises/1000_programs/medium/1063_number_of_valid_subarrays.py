"""Program 1063: Number of Valid Subarrays.

Difficulty: Medium
Category: Array

Task: Count the number of valid subarrays.

A non-empty contiguous subarray ``nums[i..j]`` is *valid* when its leftmost
element is not larger than any of the other elements, i.e. the leftmost element
is a minimum of the subarray (ties are allowed, so ``[2, 2]`` is valid).

Input: nums
Expected Output: The number of valid subarrays

Example:
    count_valid_subarrays([1, 4, 2, 5, 3]) == 11
    count_valid_subarrays([3, 2, 1]) == 3
    count_valid_subarrays([2, 2, 2]) == 6

Approach
--------
Fix the *right* end of the subarray at index ``j`` and ask: how many indices
``i <= j`` can start a valid subarray ``nums[i..j]``?

Index ``i`` qualifies exactly when every element between ``i`` and ``j`` is at
least ``nums[i]``. In other words ``i`` survives if no element smaller than
``nums[i]`` has appeared to its right so far.

That gives a clean left-to-right sweep with a monotonic stack:

* Walk ``j`` from left to right, keeping a stack of candidate start indices.
* Before processing ``nums[j]``, drop every candidate whose value is strictly
  greater than ``nums[j]``. Those candidates are now dead forever: ``nums[j]``
  is smaller than their value, so they can never start a valid subarray that
  reaches ``j`` or beyond. Popping them here means no future index has to
  revisit them.
* Every candidate left in the stack is a valid start for a subarray ending at
  ``j``, so the answer grows by ``len(stack)``.
* Push ``j`` itself -- a single-element subarray is always valid.

The stack values are therefore kept in non-decreasing order, and the comparison
is a strict ``>`` so that equal values stay on the stack (that is what makes
``[2, 2, 2]`` score 6 rather than 3).

Correctness sketch
------------------
Induction on ``j``. Before the pops, the stack holds exactly the indices
``i <= j-1`` that were still valid candidates. Any candidate with
``nums[i] > nums[j]`` becomes invalid for this and every later right end, and
because the stack is non-decreasing those candidates sit on top, so the ``while``
loop removes exactly the newly-dead indices. Pushing ``j`` then makes the stack
the exact set of valid starts for right end ``j`` (``j`` itself always qualifies,
since a one-element subarray has its leftmost element as a minimum). So adding
``len(stack)`` after the push counts the valid subarrays ending at ``j``.
Summing over all ``j`` counts every valid subarray exactly once, by its unique
right end.

Complexity: O(n) time (each index is pushed once and popped at most once),
O(n) space in the worst case.
"""


def count_valid_subarrays(nums: list[int]) -> int:
    """Return the number of subarrays whose leftmost element is a minimum.

    Args:
        nums: The list of integers to inspect.

    Returns:
        The number of non-empty valid subarrays. ``0`` for an empty list.

    Raises:
        TypeError: If ``nums`` is not a list of integers.

    Example:
        >>> count_valid_subarrays([1, 4, 2, 5, 3])
        11
        >>> count_valid_subarrays([3, 2, 1])
        3
    """
    # Validate up front so a bad call fails loudly instead of silently
    # returning a meaningless count.
    for index, value in enumerate(nums):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(
                f"nums must contain only integers, but nums[{index}] is {value!r}"
            )

    # Candidate start values, kept in non-decreasing order. Only the values
    # matter for the comparisons, so indices are not stored.
    stack: list[int] = []
    total = 0

    for value in nums:
        # Strictly-greater values can no longer start a valid subarray, so they
        # are removed for good. Values equal to `value` stay put.
        while stack and stack[-1] > value:
            stack.pop()

        # This index is a candidate for the current and every future right end;
        # a single-element subarray is always valid.
        stack.append(value)

        # Every candidate in the stack now forms a valid subarray ending here,
        # so the stack size is the number of valid subarrays ending at `value`.
        total += len(stack)

    return total


def _brute_force_count(nums: list[int]) -> int:
    """Reference O(n^3) implementation used only to validate the fast version."""
    n = len(nums)
    count = 0
    for start in range(n):
        for end in range(start, n):
            # The leftmost element must not exceed anything in the subarray.
            if all(
                nums[end_index] >= nums[start] for end_index in range(start, end + 1)
            ):
                count += 1
    return count


def _run_tests() -> None:
    """Run the self-checks covering normal input, edge cases and failures."""
    # --- Documented examples ----------------------------------------------
    assert count_valid_subarrays([1, 4, 2, 5, 3]) == 11
    assert count_valid_subarrays([3, 2, 1]) == 3
    assert count_valid_subarrays([2, 2, 2]) == 6

    # --- Edge cases --------------------------------------------------------
    # Empty list: no non-empty subarrays exist.
    assert count_valid_subarrays([]) == 0
    # Single element: exactly one subarray, and it is valid.
    assert count_valid_subarrays([3]) == 1
    # Strictly increasing: the leftmost is always the minimum, so every
    # subarray is valid -> n * (n + 1) / 2.
    assert count_valid_subarrays([1, 2, 3, 4, 5]) == 15
    # Strictly decreasing: only single elements are valid -> n.
    assert count_valid_subarrays([5, 4, 3, 2, 1]) == 5
    # All equal: every subarray is valid.
    assert count_valid_subarrays([7, 7, 7, 7]) == 10
    # Zeros and negative values are ordinary integers here. For [0, 0, 1, 0] the
    # per-start counts are 4 + 3 + 1 + 1: the leading zeros may extend all the
    # way to the end, while the 1 cannot cross the trailing 0.
    assert count_valid_subarrays([0, 0, 1, 0]) == 9
    assert count_valid_subarrays([-1, -3, -2]) == 4
    # The maximum possible answer, to confirm no overflow in the count.
    assert count_valid_subarrays(list(range(1000))) == 1000 * 1001 // 2

    # --- Failure cases: invalid input raises TypeError ---------------------
    for bad_input in ([1, "2", 3], [None], [1.5], [True]):
        try:
            count_valid_subarrays(bad_input)  # type: ignore[arg-type]
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for {bad_input!r}")

    # --- Brute-force cross-check on exhaustive small inputs ----------------
    checked = 0
    for first in range(-2, 3):
        for second in range(-2, 3):
            for third in range(-2, 3):
                for fourth in range(-2, 3):
                    candidate = [first, second, third, fourth]
                    assert count_valid_subarrays(candidate) == _brute_force_count(
                        candidate
                    ), candidate
                    checked += 1
    assert checked == 625, f"expected 625 cross-checked cases, got {checked}"

    print(f"All tests passed ({checked} brute-force cross-checks included).")


if __name__ == "__main__":
    _run_tests()
