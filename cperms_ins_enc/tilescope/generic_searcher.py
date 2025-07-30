import abc
from comb_spec_searcher import CombinatorialSpecificationSearcher
from ..cayley_permutations import string_to_basis
from functools import cached_property


class GenericSearcher(abc.ABC):
    def __init__(self, basis: str):
        if isinstance(basis, str):
            self.basis = string_to_basis(basis)
        else:
            self.basis = basis
        if not self.regular_check():
            raise Exception(
                f"The class Av{tuple(self.basis)} can not be enumerated with {self.type_of_encoding()} insertion encoding"
            )

    @abc.abstractmethod
    def type_of_encoding(self):
        """Returns the type of encoding."""

    @abc.abstractmethod
    def start_class(self):
        """Returns the starting class - a tiling or configuration avoiding a basis."""

    @abc.abstractmethod
    def regular_check(self):
        """Checks if the class can be enumerated with the given insertion encoding."""

    @abc.abstractmethod
    def pack(self):
        """Returns the strategy pack."""

    @cached_property
    def comb_spec_searcher(self) -> CombinatorialSpecificationSearcher:
        """Returns the CombinatorialSpecificationSearcher object for this searcher."""
        return CombinatorialSpecificationSearcher(
            self.start_class(), self.pack(), debug=debug
        )

    def auto_search(
        self, max_expansion_time=600, debug=False
    ) -> CombinatorialSpecificationSearcher:
        """Search for a specification."""
        return self.comb_spec_searcher(debug=debug).auto_search(
            max_expansion_time=max_expansion_time
        )
