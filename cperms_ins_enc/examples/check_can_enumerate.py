"""This module is for checking if a Cayley permutation class has a regular insertion encoding.

The string `basis` can be changed to any string of basis patterns which are one-based or
zero-based and separated by anything.
"""

from check_regular import (
    regular_vertical_insertion_encoding,
    regular_horizontal_insertion_encoding,
)

basis = "01"

print(
    "Can enumerate with vertical insertion encoding:",
    regular_vertical_insertion_encoding(basis),
)

print(
    "Can enumerate with horizontal insertion encoding:",
    regular_horizontal_insertion_encoding(basis),
)
