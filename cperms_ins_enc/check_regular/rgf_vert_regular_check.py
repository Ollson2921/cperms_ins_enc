"""Functions to check if a basis of a RGF class has a regular insertion encoding."""

from cayley_permutations import string_to_basis, CayleyPermutation
from cperms_ins_enc.check_regular.check_regular_vert import (
    con_inc,
    con_con,
    con_dec,
    dec_inc,
    inc_inc,
    inc_con,
    dec_con,
)
from cperms_ins_enc.check_regular.check_regular_hori import is_decreasing


def rgf_regular_vertical_insertion_encoding(
    basis: str | tuple[CayleyPermutation],
) -> bool:
    """Checks if a basis of a RGF class has a regular insertion encoding.

    Example:
    >>> rgf_regular_vertical_insertion_encoding("01_10")
    True
    """
    basis = string_to_basis(basis) if isinstance(basis, str) else basis
    if not check_jux(basis):
        return False
    if not check_greedy_grids(basis):
        return False
    if not check_grids(basis):
        return False
    return True


def check_grids(basis: tuple[CayleyPermutation]) -> bool:
    """checks for the grid classes"""
    if not any(grid_dec_dec(cperm) for cperm in basis):
        return False
    if not any(grid_inc_dec(cperm) for cperm in basis):
        return False
    if not any(grid_inc_con(cperm) for cperm in basis):
        return False
    if not any(grid_dec_con(cperm) for cperm in basis):
        return False
    return True


def check_greedy_grids(basis: tuple[CayleyPermutation]) -> bool:
    """Checks for the grid classes which are greedy left gridded."""
    if not any(greedy_grid_left(cperm, 0) for cperm in basis):
        return False
    if not any(greedy_grid_left(cperm, 1) for cperm in basis):
        return False
    return True


def check_jux(basis: tuple[CayleyPermutation]) -> bool:
    """Checks for the vertical juxtapositions"""
    if not any(con_dec(cperm) for cperm in basis):
        return False
    if not any(con_con(cperm) for cperm in basis):
        return False
    if not any(con_inc(cperm) for cperm in basis):
        return False
    return True


def greedy_grid_left(cperm: list[int], type_of_seq: int) -> bool:
    """Only use when increasing sequence on top

    Returns True if the sequence is griddable on a 2x2 grid
    where the bottom left cell is increasing, top left is empty,
    bottom right is of type 'type_of_seq' where
    0 -> decreasing
    1 -> increasing
    and top right is increasing."""
    if len(cperm) < 3:
        return True
    left = cperm[0]
    for idx in range(1, len(cperm)):
        if left >= cperm[idx]:
            break
        left = cperm[idx]
    else:
        return True
    min_height = left
    remaining = cperm[idx:]
    if len(remaining) < 2:
        return True
    if type_of_seq == 0:
        return dec_inc(remaining, min_height)
    if type_of_seq == 1:
        return inc_inc(remaining, min_height)
    raise ValueError(
        "Type must be 0 for decreasing or 1 for increasing, "
        f"got {type_of_seq} instead."
    )


def grid_inc_con(cperm: list[int]) -> bool:
    """Returns True if the sequence is increasing on bottom
    and constant on top."""
    if len(cperm) < 3:
        return True
    max_val = max(cperm)
    left = cperm[0]
    if left == max_val:
        return inc_con(cperm[1:])
    for idx in range(1, len(cperm)):
        if left >= cperm[idx] or cperm[idx] == max_val:
            break
        left = cperm[idx]
    else:
        return True
    remaining = cperm[idx:]
    return inc_con(remaining)


def grid_dec_con(cperm: list[int]) -> bool:
    """Returns True if the sequence is increasing on bottom
    and constant on top with an increasing sequence at the start."""
    if len(cperm) < 3:
        return True
    max_val = max(cperm)
    left = cperm[0]
    if left == max_val:
        return dec_con(cperm[1:])
    for idx in range(1, len(cperm)):
        if left >= cperm[idx] or cperm[idx] == max_val:
            break
        left = cperm[idx]
    else:
        return True
    remaining = cperm[idx:]
    return dec_con(remaining)


def grid_inc_dec(cperm: list[int]) -> bool:
    """Returns True if the sequence is increasing on bottom
    and decreasing on top with increasing at the start
    (everything in grids)."""
    if len(cperm) < 3:
        return True
    cperm = cperm[::-1]
    middle_val = cperm[0]
    last_val_top = middle_val
    last_val_bottom = middle_val
    top_vals = []
    for idx, val in enumerate(cperm[1:]):
        if val <= middle_val:
            if val >= last_val_bottom:
                break
            last_val_bottom = val
        else:
            if val <= last_val_top:
                break
            last_val_top = val
            top_vals.append(val)
    else:
        return True
    remaining = cperm[idx + 1 :]
    if top_vals:
        if remaining[0] > top_vals[0]:
            return False
    return is_decreasing(remaining)


def grid_dec_dec(cperm: list[int]) -> bool:
    """Returns True if the sequence is decreasing on bottom
    and decreasing on top. with increasing sequence at the start
    (everything in grids)."""
    # pylint: disable=too-many-branches
    if len(cperm) < 3:
        return True
    cperm = cperm[::-1]
    top_seq = []
    bottom_seq = []
    idx = 0
    for idx, val in enumerate(cperm):
        if val == idx:
            bottom_seq.append(val)
        else:
            if len(bottom_seq) > 0 and val <= bottom_seq[-1]:
                break
            top_seq.append(val)
            break
    if not top_seq:
        return is_decreasing(cperm[idx:])
    line = top_seq[0]
    start_index = len(bottom_seq) + 1

    for val in cperm[start_index:]:
        if val < line:
            if not bottom_seq:
                bottom_seq.append(val)
            elif val <= bottom_seq[-1]:
                break
            bottom_seq.append(val)
        else:
            if val <= top_seq[-1]:
                break
            top_seq.append(val)

    remaining = cperm[len(bottom_seq) + len(top_seq) + 1 :]
    if not remaining:
        return True
    if not is_decreasing(remaining) or not line > max(remaining):
        return False
    return True
