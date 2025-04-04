"""This module is for checking if a Cayley permutation class has a regular insertion encoding.

The string `basis` can be changed to any string of basis patterns or `basis_patterns` can be changed directly to an iterable of CayleyPermutations.
"""

from vertical_insertion_encoding import regular_vertical_insertion_encoding
from horizontal_ins_enc import regular_horizontal_insertion_encoding
from cayley_permutations import string_to_basis

basis = "01"

basis_patterns = string_to_basis(basis)

print(
    "Has a regular vertical insertion encoding:",
    regular_vertical_insertion_encoding(basis_patterns),
)

print(
    "Has a regular horizontal insertion encoding:",
    regular_horizontal_insertion_encoding(basis_patterns),
)
