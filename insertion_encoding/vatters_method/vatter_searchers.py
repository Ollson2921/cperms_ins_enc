"""Searchers for insertion encoding adapted from
Vatter's method."""

from comb_spec_searcher import (
    StrategyPack,
    AtomStrategy,
)
from cayley_permutations import CayleyPermutation
from check_regular_ins_enc import (
    regular_horizontal_insertion_encoding,
    regular_vertical_insertion_encoding,
)
from ..tilescope.generic_searcher import GenericSearcher
from .vert_config import VerticalConfiguration
from .hori_config import HorizontalConfiguration
from .strategies import (
    VertIndexDeletingFactory,
    HoriIndexDeletingFactory,
    ApplyLetterStrategy,
    ConfigAvoidingBasis,
)


class VatterVerticalSearcher(GenericSearcher):
    """A searcher for the vertical insertion encoding adapted from Vatter's method."""

    def regular_check(self):
        return regular_vertical_insertion_encoding(self.basis)

    def type_of_encoding(self):
        return "vertical"

    def start_class(self):
        return ConfigAvoidingBasis(VerticalConfiguration(["🔹"]), self.basis)

    def pack(self):
        return StrategyPack(
            initial_strats=[VertIndexDeletingFactory()],
            inferral_strats=[],
            expansion_strats=[[ApplyLetterStrategy()]],
            ver_strats=[AtomStrategy()],
            name="Vertical insertion encoding with Vatter's method.",
        )


class VatterHorizontalSearcher(GenericSearcher):
    """A searcher for the horizontal insertion encoding adapted from Vatter's method."""

    def regular_check(self):
        return regular_horizontal_insertion_encoding(self.basis)

    def type_of_encoding(self):
        return "horizontal"

    def start_class(self):
        return ConfigAvoidingBasis(
            HorizontalConfiguration(CayleyPermutation([]), [-0.5]), self.basis
        )

    def pack(self):
        return StrategyPack(
            initial_strats=[HoriIndexDeletingFactory()],
            inferral_strats=[],
            expansion_strats=[[ApplyLetterStrategy()]],
            ver_strats=[AtomStrategy()],
            name="Horizontal insertion encoding with Vatter's method.",
        )
