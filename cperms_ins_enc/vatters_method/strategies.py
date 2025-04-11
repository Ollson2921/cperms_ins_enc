"""This module contains the specification searcher for the insertion encoding."""

from typing import Iterator, List, Tuple, Dict
from comb_spec_searcher import (
    CombinatorialObject,
    CombinatorialClass,
    DisjointUnionStrategy,
    CartesianProductStrategy,
    StrategyFactory,
)
from ..cayley_permutations import CayleyPermutation
from .vert_config import VerticalConfiguration
from .hori_config import HorizontalConfiguration


class CPermutation(CayleyPermutation, CombinatorialObject):
    """A Cayley permutation as a combinatorial object."""

    def size(self):
        return len(self)


class ConfigAvoidingBasis(CombinatorialClass[CPermutation]):
    """
    The set of Cayley permutations from the configuration avoiding the basis.
    """

    def __init__(self, config, basis: List[CayleyPermutation]) -> None:
        self.config = config
        self.basis = basis
        super().__init__()

    def is_empty(self):
        size = len(self.config)
        return not any(True for cperm in self.config.cayley_perms(size, self.basis))

    def to_jsonable(self) -> dict:
        raise NotImplementedError("TODO")

    @classmethod
    def from_dict(cls, d: dict):
        pass

    def __eq__(self, other):
        if not isinstance(other, ConfigAvoidingBasis):
            return False
        return bool(self.config == other.config and self.basis == other.basis)

    def __hash__(self):
        return hash(hash(self.config) + hash(tuple(self.basis)))

    def __repr__(self) -> str:
        return f"ConfigAvoidingBasis({repr(self.config)}, {repr(self.basis)})"

    def is_atom(self) -> bool:
        return self.config.is_cayley_perm()

    def minimum_size_of_object(self) -> int:
        return len(self.config)

    def objects_of_size(self, n: int, **parameters: int) -> Iterator[CPermutation]:
        for cperm in self.config.cayley_perms(n, self.basis):
            if len(cperm) == n:
                yield CPermutation(cperm.cperm)

    def __str__(self):
        return f"Configuration {self.config} avoiding basis {', '.join(str(p) for p in self.basis)}"


class ApplyLetterStrategy(DisjointUnionStrategy[ConfigAvoidingBasis, CPermutation]):
    """Applies all possible letters of the insertion encoding."""

    def decomposition_function(
        self, comb_class: ConfigAvoidingBasis
    ) -> Tuple[ConfigAvoidingBasis, ...] | None:
        children = []
        for child in comb_class.config.children():
            children.append(ConfigAvoidingBasis(child, comb_class.basis))
        return tuple(children)

    def formal_step(self) -> str:
        return "Applies all possible letters of the insertion encoding."

    def forward_map(
        self,
        comb_class: ConfigAvoidingBasis,
        obj: CPermutation,
        children: Tuple[ConfigAvoidingBasis, ...] | None = None,
    ) -> Tuple[CPermutation | None, ...]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, d: Dict) -> "ApplyLetterStrategy":
        return cls()


class VertDeleteIndexStrategy(
    CartesianProductStrategy[ConfigAvoidingBasis, CPermutation]
):
    """Deletes an index from the configuration."""

    def __init__(
        self,
        indx: int,
        ignore_parent: bool = True,
        inferrable: bool = False,
        possibly_empty: bool = False,
        workable: bool = True,
    ):
        # pylint: disable=too-many-arguments
        self.index = indx
        super().__init__(ignore_parent, inferrable, possibly_empty, workable)

    def decomposition_function(
        self, comb_class: ConfigAvoidingBasis
    ) -> Tuple[ConfigAvoidingBasis, ...] | None:
        deleted = comb_class.config.delete_index(self.index)
        atom = VerticalConfiguration([1])
        return (
            ConfigAvoidingBasis(deleted, comb_class.basis),
            ConfigAvoidingBasis(atom, comb_class.basis),
        )

    def formal_step(self):
        return f"Removing index {self.index}."

    def backward_map(
        self,
        comb_class: ConfigAvoidingBasis,
        objs: Tuple[CPermutation | None, ...],
        children: Tuple[ConfigAvoidingBasis, ...] | None = None,
    ) -> Iterator[CPermutation]:
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: ConfigAvoidingBasis,
        obj: CPermutation,
        children: Tuple[ConfigAvoidingBasis, ...] | None = None,
    ) -> Tuple[CPermutation | None, ...]:
        raise NotImplementedError

    def to_jsonable(self) -> dict:
        d = super().to_jsonable()
        d["index"] = self.index
        return d

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d.pop("index"), **d)


class HoriDeleteIndexStrategy(VertDeleteIndexStrategy):
    def decomposition_function(
        self, comb_class: ConfigAvoidingBasis
    ) -> Tuple[ConfigAvoidingBasis, ...] | None:
        deleted = comb_class.config.delete_index(self.index)
        atom = HorizontalConfiguration(CayleyPermutation([1]))
        return (
            ConfigAvoidingBasis(deleted, comb_class.basis),
            ConfigAvoidingBasis(atom, comb_class.basis),
        )


class VertIndexDeletingFactory(StrategyFactory):
    """Creates index deleting strategies."""

    def __call__(
        self, configuration: ConfigAvoidingBasis
    ) -> Iterator[VertDeleteIndexStrategy]:
        for index in configuration.config.deleteable_indices(configuration.basis):
            yield VertDeleteIndexStrategy(index)

    def __str__(self):
        return "Index deleting factory."

    def __repr__(self):
        return "IndexDeletingFactory()"

    def to_jsonable(self):
        pass

    @classmethod
    def from_dict(cls, d: dict):
        pass


class HoriIndexDeletingFactory(VertIndexDeletingFactory):
    def __call__(
        self, configuration: ConfigAvoidingBasis
    ) -> Iterator[HoriDeleteIndexStrategy]:
        for index in configuration.config.deleteable_indices(configuration.basis):
            yield HoriDeleteIndexStrategy(index)
