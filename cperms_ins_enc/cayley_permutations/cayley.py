"""This module contains the CayleyPermutation class and functions for working with them."""

from itertools import combinations
from typing import Iterable, Tuple, List


class CayleyPermutation:
    """
    A Cayley Permutation is a list of integers with repeats allowed where
    if n is in the list, every k < n is in the list.
    Input to a Cayley permutation can zero based or one based and will
    be converted to zero based.

    Examples:
    >>> print(CayleyPermutation([0, 1, 2]))
    012
    >>> print(CayleyPermutation([1, 0, 2, 1]))
    1021
    """

    def __init__(self, cperm: Iterable[int]):
        """
        Checks that the input is a Cayley permutation and converts it to zero based if not already.
        """
        try:
            self.cperm: Tuple[int, ...] = tuple(cperm)
        except TypeError as error:
            raise TypeError(
                "Input to CayleyPermutation must be an iterable of ints."
            ) from error

        if len(self.cperm) != 0:
            for val in range(1, max(self.cperm)):
                if val not in self.cperm:
                    raise ValueError(
                        "Input to CayleyPermutation must be a Cayley permutation."
                    )

            if 0 not in self.cperm:
                self.cperm = tuple(x - 1 for x in self.cperm)

    def sub_cperms(self) -> Iterable["CayleyPermutation"]:
        """Returns all sub-Cayley permutations of the Cayley permutation."""
        sub_cperms = set()
        next_cperms = self.remove_one_point(self)
        while next_cperms:
            sub_cperms.update(next_cperms)
            next_cperms = [
                cperm for cperm in next_cperms for cperm in self.remove_one_point(cperm)
            ]
        return sub_cperms

    def remove_one_point(
        self, cperm: "CayleyPermutation"
    ) -> Iterable["CayleyPermutation"]:
        """Returns all sub-Cayley permutations that are the Cayley permutation with one point removed."""
        sub_cperms = set()
        if len(cperm) == 1:
            return sub_cperms
        for i in range(len(cperm)):
            sub_cperms.add(self.standardise((cperm.cperm[:i] + cperm.cperm[i + 1 :])))
        return sub_cperms

    @classmethod
    def of_size(cls, size: int) -> Iterable["CayleyPermutation"]:
        """
        Returns a list of all Cayley permutations of size 'size'.

        Examples:
        >>> CayleyPermutation.of_size(0)
        [CayleyPermutation([])]
        >>> CayleyPermutation.of_size(1)
        [CayleyPermutation([0])]
        >>> CayleyPermutation.of_size(2)
        [CayleyPermutation([1, 0]), CayleyPermutation([0, 1]), CayleyPermutation([0, 0])]
        """
        cperms: Iterable["CayleyPermutation"] = []
        if size == 0:
            return [CayleyPermutation([])]
        if size == 1:
            return [CayleyPermutation([0])]
        for cperm in CayleyPermutation.of_size(size - 1):
            cperms.extend(cperm.add_maximum())
        return cperms

    def insert(self, index, value):
        """Inserts value at index in the Cayley permutation."""
        return CayleyPermutation(self.cperm[:index] + [value] + self.cperm[index:])

    def subperm_from_indices(self, indices: List[int]) -> "CayleyPermutation":
        """Returns the Cayley permutation at the indices."""
        return CayleyPermutation.standardise([self.cperm[idx] for idx in indices])

    def indices_above_value(self, value: int) -> List[int]:
        """Returns a list of the indices of the values that
        are greater than or equal to the input value."""
        above_max_indices = []
        for idx, val in enumerate(self.cperm):
            if val >= value:
                above_max_indices.append(idx)
        return above_max_indices

    def add_maximum(self) -> Iterable["CayleyPermutation"]:
        """Adds a new maximum to the Cayley permutation in every possible way
        (one larger anywhere or the same as the current max at a smaller index).

        Example:
        >>> for cperm in CayleyPermutation([0, 1]).add_maximum():
        ...     print(cperm)
        201
        021
        012
        101
        011
        """
        val = max(self.cperm)
        index = self.cperm.index(val)
        perms = []
        for i in range(len(self.cperm) + 1):
            perms.append(
                CayleyPermutation(
                    [x for x in self.cperm[:i]]
                    + [val + 1]
                    + [x for x in self.cperm[i:]]
                )
            )
        for i in range(index + 1):
            perms.append(
                CayleyPermutation(
                    [x for x in self.cperm[:i]] + [val] + [x for x in self.cperm[i:]]
                )
            )
        return perms

    def contains(self, patterns: Iterable["CayleyPermutation"]) -> bool:
        """
        Input a list of patterns and returns true if contains any of them.

        Examples:
        >>> CayleyPermutation([0, 1, 2]).contains([CayleyPermutation([0, 1])])
        True
        >>> CayleyPermutation([0, 1, 2]).contains([CayleyPermutation([0, 1]),
        ... CayleyPermutation([1, 0])])
        True
        >>> CayleyPermutation([0, 1, 2]).contains([CayleyPermutation([1, 0])])
        False
        """
        return any(self.contains_pattern(pattern) for pattern in patterns)

    def contains_pattern(self, pattern: "CayleyPermutation") -> bool:
        """
        Input one pattern and returns true if the pattern is contained.

        Examples:
        >>> CayleyPermutation([0, 1, 2]).contains_pattern(CayleyPermutation([0, 1]))
        True
        >>> CayleyPermutation([0, 1, 2]).contains_pattern(CayleyPermutation([1, 0]))
        False
        """
        size = len(self)
        for indices in combinations(range(size), len(pattern)):
            occ = [self.cperm[idx] for idx in indices]
            stand = self.standardise(occ)
            if stand == pattern:
                return True
        return False

    def avoids(self, pattern: Iterable["CayleyPermutation"]) -> bool:
        """Returns true if the Cayley permutation avoids any of the patterns."""
        return not self.contains(pattern)

    def avoids_pattern(self, pattern: "CayleyPermutation") -> bool:
        """Returns true if the Cayley permutation avoids the pattern."""
        return not self.contains_pattern(pattern)

    @classmethod
    def standardise(cls, pattern: Iterable[int]) -> "CayleyPermutation":
        """Returns the standardised version of a pattern.

        Example:
        >>> CayleyPermutation.standardise([2, 3])
        CayleyPermutation([0, 1])
        """
        pattern = tuple(pattern)
        key = sorted(set(pattern))
        stand = {}
        for i, v in enumerate(key):
            stand[v] = i
        return CayleyPermutation([stand[pat] for pat in pattern])

    def first_k_entries(self, k: int) -> List[int]:
        """Returns a list of the indices of the first k numbers
        that were inserted in the Cayley permutation.

        Example:
        >>> CayleyPermutation([2, 0, 1, 2]).first_k_entries(2)
        [1, 2]
        >>> CayleyPermutation([0, 1, 0, 1, 2]).first_k_entries(3)
        [0, 2, 3]
        """
        current_min = 0
        indices: List[int] = []
        while len(indices) < k:
            mindices = []
            for idx, val in enumerate(self.cperm):
                if val == current_min:
                    mindices.append(idx)
            indices.extend(mindices[-(k - len(indices)) :])
            current_min += 1
        return sorted(indices)

    def last_k_entries(self, k: int) -> List[int]:
        """Returns a list of the indices of the last k numbers that were inserted.

        Example:
        >>> CayleyPermutation([2, 0, 1, 2]).last_k_entries(2)
        [0, 3]
        """
        current_max = max(self.cperm)
        indices: List[int] = []
        while len(indices) < k:
            maxindices = []
            for idx, val in enumerate(self.cperm):
                if val == current_max:
                    maxindices.append(idx)
            indices.extend(maxindices[: k - len(indices)])
            current_max -= 1
        return sorted(indices)

    def index_rightmost_max(self) -> int:
        """Returns the index of the rightmost maximum."""
        if len(self) == 0:
            return 1
        max_val = max(self)
        for idx, val in reversed(list(enumerate(self))):
            if val == max_val:
                return idx
        raise ValueError("No maximum found.")

    def occurrences(
        self, basis: Iterable["CayleyPermutation"]
    ) -> dict["CayleyPermutation", List[Tuple[int, ...]]]:
        """Returns a dictionary of the occurrences of a pattern in the basis
        and indices of the Cayley permutation where they occur.

        Example:
        >>> basis = [CayleyPermutation([0, 0])]
        >>> CayleyPermutation([0, 1, 2, 1, 2]).occurrences(basis)
        {CayleyPermutation([0, 0]): [(1, 3), (2, 4)]}
        """
        size = len(self)
        dict_of_occ_and_indices: dict["CayleyPermutation", List[Tuple[int, ...]]] = {}
        for pattern in basis:
            dict_of_occ_and_indices[pattern] = []
            for indices in combinations(range(size), len(pattern)):
                occ = [self.cperm[idx] for idx in indices]
                stand = self.standardise(occ)
                if stand == pattern:
                    dict_of_occ_and_indices[pattern].append(indices)
        return dict_of_occ_and_indices

    def avoids_same_after_deleting(
        self, basis: Iterable["CayleyPermutation"], index: int
    ) -> bool:
        """
        Returns true if the Cayley permutation avoids
        the basis still after deleting the index.
        """
        basis = tuple(basis)
        if self.contains(basis):
            cperm_deleted = self.delete_index(index)
            if not cperm_deleted.contains(basis):
                return False
        return True

    def delete_index(self, index: int) -> "CayleyPermutation":
        """Returns a Cayley permutation with the index deleted."""
        return CayleyPermutation.standardise(
            self.cperm[:index] + self.cperm[index + 1 :]
        )

    def to_jsonable(self) -> dict:
        """Returns a dictionary of the Cayley permutation."""
        return {"cperm": self.cperm}

    @classmethod
    def from_dict(cls, d: dict) -> "CayleyPermutation":
        """Returns a Cayley permutation from a dictionary."""
        return cls(d["cperm"])

    def __len__(self):
        return len(self.cperm)

    def __iter__(self):
        return iter(self.cperm)

    def __hash__(self):
        return hash(tuple(self.cperm))

    def __str__(self):
        if len(self) == 0:
            return "\u03b5"
        return "".join(str(x) if x < 10 else f"({str(x)})" for x in self.cperm)

    def __repr__(self):
        return "".join(str(x) if x < 10 else f"({str(x)})" for x in self.cperm)

    def __lt__(self, other: "CayleyPermutation") -> bool:
        return (len(self.cperm), self.cperm) < (len(other.cperm), other.cperm)

    def __le__(self, other: "CayleyPermutation") -> bool:
        return (len(self.cperm), self.cperm) <= (len(other.cperm), other.cperm)

    def __getitem__(self, key: int) -> int:
        return self.cperm[key]

    def __eq__(self, other) -> bool:
        return self.cperm == other.cperm
