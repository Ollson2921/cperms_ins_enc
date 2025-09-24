"""This file enumerates restricted growth functions using the vertical
insertion encoding by the tilings method.

Change the basis to any string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class is not regular for vertical insertion encoding, an exception will
be raised. If it is then it will find a specification for it. The lines below
can be used to print the specification, print the generating function, and
print how many restricted growth functions there are in the class up to
size n for any n.
"""

from cperms_ins_enc import RGFVerticalSearcher

# basis = "231,312,2121"


# spec = RGFVerticalSearcher(basis).auto_search(max_expansion_time=600)

# # Print the specification
# spec.show()

# # Print the generating function
# spec.get_genf()

# # Print the counts up to size n
# n = 10
# print([spec.count_objects_of_size(i) for i in range(n)])


from itertools import combinations
from cperms_ins_enc import CayleyPermutation
from cperms_ins_enc import Av, string_to_basis, CayleyPermutation
from cperms_ins_enc.check_regular import rgf_regular_vertical_insertion_encoding

for basis in combinations(CayleyPermutation.of_size(3), 3):
    if rgf_regular_vertical_insertion_encoding(basis) is False:
        continue
    spec = RGFVerticalSearcher(basis).auto_search(max_expansion_time=600)
    n = 8
    spec_counts = [spec.count_objects_of_size(i) for i in range(n)]
    print(spec_counts)
    counts = []
    for n in range(8):
        count = 0
        for cperm in Av(basis).generate_cperms(n):
            if cperm.is_rgf():
                count += 1
        counts.append(count)
    print(counts)
    assert spec_counts == counts
