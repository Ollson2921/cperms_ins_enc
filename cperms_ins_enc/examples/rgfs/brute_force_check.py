"""This file is for checking the counts of a class and the restricted
growth functions contained in the class by brute force."""

from cayley_permutations import Av, string_to_basis, CayleyPermutation


basis = "0132, 231, 41302"
basis_patterns = string_to_basis(basis)

## Prints all Cayley permutation of size 3 in the class Av{basis_patterns}
m = 3
print(f"Restricted growth functions of size {m} in the class Av{basis_patterns}:")
for cperm in Av(string_to_basis(basis)).generate_cperms(m):
    if cperm.is_rgf():
        print(cperm)


## Prints the number of Cayley permutations of size 0 to m in the class Av{basis_patterns}
m = 7
print(f"Number of restricted growth functions in the class Av{basis_patterns}:")
counts = []
for n in range(m):
    count = 0
    for cperm in Av(string_to_basis(basis)).generate_cperms(n):
        if cperm.is_rgf():
            count += 1
    counts.append(count)
print(counts)


## Print True if the Cayley permutation 'cperm' is a restricted growth function
cperm = CayleyPermutation([0, 1, 2, 3])
print(
    f"Is the Cayley permutation {cperm} a restricted growth function:", cperm.is_rgf()
)

## Print True if the Cayley permutation 'cperm' avoids the basis
cperm = CayleyPermutation([0, 1, 2, 3])
print(
    f"Is the Cayley permutation {cperm} in the class Av{tuple(basis_patterns)}:",
    Av(basis_patterns).in_class(cperm),
)
