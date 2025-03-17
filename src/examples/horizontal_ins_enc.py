from tilescope import TileScope, TileScopePack
from comb_spec_searcher.rule_db import RuleDBForest
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import string_to_basis
from horizontal_ins_enc import regular_horizontal_insertion_encoding

basis = "01"

basis_patterns = string_to_basis(basis)

if not regular_horizontal_insertion_encoding(basis_patterns):
    raise Exception("Not a regular class for vertical insertion encoding")

tiling = Tiling(
    [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis_patterns],
    [],
    (1, 1),
)
scope = TileScope(
    tiling,
    TileScopePack.horizontal_insertion_encoding(),
    ruledb=RuleDBForest(),
)
spec = scope.auto_search(max_expansion_time=600)

## Print the specification
spec.show()

## Find counts and generating function
for i in range(10):
    print(spec.count_objects_of_size(i))
print(spec.get_genf())
