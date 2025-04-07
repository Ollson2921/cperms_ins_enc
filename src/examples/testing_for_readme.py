from cayley_permutations import CayleyPermutation, string_to_basis

# cperm = CayleyPermu
print(string_to_basis("0123, 231, 41302"))

print((CayleyPermutation((0, 1, 2, 3)), CayleyPermutation((1, 2, 0))))

print(
    [
        CayleyPermutation((0, 1, 2, 3)),
        CayleyPermutation((1, 2, 0)),
        CayleyPermutation((4, 1, 3, 0, 2)),
    ]
)
print(string_to_basis("0123, 231"))

print(string_to_basis("0123, 231, 41302"))  # As 41302 contains 120 it is removed
