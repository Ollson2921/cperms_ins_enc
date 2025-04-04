"""This file enumerates Cayley permutation classes using the horizontal insertion
encoding by the tilings method.

Change the basis to any string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class does not have a horizontal insertion encoding then an exception will be raised.
If it is then it will find a specification for it. The lines below can be used to
print the specification, print the generating function, and print how many Cayley
permutations there are in the class up to size n for any n.
"""

from tilescope import TileScope, TileScopePack
from comb_spec_searcher.rule_db import RuleDBForest
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import string_to_basis, Av
from horizontal_ins_enc import regular_horizontal_insertion_encoding

basis = "231, 321, 123"

from itertools import combinations
from cayley_permutations import CayleyPermutation

for m in range(1, 14):
    bases_size_3 = set(combinations(CayleyPermutation.of_size(3), m))
    for basis in bases_size_3:
        basis_patterns = basis
        if regular_horizontal_insertion_encoding(basis_patterns):
            tilings = Tiling(
                [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis_patterns],
                [],
                (1, 1),
            )
            scope = TileScope(
                tilings,
                TileScopePack.horizontal_insertion_encoding(),
                ruledb=RuleDBForest(),
            )
            try:
                spec = scope.auto_search(max_expansion_time=600)
                print(spec.get_genf())
                n = 10
                for i in range(n):
                    print(
                        f"Size {i}: ",
                        spec.count_objects_of_size(i),
                        len(Av(basis_patterns).generate_cperms(i)),
                    )
            except Exception:
                pass

# basis_patterns = string_to_basis(basis)

# if not regular_horizontal_insertion_encoding(basis_patterns):
#     raise Exception("Not a regular class for horizontal insertion encoding")

# tiling = Tiling(
#     [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis_patterns],
#     [],
#     (1, 1),
# )
# scope = TileScope(
#     tiling,
#     TileScopePack.horizontal_insertion_encoding(),
#     ruledb=RuleDBForest(),
# )
# spec = scope.auto_search(max_expansion_time=600)

# ## Print the specification
# # spec.show()

# ## Print the generating function
# print(spec.get_genf())

# ## Print the counts up to size n
# n = 10
# for i in range(n):
#     print(
#         f"Size {i}: ",
#         spec.count_objects_of_size(i),
#         len(Av(basis_patterns).generate_cperms(i)),
#     )
