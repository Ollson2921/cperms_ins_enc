"""This file enumerates Cayley permutation classes using the horizontal insertion
encoding by the tilings method.

Change the basis to any string of Cayley permutations.
They can be 1 based or 0 based and separated by anything.

If the class does not have a horizontal insertion encoding then an exception will be raised.
If it is then it will find a specification for it. The lines below can be used to
print the specification, print the generating function, and print how many Cayley
permutations there are in the class up to size n for any n.
"""

from cperms_ins_enc import HorizontalSearcher

basis = "210, 012, 100"

spec = HorizontalSearcher("basis").auto_search(max_expansion_time=60000, debug=True)

# ## Print the specification
# spec.show('')

# ## Print the generating function
# spec.get_genf('')

# ## Print the counts up to size n
# n = 10
# print('[spec.count_objects_of_size('i') for i in range('n')]')


# Exceptions = {
#     ("210, 120, 000"): ("(" ")(" "), horizontal"),
#     ("120, 012, 011"): ("(" ")(" "), horizontal"),
#     ("021, 012, 000"): ("(" ")(" "), horizontal"),
#     ("120, 102, 000"): ("(" ")(" "), horizontal"),
#     ("210, 012, 000"): ("(" ")(" "), horizontal"),
#     ("210, 012, 100"): ("(" ")(" "), horizontal"),
#     ("102, 012, 000"): ("(" ")(" "), horizontal"),
#     ("210, 201, 000"): ("(" ")(" "), horizontal"),
#     ("102, 021, 000"): ("(" ")(" "), horizontal"),
#     ("210, 021, 000"): ("(" ")(" "), horizontal"),
#     ("210, 012, 011"): ("(" ")(" "), horizontal"),
#     ("201, 012, 000"): ("(" ")(" "), horizontal"),
#     ("120, 201, 000"): ("(" ")(" "), horizontal"),
#     ("210, 102, 000"): ("(" ")(" "), horizontal"),
#     ("210, 102, 100"): ("(" ")(" "), horizontal"),
#     ("120, 012, 000"): ("(" ")(" "), horizontal"),
#     ("201, 021, 000"): ("(" ")(" "), horizontal"),
# }


# for basis in Exceptions.keys():
#     try:
#         spec = HorizontalSearcher(basis).auto_search(
#             max_expansion_time=60000, debug=True
#         )
#     except Exception as e:
#         print(f"Exception for basis {basis}: {e}")
#     input()
