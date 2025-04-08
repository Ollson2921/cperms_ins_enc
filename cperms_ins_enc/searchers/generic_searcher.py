from comb_spec_searcher import CombinatorialSpecificationSearcher
from cayley_permutations import string_to_basis
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm


class GenericSearcher:
    def __init__(self, basis: str):
        self.basis = string_to_basis(basis)
        if not self.regular_check():
            raise Exception(
                f"The class Av{tuple(self.basis)} can not be enumerated with {self.type_of_encoding()} insertion encoding"
            )

    def type_of_encoding(self):
        raise NotImplementedError("This method is not implemented yet.")

    def start_class(self):
        raise NotImplementedError("This method is not implemented yet.")

    def regular_check(self):
        raise NotImplementedError("This method is not implemented yet.")

    def pack(self):
        raise NotImplementedError("This method is not implemented yet.")

    def comb_spec_searcher(self) -> CombinatorialSpecificationSearcher:
        """Returns the CombinatorialSpecificationSearcher object for this searcher."""
        return CombinatorialSpecificationSearcher(
            self.start_class(),
            self.pack(),
        )

    def auto_search(
        self,
        max_expansion_time=600,
    ) -> CombinatorialSpecificationSearcher:
        """Search for a specification."""
        return self.comb_spec_searcher().auto_search(
            max_expansion_time=max_expansion_time,
        )
