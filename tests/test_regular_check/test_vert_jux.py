from itertools import combinations
from typing import List, Iterator
from insertion_encoding.check_regular.check_regular_vert import checks_vert_type

from cayley_permutations import CayleyPermutation, Av

decreasing = [CayleyPermutation([0, 0]), CayleyPermutation([0, 1])]
increasing = [CayleyPermutation([0, 0]), CayleyPermutation([1, 0])]
constant = [CayleyPermutation([1, 0]), CayleyPermutation([0, 1])]


def shuffle(list_a: List[int], list_b: List[int]) -> Iterator[List[int]]:
    """Returns all possible shuffles of two lists list_a and list_b.

    Example:
    >>> for shuff in CayleyPermutation.shuffle([1, 2], [3, 4]):
    ...     print(shuff)
    [1, 2, 3, 4]
    [1, 3, 2, 4]
    [1, 3, 4, 2]
    [3, 1, 2, 4]
    [3, 1, 4, 2]
    [3, 4, 1, 2]
    """
    length_a = len(list_a)
    length_b = len(list_b)
    for a_indices in combinations(range(length_a + length_b), length_a):
        b_indices = [i for i in range(length_a + length_b) if i not in a_indices]
        shuff = list(range(length_a + length_b))
        for idx_a, idx_shuff in enumerate(a_indices):
            shuff[idx_shuff] = list_a[idx_a]
        for idx_b, idx_shuff in enumerate(b_indices):
            shuff[idx_shuff] = list_b[idx_b]
        yield list(shuff)


def generate_vertical_jux(top_sequence, bottom_sequence, size):
    """Generates all vertical juxtaposisiont of size 'size' of type
    bottom_sequence above top_sequence which are bases."""
    vertical_jux = set()
    for n in range(size + 1):
        for a_perm in Av(bottom_sequence).generate_cperms(n):
            for b_perm in Av(top_sequence).generate_cperms(size - n):
                if a_perm:
                    max_a = max(a_perm)
                    b_perm_new = [val + max_a + 1 for val in b_perm]
                else:
                    b_perm_new = b_perm
                for shuff in shuffle(a_perm, b_perm_new):
                    vertical_jux.add(CayleyPermutation(shuff))
    return vertical_jux


def test_inc_inc():
    """Test vertical jux of form inc on top, inc on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(increasing, increasing, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (1, 1)
            ), f"Failed for {cperm} of size {size}, is not inc_inc vertical jux."


def test_inc_dec():
    """Test vertical jux of form inc on top, dec on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(increasing, decreasing, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (1, 0)
            ), f"Failed for {cperm} of size {size}, is not inc_dec vertical jux"


def test_inc_con():
    """Test vertical jux of form inc on top, con on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(increasing, constant, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (1, 2)
            ), f"Failed for {cperm} of size {size}, is not inc_con vertical jux"


def test_dec_inc():
    """Test vertical jux of form dec on top, inc on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(decreasing, increasing, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (0, 1)
            ), f"Failed for {cperm} of size {size}, is not dec_inc vertical jux"


def test_dec_dec():
    """Test vertical jux of form dec on top, dec on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(decreasing, decreasing, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (0, 0)
            ), f"Failed for {cperm} of size {size}, is not dec_dec vertical jux"


def test_dec_con():
    """Test vertical jux of form dec on top, con on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(decreasing, constant, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (0, 2)
            ), f"Failed for {cperm} of size {size}, is not dec_con vertical jux"


def test_con_inc():
    """Test vertical jux of form con on top, inc on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(constant, increasing, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (2, 1)
            ), f"Failed for {cperm} of size {size}, is not con_inc vertical jux"


def test_con_dec():
    """Test vertical jux of form con on top, dec on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(constant, decreasing, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (2, 0)
            ), f"Failed for {cperm} of size {size}, is not con_dec vertical jux"


def test_con_con():
    """Test vertical jux of form con on top, con on bottom pass check."""
    for size in range(1, 6):
        vertical_jux = generate_vertical_jux(constant, constant, size)
        for cperm in vertical_jux:
            assert checks_vert_type(
                cperm, (2, 2)
            ), f"Failed for {cperm} of size {size}, is not con_con vertical jux"
