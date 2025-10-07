"""Factors the tiling into sections that are independent of each other."""

from typing import Dict, Optional, Tuple, Iterator
from comb_spec_searcher import CartesianProductStrategy
from comb_spec_searcher.exception import StrategyDoesNotApply
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.factors import Factors


class FactorStrategy(CartesianProductStrategy[Tiling, GriddedCayleyPerm]):
    """Strategy for factoring tilings"""

    def __init__(
        self,
        ignore_parent: bool = True,
        workable: bool = True,
    ):
        super().__init__(
            ignore_parent=ignore_parent, workable=workable, inferrable=True
        )

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        factors = Factors(comb_class).find_factors()
        if not factors:
            raise StrategyDoesNotApply("No factors found.")
        return factors

    def extra_parameters(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[Dict[str, str], ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
            if children is None:
                raise StrategyDoesNotApply("Strategy does not apply")
        return tuple({} for _ in children)

    def formal_step(self) -> str:
        """
        Return a string that describe the operation performed on the tiling.
        """
        return "Factor the tiling into factors"

    def backward_map(
        self,
        comb_class: Tiling,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: Tiling,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Tuple[GriddedCayleyPerm, ...]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"ignore_parent={self.ignore_parent}, "
            f"workable={self.workable})"
        )

    # JSON methods

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("inferrable")
        d.pop("possibly_empty")
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "FactorStrategy":
        return cls(**d)


class RGFFactorStrategy(FactorStrategy):
    """Strategy for factoring tilings for the insertion encoding
    of RGFs."""

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        factors = Factors(comb_class).rgf_find_factors()
        if not factors:
            raise StrategyDoesNotApply("No factors found.")
        return factors

    def formal_step(self) -> str:
        """
        Return a string that describe the operation performed on the tiling.
        """
        return "Factor by removing points from the tiling"
