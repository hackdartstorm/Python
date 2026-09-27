"""Program 1089: Duplicate Zeros.

Difficulty: Medium
Category: Array

Task: Duplicate zeros in array.

Given a fixed-length integer array ``arr``, duplicate every ``0`` in place. The
original elements must shift to the right, and the length of the array must stay
the same, so any element pushed past the last index is dropped.

Input: arr
Expected Output: Modified array

Example:
    duplicate_zeros([1, 0, 2, 3, 0, 4, 5, 0])
    -> [1, 0, 0, 2, 3, 0, 0, 4]

Approach
--------
A naive solution builds a second list of the expanded array and truncates it,
but that needs O(n) extra space. The exercise asks for the in-place version, so
we can only use a fixed number of local variables.

The trick is to walk the array from *right to left* and compute, for every
source index, the position it will occupy after the duplication:

* A value only ever moves to the *right*, so a zero at index ``j`` shifts every
  element after it. The final position of ``arr[j]`` is therefore
  ``j + (number of zeros strictly before j)``.
* If ``arr[j]`` is itself a zero it claims two slots: that position and the next
  one.
* Source elements whose position would be ``>= len(arr)`` have been pushed off
  the end, so they are simply skipped.

We track ``zeros_before`` as the running count of zeros in ``arr[0..j]``.
Because we iterate backwards we can maintain it in O(1) per step: start it at
the total number of zeros and decrement it after visiting each zero.

Walking backwards is what makes the in-place version safe -- the destination is
always at or after the source, so we never overwrite an element we have not read
yet.

Complexity: O(n) time, O(1) extra space.
"""


def duplicate_zeros(arr: list[int]) -> list[int]:
    """Duplicate every zero in ``arr`` in place, keeping the array length.

    Args:
        arr: The list of integers to modify. It is modified in place.

    Returns:
        The same list object that was passed in, for convenience.

    Raises:
        TypeError: If ``arr`` is not a list of integers.

    Example:
        >>> duplicate_zeros([1, 0, 2, 3, 0, 4, 5, 0])
        [1, 0, 0, 2, 3, 0, 0, 4]
    """
    # Guard the contract up front so a bad call fails loudly instead of silently
    # producing nonsense part-way through the loop.
    for index, value in enumerate(arr):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(
                f"arr must contain only integers, but arr[{index}] is {value!r}"
            )

    n = len(arr)
    if n == 0:
        return arr

    # Running count of the zeros in arr[0..j]; walking backwards it starts as
    # the total number of zeros and shrinks as we pass each one.
    zeros_before = arr.count(0)
    written = 0  # number of slots filled so far, only used for the report

    for j in range(n - 1, -1, -1):
        is_zero = arr[j] == 0

        # Final resting place of arr[j] after every zero to its left pushed it
        # right. A zero also claims the following slot for its duplicate.
        destination = j + zeros_before - (1 if is_zero else 0)

        if destination < n:
            arr[destination] = arr[j]
            written += 1
            if is_zero and destination + 1 < n:
                arr[destination + 1] = 0
                written += 1

        if is_zero:
            zeros_before -= 1

    return arr


def _run_tests() -> None:
    """Run the self-checks covering normal input, edge cases and failures."""
    # --- Normal / documented examples -------------------------------------
    assert duplicate_zeros([1, 0, 2, 3, 0, 4, 5, 0]) == [1, 0, 0, 2, 3, 0, 0, 4]
    assert duplicate_zeros([1, 0, 1]) == [1, 0, 0]
    assert duplicate_zeros([0, 0, 0]) == [0, 0, 0]

    # --- Edge cases --------------------------------------------------------
    # Empty list.
    assert duplicate_zeros([]) == []
    # Single element, with and without a zero.
    assert duplicate_zeros([0]) == [0]
    assert duplicate_zeros([7]) == [7]
    # Every element is a zero: the result is all zeros, same length.
    assert duplicate_zeros([0, 0, 0, 0, 0]) == [0, 0, 0, 0, 0]
    # No zeros at all: the array must be untouched.
    assert duplicate_zeros([1, 2, 3]) == [1, 2, 3]
    # A trailing zero is duplicated and the last element is dropped.
    assert duplicate_zeros([1, 2, 0]) == [1, 2, 0]
    # A leading zero pushes everything one slot to the right.
    assert duplicate_zeros([0, 1, 2]) == [0, 0, 1]
    # Duplication overflows the end and truncates.
    assert duplicate_zeros([1, 0, 0, 0, 0]) == [1, 0, 0, 0, 0]
    # Negative values must be preserved.
    assert duplicate_zeros([-1, 0, -2]) == [-1, 0, 0]

    # --- Length and identity are preserved (in place) ---------------------
    for sample in ([1, 0, 2, 3, 0, 4, 5, 0], [0, 0, 0], [4, 5, 6], []):
        original_length = len(sample)
        assert duplicate_zeros(sample) is sample, "must modify the list in place"
        assert len(sample) == original_length, "length must not change"

    # --- Failure cases: invalid input raises TypeError ---------------------
    for bad_input in ([1, "0", 2], [None], [1.5], [True]):
        try:
            duplicate_zeros(bad_input)  # type: ignore[arg-type]
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for {bad_input!r}")

    # --- Brute-force cross-check on many random inputs ---------------------
    def reference(arr: list[int]) -> list[int]:
        """Obvious O(n) extra-space version, used only to validate the above."""
        expanded: list[int] = []
        for value in arr:
            expanded.append(value)
            if value == 0:
                expanded.append(0)
        return expanded[: len(arr)]

    checked = 0
    for first in range(-2, 3):
        for second in range(-2, 3):
            for third in range(-2, 3):
                candidate = [first, second, third]
                assert duplicate_zeros(list(candidate)) == reference(candidate)
                checked += 1
    assert checked == 125, f"expected 125 cross-checked cases, got {checked}"

    print(f"All tests passed ({checked} brute-force cross-checks included).")


if __name__ == "__main__":
    _run_tests()
