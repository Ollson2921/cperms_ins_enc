"""This module is used for checking if a sequence
is a horizontal juxtaposition and if a basis has a regular
horizontal insertion encoding."""

from cayley_permutations import string_to_basis, CayleyPermutation
from check_regular_ins_enc import seq_type

def rgf_regular_horizontal_insertion_encoding(
    basis: str | tuple[CayleyPermutation, ...],
) -> bool:
    """Checks if an RGF class has a regular horizontal insertion encoding.
    The basis must have Cayley permutations which are of the form
    increasing | increasing
    increasing | decreasing

    Example:
    >>> rgf_regular_horizontal_insertion_encoding("012, 210")
    True
    """
    basis = string_to_basis(basis) if isinstance(basis, str) else basis
    for j in range(2):
        if any(rgfinc_left(list(cperm), j) for cperm in basis):
            continue
        return False
    return True


def rgfinc_left(cperm: list[int], seqtype: int) -> bool:
    """Returns True if the left part of the sequence is strictly
    increasing and right is of type 'seqtype'.
    0 -> strictly decreasing
    1 -> strictly increasing"""
    if len(cperm) == 0 or len(cperm) == 1:
        return True
    left = cperm[0]
    for idx in range(1, len(cperm)):
        if left >= cperm[idx]:
            break
        left = cperm[idx]
    else:
        return True
    return seq_type(cperm[idx:], seqtype, [])
