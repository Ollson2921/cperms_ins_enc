"""A searcher for the vertical insertion encoding."""

from comb_spec_searcher import StrategyPack, AtomStrategy
from check_regular_ins_enc import (
    regular_vertical_insertion_encoding,
)
from .strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    FactorStrategy,
    RGFFactorStrategy,
    VerticalInsertionEncodingPlacementFactory,
    VerticalInsertionEncodingRequirementInsertionFactory,
    RGFVerticalInsertionEncodingPlacementFactory,
)
from ..check_regular import (
    rgf_regular_vertical_insertion_encoding,
)
from .generic_searcher import GenericTilingsSearcher


class VerticalSearcher(GenericTilingsSearcher):
    """A searcher for the vertical insertion encoding."""

    def regular_check(self):
        return regular_vertical_insertion_encoding(self.basis)

    def type_of_encoding(self):
        return "vertical"

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
                RGFFactorStrategy(),
                VerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[RGFVerticalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="RGF Vertical Insertion Encoding",
            symmetries=[],
            iterative=False,
        )
