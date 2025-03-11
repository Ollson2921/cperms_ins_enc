from tilescope import TileScope, TileScopePack
from comb_spec_searcher.rule_db import RuleDBForest
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import Av, string_to_basis
from vertical_insertion_encoding import regular_vertical_insertion_encoding
from horizontal_ins_enc import regular_horizontal_insertion_encoding


basis = "01, 10"

basis_patterns = string_to_basis(basis)

if not regular_vertical_insertion_encoding(basis_patterns):
    raise Exception("Not a regular class")

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

## Check counts are correct
number_of_terms_to_compare = 8

tilings_count = []
for i in range(number_of_terms_to_compare):
    tilings_count.append(spec.count_objects_of_size(i))

print(tilings_count)
brute_force_count = Av(basis_patterns).counter(number_of_terms_to_compare - 1)
print(brute_force_count)

if tilings_count != brute_force_count:
    with open(f"Error_for_Av{basis_patterns}.txt", "w") as f:
        f.write("Class Av(", basis_patterns, ")\n")
        f.write("Tilings count = ", tilings_count, "\n")
        f.write("Brute force count = ", brute_force_count, "\n")
    print("Error")
    print("Class Av(", basis_patterns, ")")
    print("Tilings count = ", tilings_count)
    print("Brute force count = ", brute_force_count)
    input()
