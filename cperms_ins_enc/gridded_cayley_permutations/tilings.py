from typing import Iterable, Iterator, Tuple
from collections import defaultdict
from copy import copy
from itertools import product
from math import factorial
from comb_spec_searcher import CombinatorialClass

from ..cayley_permutations import CayleyPermutation
from .row_col_map import RowColMap
from .gridded_cayley_perms import GriddedCayleyPerm
from .simplify_obstructions_and_requirements import SimplifyObstructionsAndRequirements
from .minimal_gridded_cperms import MinimalGriddedCayleyPerm


def binomial(x, y):
    try:
        return factorial(x) // factorial(y) // factorial(x - y)
    except ValueError:
        return 0


class Tiling(CombinatorialClass):
    def __init__(
        self,
        obstructions: Iterable[GriddedCayleyPerm],
        requirements: Iterable[Iterable[GriddedCayleyPerm]],
        dimensions: Tuple[int, int],
    ) -> None:
        self.obstructions = tuple(obstructions)
        self.requirements = tuple(tuple(req) for req in requirements)
        self.dimensions = tuple(dimensions)

        algorithm = SimplifyObstructionsAndRequirements(
            self.obstructions, self.requirements, self.dimensions
        )
        algorithm.simplify()
        self.obstructions = algorithm.obstructions
        self.requirements = algorithm.requirements

    def _gridded_cayley_permutations(self, size: int) -> Iterator[GriddedCayleyPerm]:
        """
        Generating gridded Cayley permutations of size 'size'.
        """
        if size == 0:
            yield GriddedCayleyPerm(CayleyPermutation([]), [])
            return
        for gcp in self._gridded_cayley_permutations(size - 1):
            next_ins = gcp.next_insertions(self.dimensions)
            for val, cell in next_ins:
                next_gcp = gcp.insertion_different_value(val, cell)
                if self.satisfies_obstructions(next_gcp):
                    yield next_gcp
                if val in gcp.pattern.cperm:
                    if cell[1] == gcp.row_containing_value(val):
                        next_gcp = gcp.insertion_same_value(val, cell)
                        if self.satisfies_obstructions(next_gcp):
                            yield next_gcp

    def gridded_cayley_permutations(self, size: int) -> Iterator[GriddedCayleyPerm]:
        """Generating gridded Cayley permutations of size 'size' (that satisfy the requirements)."""
        yield from filter(
            self.satisfies_requirements, self._gridded_cayley_permutations(size)
        )

    def satisfies_obstructions(self, gcp: GriddedCayleyPerm) -> bool:
        """
        Checks whether a single gridded Cayley permutation satisfies the obstructions.
        """
        return not gcp.contains(self.obstructions)

    def satisfies_requirements(self, gcp: GriddedCayleyPerm) -> bool:
        """
        Checks whether a single gridded Cayley permutation satisfies the requirements.
        """
        for req in self.requirements:
            if not gcp.contains(req):
                return False
        return True

    def active_cells(self):
        """Returns the set of active cells in the tiling.
        (Cells are active if they do not contain a point obstruction.)"""
        active_cells = set(
            product(range(self.dimensions[0]), range(self.dimensions[1]))
        )
        for ob in self.obstructions:
            if len(ob) == 1:
                active_cells.discard(ob.positions[0])
        return active_cells

    def positive_cells(self):
        """Returns a set of cells that are positive in the tiling.
        (Cells are positive if they contain a point requirement.)"""
        positive_cells = set()
        for req_list in self.requirements:
            current = set(req_list[0].positions)
            for req in req_list:
                current = current.intersection(req.positions)
            positive_cells.update(current)
        return positive_cells

    def point_cells(self):
        """Returns the set of cells that can only contain a point."""
        point_cells = set()
        for cell in self.positive_cells():
            if (
                GriddedCayleyPerm(CayleyPermutation([0, 1]), [cell, cell])
                in self.obstructions
                and GriddedCayleyPerm(CayleyPermutation([1, 0]), [cell, cell])
                in self.obstructions
                and GriddedCayleyPerm(CayleyPermutation([0, 0]), [cell, cell])
                in self.obstructions
            ):
                point_cells.add(cell)
        return point_cells

    def delete_columns(self, cols: Iterable[int]) -> "Tiling":
        """
        Deletes columns at indices specified
        from the tiling and returns the new tiling.
        """
        col_map = {}
        counter = 0
        for ind in range(self.dimensions[0]):
            if ind in cols:
                continue
            col_map[ind] = counter
            counter += 1

        row_map = {i: i for i in range(self.dimensions[1])}
        rc_map = RowColMap(col_map, row_map)
        new_obstructions = [
            ob for ob in self.obstructions if not (ob.positions[0][0] in cols)
        ]

        new_obstructions = rc_map.map_gridded_cperms(new_obstructions)

        new_requirements = rc_map.map_requirements(self.requirements)
        new_dimensions = (
            self.dimensions[0] - len(cols),
            self.dimensions[1],
        )
        return Tiling(new_obstructions, new_requirements, new_dimensions)

    def delete_rows_and_columns(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> "Tiling":
        """
        Deletes rows and columns at indices specified
        from the tiling and returns the new tiling.
        """
        col_map = {}
        counter = 0
        for ind in range(self.dimensions[0]):
            if ind in cols:
                continue
            col_map[ind] = counter
            counter += 1

        row_map = {}
        counter = 0
        for ind in range(self.dimensions[1]):
            if ind in rows:
                continue
            row_map[ind] = counter
            counter += 1
        rc_map = RowColMap(col_map, row_map)
        new_obstructions = [
            ob
            for ob in self.obstructions
            if not (ob.positions[0][1] in rows or ob.positions[0][0] in cols)
        ]

        new_obstructions = rc_map.map_gridded_cperms(new_obstructions)

        new_requirements = rc_map.map_requirements(self.requirements)
        new_dimensions = (
            self.dimensions[0] - len(cols),
            self.dimensions[1] - len(rows),
        )
        return Tiling(new_obstructions, new_requirements, new_dimensions)

    def find_empty_rows_and_columns(self):
        """Returns a list of the indices of empty rows and
        a list of the indices of empty columns."""
        if self.dimensions == (0, 0):
            return [], []
        col_count = defaultdict(int)
        row_count = defaultdict(int)
        for ob in self.obstructions:
            if len(ob) == 1:
                col_count[ob.positions[0][0]] += 1
                row_count[ob.positions[0][1]] += 1
        empty_cols = []
        for col, count in col_count.items():
            if count == self.dimensions[1]:
                empty_cols.append(col)
        empty_rows = []
        for row, count in row_count.items():
            if count == self.dimensions[0]:
                empty_rows.append(row)
        return empty_cols, empty_rows

    def remove_empty_rows_and_columns(self):
        """Deletes any rows and columns in the gridding that are empty"""
        empty_cols, empty_rows = self.find_empty_rows_and_columns()
        return self.delete_rows_and_columns(empty_cols, empty_rows)

    def remove_empty_columns(self):
        """Deletes any columns in the gridding that are empty"""
        empty_cols, _ = self.find_empty_rows_and_columns()
        return self.delete_columns(empty_cols)

    def sub_tiling(self, cells: Iterable[Tuple[int, int]]) -> "Tiling":
        """
        Returns a sub-tiling of the tiling at the given cells.
        """
        cells = set(cells)
        obstructions = []
        for ob in self.obstructions:
            if all(cell in cells for cell in ob.positions):
                obstructions.append(ob)
        requirements = []
        for req_list in self.requirements:
            new_req_list = []
            for req in req_list:
                if all(cell in cells for cell in req.positions):
                    new_req_list.append(req)
            if new_req_list:
                requirements.append(new_req_list)
                # assert len(new_req_list) == len(req_list)

        for cell in product(range(self.dimensions[0]), range(self.dimensions[1])):
            if cell not in cells:
                obstructions.append(GriddedCayleyPerm(CayleyPermutation([0]), [cell]))

        return Tiling(obstructions, requirements, self.dimensions)

    def remove_requirements(self, reqs: Iterable[GriddedCayleyPerm]) -> "Tiling":
        """
        Returns a new tiling with the given requirements removed. (requirements, not req lists)
        """
        new_requirements = []
        for req_list in self.requirements:
            new_req_list = [req for req in req_list if req not in reqs]
            if new_req_list:
                new_requirements.append(new_req_list)
        return Tiling(self.obstructions, new_requirements, self.dimensions)

    ### Requirement insertion methods ###

    def add_obstructions(self, gcps: Iterable[GriddedCayleyPerm]) -> "Tiling":
        """
        Returns a new tiling with the given gridded Cayley permutations added as obstructions.
        """
        return Tiling(
            self.obstructions + tuple(gcps), self.requirements, self.dimensions
        )

    def add_obstruction(self, gcp: GriddedCayleyPerm) -> "Tiling":
        """
        Returns a new tiling with the given gridded Cayley permutation added as an obstruction.
        """
        return self.add_obstructions([gcp])

    def add_requirements(
        self, requirements: Iterable[Iterable[GriddedCayleyPerm]]
    ) -> "Tiling":
        """
        Returns a new tiling with the given requirements added.
        """
        return Tiling(
            self.obstructions, self.requirements + tuple(requirements), self.dimensions
        )

    def add_requirement_list(
        self, requirement_list: Iterable[GriddedCayleyPerm]
    ) -> "Tiling":
        """
        Returns a new tiling with the given requirement list added.
        """
        return self.add_requirements([requirement_list])

    def point_rows(self):
        """Returns the set of rows which only contain points of the same value."""
        point_rows = set()
        counter_dict = defaultdict(int)
        for ob in self.obstructions:
            if ob.pattern in (CayleyPermutation([0, 1]), CayleyPermutation([1, 0])):
                if ob.positions[0][1] == ob.positions[1][1]:
                    counter_dict[ob.positions[0][1]] += 1
        for row, count in counter_dict.items():
            n = len(self.cells_in_row(row))
            if 2 * binomial(n, 2) + 2 * n == count:
                point_rows.add(row)
        return point_rows

    def cells_in_row(self, row: int):
        """Returns the set of active cells in the given row."""
        cells = set()
        for cell in self.active_cells():
            if cell[1] == row:
                cells.add(cell)
        return cells

    def cells_in_col(self, col: int):
        """Returns the set of active cells in the given column."""
        cells = set()
        for cell in self.active_cells():
            if cell[0] == col:
                cells.add(cell)
        return cells

    def col_is_positive(self, col: int):
        req_list = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell])
            for cell in self.cells_in_col(col)
        )
        return self.add_obstructions(req_list).is_empty()

    def row_is_positive(self, row: int):
        req_list = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell])
            for cell in self.cells_in_row(row)
        )
        return self.add_obstructions(req_list).is_empty()

    ### CSS methods

    def to_jsonable(self) -> dict:
        res = {
            "obstructions": [ob.to_jsonable() for ob in self.obstructions],
            "requirements": [
                [req.to_jsonable() for req in req_list]
                for req_list in self.requirements
            ],
            "dimensions": self.dimensions,
        }
        res.update(super().to_jsonable())
        return res

    @classmethod
    def from_dict(cls, d):
        return Tiling(
            [GriddedCayleyPerm.from_dict(ob) for ob in d["obstructions"]],
            [
                [GriddedCayleyPerm.from_dict(req) for req in req_list]
                for req_list in d["requirements"]
            ],
            d["dimensions"],
        )

    def maximum_length_of_minimum_gridded_cayley_perm(self):
        return sum(max(len(gcp) for gcp in req_list) for req_list in self.requirements)

    def is_empty(self):
        return any(len(ob) == 0 for ob in self.obstructions) or self._is_empty()

    def _is_empty(self):
        for _ in self.minimal_gridded_cperms():
            return False
        return True

    def minimal_gridded_cperms(self) -> Iterator[GriddedCayleyPerm]:
        """Returns an iterator of minimal gridded Cayley permutations."""
        yield from MinimalGriddedCayleyPerm(
            self.obstructions, self.requirements
        ).minimal_gridded_cperms()

    def is_atom(self):
        return self.dimensions == (0, 0) or (
            self.dimensions == (1, 1)
            and (0, 0) in self.positive_cells()
            and GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)])
            in self.obstructions
            and GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)])
            in self.obstructions
            and GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])
            in self.obstructions
        )

    def minimum_size_of_object(self) -> int:
        assert not self.is_empty()
        i = 0
        while True:
            for _ in self.objects_of_size(i):
                return i
            i += 1

    def objects_of_size(self, n: int, **parameters: int) -> Iterator[GriddedCayleyPerm]:
        yield from self.gridded_cayley_permutations(n)

    def __repr__(self) -> str:
        return f"Tiling({self.obstructions}, {self.requirements}, {self.dimensions})"

    def __str__(self) -> str:
        if self.dimensions == (0, 0):
            if self.is_empty():
                return "+---+\n| ∅ |\n+---+\nDimensions (0, 0)\nKey:\n∅: Av(ε)\nCrossing obstructions:"
            else:
                return "+---+\n| # |\n+---+\nDimensions (0, 0)\nKey:\nCrossing obstructions:"

        crossing_string = "Crossing obstructions: \n"

        cell_basis = defaultdict(list)
        if any(len(ob) == 0 for ob in self.obstructions):
            for cell in self.active_cells():
                cell_basis[cell].append(CayleyPermutation([]))
        else:
            for ob in self.obstructions:
                if ob.is_local() and len(ob) > 0:
                    cell_basis[ob.positions[0]].append(ob.pattern)
                else:
                    crossing_string += str(ob) + "\n"
        basis_key = {}
        cell_key = {}
        for cell, basis in cell_basis.items():
            if tuple(basis) not in basis_key:
                if all(
                    p in basis
                    for p in [
                        CayleyPermutation([0, 0]),
                        CayleyPermutation([0, 1]),
                        CayleyPermutation([1, 0]),
                    ]
                ):
                    if cell in self.positive_cells():
                        cell_key[cell] = "\u25cf"
                    else:
                        cell_key[cell] = "\u25cb"
                    continue
                elif CayleyPermutation([0]) in basis:
                    cell_key[cell] = "#"
                    continue
                elif CayleyPermutation([]) in basis:
                    basis_key[tuple(basis)] = "\u2205"
                elif [CayleyPermutation([0, 0]), CayleyPermutation([0, 1])] == basis:
                    basis_key[tuple(basis)] = "/"
                elif [CayleyPermutation([0, 0]), CayleyPermutation([1, 0])] == basis:
                    basis_key[tuple(basis)] = "\\"
                else:
                    basis_key[tuple(basis)] = len(basis_key)
            cell_key[cell] = basis_key[tuple(basis)]

        requirements_string = ""
        for i, req_list in enumerate(self.requirements):
            requirements_string += f"Requirements {i}: \n"
            for req in req_list:
                requirements_string += f"{req} \n"

        n, m = self.dimensions
        edge_row = "---".join("+" for _ in range(n + 1)) + "\n"
        fill_row = "   ".join("|" for _ in range(n + 1)) + "\n"
        grid = fill_row.join(edge_row for _ in range(m + 1))
        fill_rows = [copy(fill_row) for _ in range(m)]
        for cell, key in cell_key.items():
            i, j = cell
            fill_rows[j] = (
                fill_rows[j][: 2 + 4 * i] + str(key) + fill_rows[j][3 + 4 * i :]
            )
        grid = edge_row + edge_row.join(reversed(fill_rows)) + edge_row

        key_string = "Key: \n"
        for basis, key in basis_key.items():
            basis_string = f"Av({','.join(str(p) for p in basis)})"
            key_string += f"{key}: {basis_string} \n"

        return grid + key_string + crossing_string + requirements_string

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tiling):
            return NotImplemented
        return (
            self.obstructions == other.obstructions
            and self.requirements == other.requirements
            and self.dimensions == other.dimensions
        )

    def __hash__(self) -> int:
        return hash((self.obstructions, self.requirements, self.dimensions))
