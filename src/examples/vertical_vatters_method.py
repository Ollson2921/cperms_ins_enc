from tilescope import TileScope, TileScopePack
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import string_to_basis, Av
from vertical_insertion_encoding import (
    regular_vertical_insertion_encoding,
    Configuration,
)
from vatters_method import ConfigAvoidingBasis, pack
from comb_spec_searcher import CombinatorialSpecificationSearcher

basis = "01, 00"

basis_patterns = string_to_basis(basis)

if not regular_vertical_insertion_encoding(basis_patterns):
    raise Exception("Not a regular class for vertical insertion encoding")


start_class = ConfigAvoidingBasis(Configuration(["🔹"]), basis_patterns)
searcher = CombinatorialSpecificationSearcher(start_class, pack)
spec = searcher.auto_search()


## Print the specification
# spec.show()

## Find counts and generating function
for i in range(10):
    print(spec.count_objects_of_size(i), Av(basis_patterns).generate_cperms(i))
print(spec.get_genf())
