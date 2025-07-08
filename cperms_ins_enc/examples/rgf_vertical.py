"""This file enumerates restricted growth functions using the vertical insertion
encoding by the tilings method.

Change the basis to any string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class is not regular for vertical insertion encoding, an exception will be raised.
If it is then it will find a specification for it. The lines below can be used to
print the specification, print the generating function, and print how many restricted
growth functions there are in the class up to size n for any n.
"""

from cperms_ins_enc.check_regular import rgf_conj_9_classes, rgf_conj_6_classes
from cperms_ins_enc import RGFVerticalSearcher

from cperms_ins_enc import (
    regular_vertical_insertion_encoding,
    regular_horizontal_insertion_encoding,
    CayleyPermutation,
)

# basis = "231,312,2121"


# spec = RGFVerticalSearcher(basis).auto_search(max_expansion_time=600)

# ## Print the specification
# # spec.show()

# # # ## Print the generating function
# spec.get_genf()

# # # ## Print the counts up to size n
# n = 10
# print([spec.count_objects_of_size(i) for i in range(n)])


from itertools import combinations


total = 0
for m in range(3, 14):
    bases_size_3 = set(combinations(CayleyPermutation.of_size(4), m))
    # conj_6_enumerated = 0
    # conj_9_enumerated = 0
    # conj_6_exception = 0
    # conj_9_exception = 0
    for basis in bases_size_3:
        total += 1
        if rgf_conj_6_classes(basis) and not rgf_conj_9_classes(basis):
            try:
                print(f"{basis} passes 6 conditions but fails all 9")
                spec = RGFVerticalSearcher(basis).auto_search(max_expansion_time=6000)
                print("computed")
                input()
                # if rgf_conj_9_classes(str(basis)):
                #     conj_9_enumerated += 1
                # else:
                #     print("Computed but failed 9 classes check for", basis)
                #     input()
                # if rgf_conj_6_classes(str(basis)):
                #     conj_6_enumerated += 1
                # else:
                #     print("Computed but failed 6 classes check for", basis)
                #     input()
            except Exception as e:
                # if rgf_conj_9_classes(str(basis)):
                #     conj_9_exception += 1
                # if rgf_conj_6_classes(str(basis)):
                # conj_6_exception += 1
                print(f"Exception for {basis}: {e}")
        print(f"Number of bases tried: {total}")
    # print("Conj 6 enumerated:", conj_6_enumerated)
    # print("Conj 9 enumerated:", conj_9_enumerated)
    # print("Conj 6 exception:", conj_6_exception)
    # print("Conj 9 exception:", conj_9_exception)
    # print("Total:", total)
