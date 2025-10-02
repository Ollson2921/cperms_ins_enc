"""Check the Cayley permutations in a class, the counts and if a specific
Cayley permutation is in the class by brute force."""

from cayley_permutations import Av, string_to_basis, CayleyPermutation


basis = "0132, 231, 41302"
basis_patterns = string_to_basis(basis)

# Prints all Cayley permutation of size 3 in the class Av{basis_patterns}
m = 3
print(Av(basis_patterns).generate_cperms(m))

# Prints the number of Cayley permutations of size 0 to n in the class Av{basis_patterns}
n = 7
print(Av(basis_patterns).counter(n))

# Print True if the Cayley permutation 'cperm' avoids the basis
cperm = CayleyPermutation([0, 1, 2, 3])
print(
    f"Is the Cayley permutation {cperm} in the class Av{tuple(basis_patterns)}:",
    Av(basis_patterns).in_class(cperm),
)
