"""This module is used for checking if a sequence
is a horizontal juxtaposition and if a basis has a regular
horizontal insertion encoding."""

from cperms_ins_enc import string_to_basis


def is_increasing(cperm: list[int], vals_seen=set()) -> bool:
    """Returns True if the sequence is strictly increasing.
    Also checks that no vals in vals_seen occur in the sequence."""
    if cperm[0] in vals_seen:
        return False
    if len(cperm) == 0:
        return True
    left = cperm[0]
    for idx in range(1, len(cperm)):
        if left >= cperm[idx]:
            return False
        if cperm[idx] in vals_seen:
            return False
        left = cperm[idx]
    return True


def is_decreasing(cperm: list[int], vals_seen=set()) -> bool:
    """Returns True if the sequence is strictly decreasing.
    Also checks that no vals in vals_seen occur in the sequence."""
    if cperm[0] in vals_seen:
        return False
    if len(cperm) == 0 and cperm[0] not in vals_seen:
        return True
    left = cperm[0]
    for idx in range(1, len(cperm)):
        if left <= cperm[idx]:
            return False
        if cperm[idx] in vals_seen:
            return False
        left = cperm[idx]
    return True


def is_constant(cperm: list[int], vals_seen=set()) -> bool:
    """Returns True if the sequence is constant.
    Also checks that no vals in vals_seen occur in the sequence."""
    if cperm[0] in vals_seen:
        return False
    if len(cperm) == 0 and cperm[0] not in vals_seen:
        return True
    left = cperm[0]
    for idx in range(1, len(cperm)):
        if left != cperm[idx]:
            return False
        if cperm[idx] in vals_seen:
            return False
    return True


def seq_type(cperm: list[int], seqtype: int, vals_seen=set()) -> bool:
    """Returns True if the sequence is of the type specified by the
    integer.
    0 -> strictly decreasing
    1 -> strictly increasing
    2 -> constant.
    Also checks that no vals in vals_seen occur in the sequence."""
    if seqtype == 0:
        return is_decreasing(cperm, vals_seen)
    elif seqtype == 1:
        return is_increasing(cperm, vals_seen)
    elif seqtype == 2:
        return is_constant(cperm, vals_seen)
    else:
        raise ValueError("Type must be 0, 1, or 2.")


def regular_horizontal_insertion_encoding(basis: str) -> bool:
    """Checks if a basis has a regular insertion encoding.
    The basis must have permutations which are of the form
    increasing | increasing
    decreasing | decreasing
    increasing | decreasing
    decreasing | increasing

    Example:
    >>> has_regular_insertion_encoding("012, 210")
    True
    """
    basis = string_to_basis(str(basis))
    for i in range(2):
        for j in range(2):
            if any(checks_hori_type(cperm, (i, j)) for cperm in basis):
                continue
            return False
    return True


def checks_hori_type(cperm: list[int], class_to_check: tuple[int, int]) -> bool:
    """
    Returns True if the sequence is a vertical juxtaposition
    of the type specified by the tuple.
    In the tuple the first element is above, the second element is below.
    0 -> strictly decreasing
    1 -> strictly increasing

    Examples:
    >>> checks_type([0, 1, 2], (1, 1))
    True
    >>> checks_type([0, 1, 2], (0, 0))
    False
    """
    if len(cperm) == 0 or len(cperm) == 1:
        return True
    if class_to_check[1] == 0:
        return dec_left(cperm, class_to_check[0])
    elif class_to_check[1] == 1:
        return inc_left(cperm, class_to_check[0])
    else:
        raise ValueError("Invalid class_to_check value. Must be 0 or 1.")


def inc_left(cperm: list[int], seqtype: int) -> bool:
    """Returns True if the left part of the sequence is strictly
    increasing and right is of type 'seqtype'.
    0 -> strictly decreasing
    1 -> strictly increasing"""
    left = cperm[0]
    vals_seen = set([left])
    for idx in range(1, len(cperm)):
        if left >= cperm[idx]:
            break
        left = cperm[idx]
        vals_seen.add(left)
    else:
        return True
    return seq_type(cperm[idx:], seqtype, vals_seen)


def dec_left(cperm: list[int], seqtype: int) -> bool:
    """Returns True if the left part of the sequence is strictly
    increasing and right is of type 'seqtype'.
    0 -> strictly decreasing
    1 -> strictly increasing"""
    left = cperm[0]
    vals_seen = set([left])
    for idx in range(1, len(cperm)):
        if left <= cperm[idx]:
            break
        left = cperm[idx]
        vals_seen.add(left)
    else:
        return True
    return seq_type(cperm[idx:], seqtype, vals_seen)
