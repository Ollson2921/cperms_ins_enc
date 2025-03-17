from vertical_insertion_encoding import regular_vertical_insertion_encoding
from horizontal_ins_enc import regular_horizontal_insertion_encoding
from cayley_permutations import CayleyPermutation
from itertools import combinations

v_reg = 0
h_reg = 0
both = 0
total = 0
for m in range(1, 14):
    bases_size_3 = set(combinations(CayleyPermutation.of_size(3), m))
    for basis in bases_size_3:
        total += 1
        if regular_vertical_insertion_encoding(
            basis
        ) or regular_horizontal_insertion_encoding(basis):
            both += 1
        if regular_vertical_insertion_encoding(basis):
            v_reg += 1
        if regular_horizontal_insertion_encoding(basis):
            h_reg += 1
print('Classes with a vertical insertion encoding', v_reg)
print('Classes with a horizontal insertion encoding', h_reg)
print('Classes with both a vertical and horizontal insertion encoding', both)
print('Total classes', total)
