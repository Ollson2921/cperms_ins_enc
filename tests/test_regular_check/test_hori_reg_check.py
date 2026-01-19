"""Tests the horizontal insertion encoding check on some rgf
horizontal juxtapositions."""

from insertion_encoding.check_regular.check_regular_hori import rgfinc_left

from cayley_permutations import CayleyPermutation, Av


def test_rgf_hori_regular_check():
    decreasing = [CayleyPermutation([0, 0]), CayleyPermutation([0, 1])]
    increasing = [CayleyPermutation([0, 0]), CayleyPermutation([1, 0])]

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
            assert rgfinc_left(
                cperm, 1
            ), f"Failed for {cperm}, is not inc_inc horizontal jux."
        for cperm in generate_some_rgf_hori_jux(increasing, decreasing, n):
            assert rgfinc_left(
                cperm, 0
            ), f"Failed for {cperm}, is not inc_dec horizontal jux."
