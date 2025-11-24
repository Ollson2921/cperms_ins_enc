"""Package for checking when different types of insertion encoding
on Cayley permutations, restricted growth functions and restricted
growth functions of mapplings are regular."""

from .check_regular_hori import (
    rgf_regular_horizontal_insertion_encoding,
)
from .rgf_vert_regular_check import rgf_regular_vertical_insertion_encoding

__all__ = [
    "rgf_regular_horizontal_insertion_encoding",
    "rgf_regular_vertical_insertion_encoding",
]
