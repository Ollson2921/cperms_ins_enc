"""Factors the tiling into sections that are independent of each other."""

from typing import Dict, Iterator, Optional, Tuple
from comb_spec_searcher import CartesianProductStrategy
from comb_spec_searcher.exception import StrategyDoesNotApply
from ...gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from ...gridded_cayley_permutations.factors import Factors


class AbstractFactorStrategy:
    def __init__(
        self,
        ignore_parent: bool = True,
        workable: bool = True,
    ):
        # TODO: input should include partition: Iterable[Iterable[Cell]] to
        #       allow for interleaving factors.
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
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: Tiling,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Tuple[GriddedCayleyPerm, ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def __str__(self) -> str:
        return self.formal_step()

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
    def from_dict(cls, d: dict) -> "AbstractFactorStrategy":
        return cls(**d)


class FactorStrategy(
    AbstractFactorStrategy, CartesianProductStrategy[Tiling, GriddedCayleyPerm]
):
    pass
