"""This file enumerates Cayley permutation classes using the horizontal insertion
encoding by the tilings method.

Change the basis to any string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class does not have a horizontal insertion encoding then an exception will be raised.
If it is then it will find a specification for it. The lines below can be used to
print the specification, print the generating function, and print how many Cayley
permutations there are in the class up to size n for any n.
"""

from searchers import HorizontalSearcher

basis = "01, 10"

from check_regular import (
    regular_horizontal_insertion_encoding,
)
from cayley_permutations import string_to_basis

print(regular_horizontal_insertion_encoding(string_to_basis(basis)))

spec = HorizontalSearcher(basis).auto_search(max_expansion_time=600)

## Print the specification
# spec.show()

## Print the generating function
print(spec.get_genf())

## Print the counts up to size n
n = 10
for i in range(n):
    print(
        f"Size {i}: ",
        spec.count_objects_of_size(i),
    )
