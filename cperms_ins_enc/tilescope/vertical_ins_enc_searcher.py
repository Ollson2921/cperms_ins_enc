from comb_spec_searcher import StrategyPack, AtomStrategy
from .strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    FactorStrategy,
    VerticalInsertionEncodingPlacementFactory,
    VerticalInsertionEncodingRequirementInsertionFactory,
    RGFVerticalInsertionEncodingPlacementFactory,
)
from ..check_regular import (
    regular_vertical_insertion_encoding,
    rgf_regular_vertical_insertion_encoding,
)
from .generic_searcher import GenericSearcher
from ..gridded_cayley_permutations import Tiling, GriddedCayleyPerm


class VerticalSearcher(GenericSearcher):
    def regular_check(self):
        return regular_vertical_insertion_encoding(self.basis)

    def type_of_encoding(self):
        return "vertical"

    def start_class(self):
        return Tiling(
            [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in self.basis],
            [],
            (1, 1),
        )

    def pack(self):
        return StrategyPack(
            initial_strats=[
                FactorStrategy(),
                VerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[VerticalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Vertical Insertion Encoding",
            symmetries=[],
            iterative=False,
        )


class RGFVerticalSearcher(VerticalSearcher):
    """A searcher for the vertical insertion encoding for
    enumerating restricted growth functions."""

    def regular_check(self):
        return rgf_regular_vertical_insertion_encoding(self.basis)

    def type_of_encoding(self):
        return "RGF vertical"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                FactorStrategy(),
                VerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[RGFVerticalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="RGF Vertical Insertion Encoding",
            symmetries=[],
            iterative=False,
        )
