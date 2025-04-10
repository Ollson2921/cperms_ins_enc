"""This module is used for checking if a Cayley permutation
is a vertical juxtaposition and if a basis has a regular
vertical insertion encoding."""

from typing import Tuple, List
from cayley_permutations import CayleyPermutation, string_to_basis


def regular_vertical_insertion_encoding(basis: str) -> bool:
    """Checks if a basis has a regular insertion encoding.

    Example:
    >>> has_regular_insertion_encoding([CayleyPermutation([0, 1]), CayleyPermutation([1, 0])])
    True
    """
    basis = string_to_basis(basis)
    for i in range(3):
        for j in range(3):
            if any(checks_type(cperm, (i, j)) for cperm in basis):
                continue
            return False
    return True


def check_if_type(cperm: List[int], jux: int) -> bool:
    """Checks if the Cayley permutation is of the type of sequence specified by the integer."""
    if jux == 0:
        return is_decreasing(cperm)
    if jux == 1:
        return is_increasing(cperm)
    if jux == 2:
        return is_constant(cperm)
    raise ValueError("Type must be 0, 1, or 2.")


def checks_type(cperm: CayleyPermutation, class_to_check: Tuple[int, int]) -> bool:
    """
    Returns True if the Cayley permutation is a vertical juxtaposition
    of the type specified by the tuple.
    In the tuple the first element is above, the second element is below.
    0 -> strictly decreasing
    1 -> strictly increasing
    2 -> constant

    Examples:
    >>> checks_type(CayleyPermutation([0, 1, 2]), (1, 1))
    True
    >>> checks_type(CayleyPermutation([0, 1, 2]), (0, 0))
    False
    """
    if len(cperm) == 0:
        return True
    max_val = max(cperm.cperm)
    for line in range(-1, max_val + 1):
        above = []
        below = []
        for val in cperm.cperm:
            if val > line:
                above.append(val)
            if val <= line:
                below.append(val)
        if (check_if_type(above, class_to_check[0])) and check_if_type(
            below, class_to_check[1]
        ):
            return True
    return False


def is_increasing(cperm: List[int]) -> bool:
    """Returns True if the Cayley permutation is strictly increasing."""
    return all(x < y for x, y in zip(cperm, cperm[1:]))


def is_decreasing(cperm: List[int]) -> bool:
    """Returns True if the Cayley permutation is strictly decreasing."""
    return all(x > y for x, y in zip(cperm, cperm[1:]))


def is_constant(cperm: List[int]) -> bool:
    """Returns True if the Cayley permutation is constant."""
    return all(x == y for x, y in zip(cperm, cperm[1:]))
