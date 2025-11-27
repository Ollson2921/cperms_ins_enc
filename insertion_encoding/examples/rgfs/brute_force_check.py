"""This file is for checking the counts of a class and the restricted
growth functions contained in the class by brute force."""

from cayley_permutations import string_to_basis, CayleyPermutation, CanonicalAv


basis = "0132, 231, 41302"
basis_patterns = string_to_basis(basis)

# Prints all Cayley permutation of size 3 in the class Av{basis_patterns}
m = 3
print(f"Restricted growth functions of size {m} in the class Av({basis}):")
for cperm in CanonicalAv(basis_patterns).generate_cperms(m):
    print(cperm)

print(f"Number of restricted growth functions length {m} in Av({basis})")
print(len(CanonicalAv(basis_patterns).generate_cperms(m)))

# Prints the number of Cayley permutations of size 0 to m in the class Av{basis_patterns}
m = 7
print(f"Number of restricted growth functions in the class Av({basis}):")
print(CanonicalAv(basis_patterns).counter(m))

# Print True if the Cayley permutation 'cperm' is a restricted growth function
cperm = CayleyPermutation([0, 1, 2, 3])
print(
    f"Is the Cayley permutation {cperm} a restricted growth function:", cperm.is_rgf()
)

# Print True if the RGF 'cperm' avoids the basis
cperm = CayleyPermutation([0, 1, 2, 3])
print(
    f"Is the restricted growth function {cperm} in the class Av({basis}):",
    CanonicalAv(basis_patterns).in_class(cperm),
)
