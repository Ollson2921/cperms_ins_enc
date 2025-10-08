"""Strategies for inserting requirements into a tiling."""

from typing import Dict, Iterable, Iterator, Optional, Tuple
from comb_spec_searcher import DisjointUnionStrategy, StrategyFactory

from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from cayley_permutations import CayleyPermutation

Cell = Tuple[int, int]

# pylint: disable=duplicate-code

class RequirementInsertionStrategy(DisjointUnionStrategy[Tiling, GriddedCayleyPerm]):
    """Strategy for inserting requirements into a tiling."""

    def __init__(self, gcps: Iterable[GriddedCayleyPerm], ignore_parent: bool = False):
        super().__init__(ignore_parent=ignore_parent)
        self.gcps = frozenset(gcps)

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        return (
            comb_class.add_obstructions(self.gcps),
            comb_class.add_requirement_list(self.gcps),
        )

    def extra_parameters(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[Dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))

    def formal_step(self):
        return f"Either avoid or contain {self.gcps}"

    def backward_map(
        self,
        comb_class: Tiling,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: Tiling,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Tuple[Optional[GriddedCayleyPerm], ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"ignore_parent={self.ignore_parent})"

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        d.pop("possibly_empty")
        d["gcps"] = [gcp.to_jsonable() for gcp in self.gcps]
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "RequirementInsertionStrategy":
        gcps = tuple(GriddedCayleyPerm.from_dict(gcp) for gcp in d.pop("gcps"))
        return cls(gcps=gcps, **d)


class VerticalInsertionEncodingRequirementInsertionFactory(StrategyFactory[Tiling]):
    """Factory for creating RequirementInsertionStrategy to make columns positive
    for the vertical insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for col in range(comb_class.dimensions[0]):
            if not comb_class.col_is_positive(col):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_col(col)
                )
                strategy = RequirementInsertionStrategy(gcps, ignore_parent=True)
                yield strategy
                return

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "VerticalInsertionEncodingRequirementInsertionFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Make columns positive"


class HorizontalInsertionEncodingRequirementInsertionFactory(StrategyFactory[Tiling]):
    """Factory for creating RequirementInsertionStrategy to make rows positive
    for the horizontal insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for row in range(comb_class.dimensions[1]):
            if not comb_class.row_is_positive(row):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_row(row)
                )
                strategy = RequirementInsertionStrategy(gcps, ignore_parent=True)
                yield strategy

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "HorizontalInsertionEncodingRequirementInsertionFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Make rows positive"


class MatchingsRequirementInsertionStrategy(RequirementInsertionStrategy):
    """Strategy for inserting requirements into a tiling
    for enumerating restricted growth functions of matchings."""

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        reqs = [
            GriddedCayleyPerm(
                CayleyPermutation([0, 0]), [gcp.positions[0], gcp.positions[0]]
            )
            for gcp in self.gcps
        ]
        return (
            comb_class.add_obstructions(self.gcps),
            comb_class.add_requirement_list(reqs),
        )


class MatchingRequirementInsertionFactory(
    HorizontalInsertionEncodingRequirementInsertionFactory
):
    """Factory for creating MatchingsRequirementInsertionStrategy to make rows positive
    for the horizontal insertion encoding for enumerating restricted growth functions
    of matchings."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for row in range(comb_class.dimensions[1]):
            if not comb_class.row_is_positive(row):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_row(row)
                )
                strategy = MatchingsRequirementInsertionStrategy(
                    gcps, ignore_parent=True
                )
                yield strategy
