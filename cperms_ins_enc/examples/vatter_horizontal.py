"""This file enumerates Cayley permutation classes using the vertical insertion encoding
via our implementation of Vatter's method for permutation classes.

Change the basis to a string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class is not regular for vertical insertion encoding, an exception will be raised.
If it is then it will find a specification for it. The lines below can be used to
print the specification, print the generating function, and print how many Cayley
permutations there are in the class up to size n for any n.
"""

from cperms_ins_enc import (
    VatterHorizontalSearcher,
    HorizontalConfiguration,
    CayleyPermutation,
)


config = HorizontalConfiguration(CayleyPermutation([0, 1, 2, 3, 4, 5, 6]), [0.5])
basis = [CayleyPermutation([0, 0])]
print(config.candidates_to_delete())
print(config.deleteable_indices(basis))

for cperm in config.cayley_perms(config.bound(basis), []):
    print(cperm)

# basis = "12_11"

# spec = VatterHorizontalSearcher(basis).auto_search(max_expansion_time=6000)


# ## Print the specification
# spec.show()

# ## Print the generating function
# spec.get_genf()

# ## Print the counts up to size n
# n = 10
# print([spec.count_objects_of_size(i) for i in range(n)])
