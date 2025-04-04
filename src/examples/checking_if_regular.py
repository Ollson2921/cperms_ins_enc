"""This module is for checking if a Cayley permutation class has a regular insertion encoding."""

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
