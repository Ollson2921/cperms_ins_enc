from comb_spec_searcher import StrategyPack, AtomStrategy
from .strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    FactorStrategy,
    HorizontalInsertionEncodingPlacementFactory,
    HorizontalInsertionEncodingRequirementInsertionFactory,
)
from ..check_regular import regular_horizontal_insertion_encoding
from .generic_searcher import GenericSearcher
from ..gridded_cayley_permutations import Tiling, GriddedCayleyPerm


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
