from cperms_ins_enc.check_regular.check_regular_vert import (
    con_inc,
    con_con,
    con_dec,
    dec_inc,
    inc_inc,
    inc_con,
    dec_con,
)
from cperms_ins_enc.check_regular.check_regular_hori import is_increasing, is_decreasing
from cperms_ins_enc import string_to_basis


def rgf_conj_6_classes(basis: str) -> bool:
    """Checks if a basis of a RGF class has a regular insertion encoding.

    Example:
    >>> rgf_regular_vertical_insertion_encoding("01_10")
    True
    """
    basis = string_to_basis(str(basis))
    if not any(con_con(cperm.cperm) for cperm in basis):
        return False
    if not any(con_inc(cperm.cperm) for cperm in basis):
        return False
    if not any(greedy_grid_left(cperm.cperm, (0, 1)) for cperm in basis):
        return False
    if not any(greedy_grid_left(cperm.cperm, (1, 1)) for cperm in basis):
        return False
    if not any(grid_inc_con(cperm.cperm) for cperm in basis):
        return False
    if not any(grid_dec_con(cperm.cperm) for cperm in basis):
        return False
    return True


def rgf_conj_9_classes(basis: str) -> bool:
    """Checks if a basis of a RGF class has a regular insertion encoding.

    Example:
    >>> rgf_regular_vertical_insertion_encoding("01_10")
    True
    """
    basis = string_to_basis(str(basis))
    if not any(grid_dec_dec(cperm.cperm) for cperm in basis):
        print("dec_dec")
        return False
    if not any(grid_inc_dec(cperm.cperm) for cperm in basis):
        print("inc_dec")
        return False
    if not any(con_dec(cperm.cperm) for cperm in basis):
        return False
    return rgf_conj_6_classes(basis)


def greedy_grid_left(cperm: list[int], type: tuple[int, int]) -> bool:
    """Only use when increasing sequence on top

    Returns True if the sequence is griddable on a 2x2 grid
    where the bottom left cell is increasing, top left is empty,
    bottom right is type[0] (increasing or decreasing),
    and top right is type[1] (increasing, decreasing or constant)."""
    if len(cperm) == 0 or len(cperm) == 1:
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
    if len(remaining) == 0 or len(remaining) == 1:
        return True
    if type == (0, 1):
        return dec_inc(remaining, min_height)
    if type == (1, 1):
        return inc_inc(remaining, min_height)


def grid_inc_con(cperm: list[int]) -> bool:
    """Returns True if the sequence is increasing on bottom
    and constant on top."""
    if len(cperm) == 0 or len(cperm) == 1:
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
    and constant on top."""
    if len(cperm) == 0 or len(cperm) == 1:
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


# def grid_inc_dec(cperm: list[int]) -> bool:
#     """Returns True if the sequence is increasing on bottom
#     and decreasing on top with increasing at the start
#     (everything in grids)."""
#     print(cperm)
#     middle_val = cperm[-1]
#     print(middle_val)
#     last_val_top = middle_val
#     last_val_bottom = middle_val
#     top_vals = []
#     for val in cperm[-2::-1]:
#         if val < middle_val:
#             if val >= last_val_bottom:
#                 break
#             last_val_bottom = val
#         else:
#             if val <= last_val_top:
#                 break
#             last_val_top = val
#             top_vals.append(val)
#     else:
#         return True
#     remaining = cperm[:-2]
# print(remaining, "remaining")
# print(top_vals, "top vals")
# if not top_vals:
#     return is_increasing(remaining)
# last_val_top = top_vals[-1]
# first_val = remaining[0]
# for val in remaining:
#     if val <= first_val:
#         return False
#     if val >= last_val_top:
#         return False
#     first_val = val
# return True


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
    cperm = cperm[::-1]
    top_seq = []
    bottom_seq = []
    for idx, val in enumerate(cperm):
        if val == idx:
            bottom_seq.append(val)
        else:
            top_seq.append(val)
            break
    if not top_seq:
        return is_decreasing(cperm[idx + 1 :])
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
    if not is_decreasing(remaining):
        return False
    if not line > max(remaining):
        return False
    return True


# print(greedy_grid_left([0, 1, 2, 3, 4, 2, 5, 1, 6], (0, 1)))  # dec_inc passes
# print(check_gridding([0, 1, 2, 3, 6, 1, 5, 2, 4], (1, 0)))  # inc_dec passes

# print(greedy_grid_left([0, 1, 2, 4, 0, 5, 1, 6, 2], (1, 1)))  # inc_inc passes
# print(greedy_grid_left([0, 1, 2, 3, 0, 2, 3, 1], (1, 1)))  # inc_inc fails

# print(grid_inc_con([0, 1, 2, 3, 4, 0, 1, 5, 2, 5, 5, 3, 4]))  # inc_con passes
# print(grid_inc_con([0, 1, 2, 3, 4, 0, 1, 4, 2, 3]))  # inc_con passes
# print(grid_inc_con([0, 1, 2, 3, 2, 0, 2, 1, 2, 2]))  # inc_con fails


# print(check_gridding([0, 1, 2, 3, 6, 0, 5, 4, 1, 3, 2], (1, 0)))  # inc_dec fails
# print(rgf_conj_9_classes("010"))  # True
# print(rgf_conj_6_classes("010"))  # True


# basis = "120, 100, 000"
# basis = "120, 110, 000"

# print(rgf_conj_6_classes(basis))
# print(rgf_conj_9_classes(basis))

# print(grid_inc_dec([1, 2, 0])) # should be true
