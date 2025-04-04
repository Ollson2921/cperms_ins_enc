from comb_spec_searcher import StrategyPack, AtomStrategy
from .strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    FactorStrategy,
    VerticalInsertionEncodingPlacementFactory,
    HorizontalInsertionEncodingPlacementFactory,
    VerticalInsertionEncodingRequirementInsertionFactory,
    HorizontalInsertionEncodingRequirementInsertionFactory,
)


class TileScopePack(StrategyPack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def vertical_insertion_encoding(cls):
        return TileScopePack(
            initial_strats=[
                FactorStrategy(),
                VerticalInsertionEncodingRequirementInsertionFactory(),
            ],  # Iterable[Strategy]
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],  # Iterable[Strategy]
            expansion_strats=[
                [VerticalInsertionEncodingPlacementFactory()]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[AtomStrategy()],  # Iterable[Strategy]
            name="Vertical Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def horizontal_insertion_encoding(cls):
        return TileScopePack(
            initial_strats=[
                FactorStrategy(),
                HorizontalInsertionEncodingRequirementInsertionFactory(),
            ],  # Iterable[Strategy]
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],  # Iterable[Strategy]
            expansion_strats=[
                [HorizontalInsertionEncodingPlacementFactory()]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[AtomStrategy()],  # Iterable[Strategy]
            name="Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )
