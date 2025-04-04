"""This file enumerates Cayley permutation classes using the vertical insertion
encoding by the tilings method.

Change the basis to any string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class is not regular for vertical insertion encoding, an exception will be raised.
If it is then it will find a specification for it. The lines below can be used to
print the specification, print the generating function, and print how many Cayley
permutations there are in the class up to size n for any n.
"""

from tilescope import TileScope, TileScopePack
from comb_spec_searcher.rule_db import RuleDBForest
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import string_to_basis
from vertical_insertion_encoding import regular_vertical_insertion_encoding

basis = "01"

basis_patterns = string_to_basis(basis)

if not regular_vertical_insertion_encoding(basis_patterns):
    raise Exception("Not a regular class for vertical insertion encoding")

tiling = Tiling(
    [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis_patterns],
    [],
    (1, 1),
)
scope = TileScope(
    tiling,
    TileScopePack.vertical_insertion_encoding(),
    ruledb=RuleDBForest(),
)
spec = scope.auto_search(max_expansion_time=600)

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
        # Av(basis_patterns).generate_cperms(i),
    )
