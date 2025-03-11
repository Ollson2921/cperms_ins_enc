from tilescope import TileScope, TileScopePack
from comb_spec_searcher.rule_db import RuleDBForest
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation, Av
from itertools import combinations
from vertical_insertion_encoding import regular_vertical_insertion_encoding

number_of_terms_to_compare = 8

for m in range(1, 7):
    bases_size_3 = set(combinations(CayleyPermutation.of_size(3), m))
    for basis_patterns in bases_size_3:
        if not regular_vertical_insertion_encoding(basis_patterns):
            continue
        rules = []
        tiling = Tiling(
            [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis_patterns],
            [],
            (1, 1),
        )
        ruledb = RuleDBForest()
        scope = TileScope(
            tiling,
            TileScopePack.insertion_encoding(),
            debug=False,
            ruledb=ruledb,
        )
        try:
            spec = scope.auto_search(max_expansion_time=600)
        except Exception as e:
            continue

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
