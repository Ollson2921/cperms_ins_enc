"""This module is used for checking if a Cayley permutation
is a vertical juxtaposition and if a basis has a regular
vertical insertion encoding."""

from cperms_ins_enc import string_to_basis


def regular_vertical_insertion_encoding(basis: str) -> bool:
    """Checks if a basis has a regular insertion encoding.

    Example:
    >>> has_regular_insertion_encoding([CayleyPermutation([0, 1]),
      CayleyPermutation([1, 0])])
    True
    """
    basis = string_to_basis(str(basis))
    for i in range(3):
        for j in range(3):
            if any(checks_type(cperm.cperm, (i, j)) for cperm in basis):
                continue
            return False
    return True


def checks_type(cperm: list[int], class_to_check: tuple[int, int]) -> bool:
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
    if len(cperm) == 0 or len(cperm) == 1:
        return True
    elif class_to_check[1] == 0:
        return dec_bottom(cperm, class_to_check[0])
    elif class_to_check[1] == 1:
        return inc_bottom(cperm, class_to_check[0])
    elif class_to_check[1] == 2:
        return con_bottom(cperm, class_to_check[0])
    else:
        raise ValueError("Invalid class_to_check value. Must be 0, 1 or 2.")


def is_increasing(cperm: list[int]) -> bool:
    """Returns True if the Cayley permutation is strictly increasing."""
    if len(cperm) == 0:
        return True
    left = cperm[0]
    for idx in range(1, len(cperm)):
        if left >= cperm[idx]:
            return False
        left = cperm[idx]
    return True


def is_decreasing(cperm: list[int]) -> bool:
    """Returns True if the Cayley permutation is strictly decreasing."""
    if len(cperm) == 0:
        return True
    left = cperm[0]
    for idx in range(1, len(cperm)):
        if left <= cperm[idx]:
            return False
        left = cperm[idx]
    return True


def is_constant(cperm: list[int]) -> bool:
    """Returns True if the Cayley permutation is constant."""
    if len(cperm) == 0:
        return True
    left = cperm[0]
    for idx in range(1, len(cperm)):
        if left != cperm[idx]:
            return False
    return True


def seq_type(cperm: list[int], seqtype: int) -> bool:
    """Returns True if the Cayley permutation is of the type specified by the
    integer.
    0 -> strictly decreasing
    1 -> strictly increasing
    2 -> constant."""
    if seqtype == 0:
        return is_decreasing(cperm)
    elif seqtype == 1:
        return is_increasing(cperm)
    elif seqtype == 2:
        return is_constant(cperm)
    else:
        raise ValueError("Type must be 0, 1, or 2.")


def inc_bottom(cperm: list[int], seqtype: int) -> bool:
    """Returns True if the Cayley permutation is increasing on bottom
    and 'seqtype' on the top where:
    0 -> strictly decreasing
    1 -> strictly increasing
    2 -> constant."""
    if cperm.count(0) != 1:
        return False
    below_indices = [cperm.index(0)]
    above_vals = [val for val in cperm if val != 0]
    for val in range(1, max(cperm) + 1):
        if cperm.count(val) > 1:
            return False
        new_idx = cperm.index(val)
        if new_idx < below_indices[-1]:
            break
        above_vals.remove(val)
        below_indices.append(new_idx)
    return seq_type(above_vals, seqtype)


def con_bottom(cperm: list[int], seqtype: int) -> bool:
    """Returns True if the Cayley permutation is constant on bottom
    and 'seqtype' on the top where:
    0 -> strictly decreasing
    1 -> strictly increasing
    2 -> constant."""
    above_vals = [val for val in cperm if val != 0]
    return seq_type(above_vals, seqtype)


def dec_bottom(cperm: list[int], seqtype: int) -> bool:
    """Returns True if the Cayley permutation is decreasing on bottom
    and 'seqtype' on the top where:
    0 -> strictly decreasing
    1 -> strictly increasing
    2 -> constant."""
    if cperm.count(0) != 1:
        return False
    below_indices = [cperm.index(0)]
    above_vals = [val for val in cperm if val != 0]
    for val in range(1, max(cperm) + 1):
        if cperm.count(val) > 1:
            return False
        new_idx = cperm.index(val)
        if new_idx > below_indices[-1]:
            break
        above_vals.remove(val)
        below_indices.append(new_idx)
    return seq_type(above_vals, seqtype)
