"""This file enumerates Cayley permutation classes using the vertical insertion
encoding by the tilings method.

Change the basis to any string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class is not regular for vertical insertion encoding, an exception will be raised.
If it is then it will find a specification for it. The lines below can be used to
print the specification, print the generating function, and print how many Cayley
permutations there are in the class up to size n for any n.
"""

from cperms_ins_enc import VerticalSearcher

basis = "231,312,2121"

spec = VerticalSearcher(basis).auto_search(max_expansion_time=600)

## Print the specification
spec.show()

# ## Print the generating function
spec.get_genf()

# ## Print the counts up to size n
n = 10
print([spec.count_objects_of_size(i) for i in range(n)])
