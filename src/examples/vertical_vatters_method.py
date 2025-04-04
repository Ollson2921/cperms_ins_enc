"""This file enumerates Cayley permutation classes using the vertical insertion encoding
via our implementation of Vatter's method for permutation classes.

Change the basis to a string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class is not regular for vertical insertion encoding, an exception will be raised.
If it is then it will find a specification for it. The lines below can be used to
print the specification, print the generating function, and print how many Cayley
permutations there are in the class up to size n for any n.
"""

from tilescope import TileScope, TileScopePack
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import string_to_basis, Av
from vertical_insertion_encoding import (
    regular_vertical_insertion_encoding,
    Configuration,
)
from vatters_method import ConfigAvoidingBasis, pack
from comb_spec_searcher import CombinatorialSpecificationSearcher

basis = "12_11"

basis_patterns = string_to_basis(basis)

if not regular_vertical_insertion_encoding(basis_patterns):
    raise Exception("Not a regular class for vertical insertion encoding")


start_class = ConfigAvoidingBasis(Configuration(["🔹"]), basis_patterns)
searcher = CombinatorialSpecificationSearcher(start_class, pack)
spec = searcher.auto_search()


## Print the specification
spec.show()

## Print the generating function
print(spec.get_genf())

## Print the counts up to size n
n = 10
for i in range(n):
    print(
        f"Size {i}: ",
        spec.count_objects_of_size(i),
        Av(basis_patterns).generate_cperms(i),
    )
