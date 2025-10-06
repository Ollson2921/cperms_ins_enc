"""Module for doing the insertion encoding for Cayley
permutations in a way more similar to Vatter's method for permutations."""

from .vatter_searchers import VatterVerticalSearcher, VatterHorizontalSearcher
from .hori_config import HorizontalConfiguration

__all__ = [
    "VatterVerticalSearcher",
    "VatterHorizontalSearcher",
    "HorizontalConfiguration",
]
