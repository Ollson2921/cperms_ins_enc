from cperms_ins_enc.check_regular import regular_horizontal_insertion_encoding, rgf_regular_horizontal_insertion_encoding
from cperms_ins_enc.check_regular.check_regular_hori import dec_left, rgfinc_left

from cayley_permutations import CayleyPermutation, Av

def test_hori_regular_check_fail():
    """Test that this class should fail as they are not permutations"""
    assert regular_horizontal_insertion_encoding("132, 212") is False
    assert dec_left([1, 0, 1], 1) is False


def test_hori_regular_check_pass():
    """Test that this class should pass."""
    assert regular_horizontal_insertion_encoding("132, 213")
    assert dec_left([1, 0, 2], 1)


def test_rgf_hori_regular_check():
    decreasing = [CayleyPermutation([0, 0]), CayleyPermutation([0, 1])]
    increasing = [CayleyPermutation([0, 0]), CayleyPermutation([1, 0])]
    constant = [CayleyPermutation([1, 0]), CayleyPermutation([0, 1])]

    def generate_some_rgf_hori_jux(left_sequence, right_sequence, size):
        """Generates all vertical juxtaposisiont of size 'size' of type
        bottom_sequence above top_sequence which are bases."""
        horizontal_jux = set()
        for n in range(size + 1):
            for a_perm in Av(left_sequence).generate_cperms(n):
                for b_perm in Av(right_sequence).generate_cperms(size - n):
                    concatenation = a_perm + b_perm
                    horizontal_jux.add(CayleyPermutation(concatenation))
        return horizontal_jux

    for n in range(10):
        for cperm in generate_some_rgf_hori_jux(increasing, increasing, n):
            assert rgfinc_left(cperm, 1), f"Failed for {cperm}, is not inc_inc horizontal jux."
        for cperm in generate_some_rgf_hori_jux(increasing, decreasing, n):
            assert rgfinc_left(cperm, 0), f"Failed for {cperm}, is not inc_dec horizontal jux."
