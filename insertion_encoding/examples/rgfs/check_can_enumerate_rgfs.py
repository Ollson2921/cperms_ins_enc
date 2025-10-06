"""This module is for checking if an RGF class has a regular
insertion encoding.

The string `basis` can be changed to any string of basis patterns which are
one-based or zero-based and separated by anything.
"""

from insertion_encoding import (
    rgf_regular_vertical_insertion_encoding,
    rgf_regular_horizontal_insertion_encoding,
)

basis = "231, 312, 2121"

print(
    "Can enumerate with vertical insertion encoding:",
    rgf_regular_vertical_insertion_encoding(basis),
)

print(
    "Can enumerate with horizontal insertion encoding:",
    rgf_regular_horizontal_insertion_encoding(basis),
)
