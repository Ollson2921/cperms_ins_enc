"""This file counts the number of RGF classes
that have a regular insertion encoding, either vertical or horizontal."""

from cayley_permutations import CayleyPermutation
from itertools import combinations
from insertion_encoding import (
    rgf_regular_vertical_insertion_encoding,
    rgf_regular_horizontal_insertion_encoding,
)

v_reg = 0
h_reg = 0
both = 0
total = 0
for m in range(1, 14):
    bases_size_3 = set(combinations(CayleyPermutation.of_size(3), m))
    for basis in bases_size_3:
        total += 1
        if rgf_regular_vertical_insertion_encoding(
            basis
        ) or rgf_regular_horizontal_insertion_encoding(basis):
            both += 1
        if rgf_regular_vertical_insertion_encoding(basis):
            v_reg += 1
        if rgf_regular_horizontal_insertion_encoding(basis):
            h_reg += 1

print("RGF classes with a vertical insertion encoding", v_reg)
print("RGF classes with a horizontal insertion encoding", h_reg)
print("RGF classes with either a vertical or horizontal insertion encoding", both)
print("Total RGF classes", total)
