from comb_spec_searcher import StrategyPack, AtomStrategy
from .strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    FactorStrategy,
    HorizontalInsertionEncodingPlacementFactory,
    HorizontalInsertionEncodingRequirementInsertionFactory,
    RGFHorizontalInsertionEncodingPlacementFactory,
    MatchingRequirementInsertionFactory,
)
from ..check_regular import (
    regular_horizontal_insertion_encoding,
    rgf_regular_horizontal_insertion_encoding,
)
from .generic_searcher import GenericSearcher
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm

from cayley_permutations import CayleyPermutation


class HorizontalSearcher(GenericSearcher):
    def regular_check(self):
        return regular_horizontal_insertion_encoding(self.basis)

    def type_of_encoding(self):
        return "horizontal"

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
                HorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[HorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )


class RGFHorizontalSearcher(HorizontalSearcher):
    """A searcher for the horizontal insertion encoding for
    enumerating restricted growth functions."""

    def regular_check(self):
        return rgf_regular_horizontal_insertion_encoding(self.basis)

    def type_of_encoding(self):
        return "RGF horizontal"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                FactorStrategy(),
                HorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[RGFHorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="RGF Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )


class MatchingHorizontalSearcher(RGFHorizontalSearcher):
    """A searcher for the horizontal insertion encoding for
    enumerating restricted growth functions."""

    def type_of_encoding(self):
        return "RGFs of matchings horizontal"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                FactorStrategy(),
                MatchingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[RGFHorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="RGFs of Matchings Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    def start_class(self):
        return (
            super()
            .start_class()
            .add_obstruction(
                GriddedCayleyPerm(
                    CayleyPermutation([0, 0, 0]), [(0, 0), (0, 0), (0, 0)]
                )
            )
        )
