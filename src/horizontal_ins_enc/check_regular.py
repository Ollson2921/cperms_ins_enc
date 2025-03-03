"""This module is used for checking if a Cayley permutation
is a horizontal juxtaposition and if a basis has a regular
horizontal insertion encoding."""

from typing import List
from cayley_permutations import CayleyPermutation


def regular_horizontal_insertion_encoding(basis: List[CayleyPermutation]) -> bool:
    """Checks if a basis has a regular insertion encoding.

    Example:
    >>> has_regular_insertion_encoding([CayleyPermutation([0, 1]), CayleyPermutation([1, 0])])
    True
    """
    for i in range(3):
        for j in range(3):
            if any(check_is_type_of_horizontal_jux(cperm, (i, j)) for cperm in basis):
                continue
            return False
    return True


def check_if_type(cperm: CayleyPermutation, jux: int) -> bool:
    """Checks if the Cayley permutation is of the type of sequence specified by the integer."""
    if jux == 0:
        return cperm.is_decreasing()
    if jux == 1:
        return cperm.is_increasing()
    if jux == 2:
        return cperm.is_constant()
    raise ValueError("Type must be 0, 1, or 2.")


def check_is_type_of_horizontal_jux(
    cperm: CayleyPermutation, class_to_check: List[int]
) -> bool:
    """
    Returns True if the Cayley permutation is a horizontal juxtaposition
    of the type specified by the list.
    In the list the first element is left, the second element is right.
    0 -> strictly decreasing
    1 -> strictly increasing
    2 -> constant

    Examples:
    >>> check_is_type_of_horizontal_jux(CayleyPermutation([0, 1, 2]), [1, 1])
    True
    >>> check_is_type_of_horizontal_jux(CayleyPermutation([0, 1, 2]), [0, 0])
    False
    """
    if len(cperm) == 0:
        return True

    for line in range(len(cperm.cperm)):
        left = cperm.cperm[:line]
        right = cperm.cperm[line:]
        if (
            check_if_type(CayleyPermutation([]).standardise(left), class_to_check[0])
        ) and check_if_type(
            CayleyPermutation([]).standardise(right), class_to_check[1]
        ):
            return True
    return False
