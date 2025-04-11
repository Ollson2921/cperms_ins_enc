from typing import List, Iterable, Iterator
from math import ceil
from ..cayley_permutations import CayleyPermutation, Av
from .vert_config import VerticalConfiguration


class Letter:
    """A letter has three values. The first is one of {u, m, d, f},
    the second is the index of the slot to be be inserted into
    and the third dictates if there are more occurrences of the same value to come."""

    def __init__(self, letter: str, index: int, repeat: int):
        self.letter = letter
        self.index = index
        self.repeat = repeat
        if self.letter not in ("m", "u", "d", "f"):
            raise ValueError("Letter must be one of m, u, d, f.")

    def apply(self, config: "HorizontalConfiguration") -> "HorizontalConfiguration":
        """Applies a letter to a configuration."""
        if isinstance(config.slots[self.index], int):
            if self.letter != "f":
                raise ValueError("Can only apply f to a constant slot.")
        if self.letter == "m":
            return self.apply_m(config, self.index, self.repeat)
        if self.letter == "u":
            return self.apply_u(config, self.index, self.repeat)
        if self.letter == "d":
            return self.apply_d(config, self.index, self.repeat)
        if self.letter == "f":
            return self.apply_f(config, self.index, self.repeat)
        raise ValueError

    def apply_m(
        self, config: "HorizontalConfiguration", index: int, repeat: int
    ) -> "HorizontalConfiguration":
        """Change "🔹" to: "🔹", max_value + repeat, "🔹"."""
        return config.apply_m(index, repeat)

    def apply_u(
        self, config: "HorizontalConfiguration", index: int, repeat: int
    ) -> "HorizontalConfiguration":
        """Change "🔹" to: max_value + repeat, "🔹"."""
        return config.apply_u(index, repeat)

    def apply_d(
        self, config: "HorizontalConfiguration", index: int, repeat: int
    ) -> "HorizontalConfiguration":
        """Change "🔹" to: "🔹", max_value + repeat."""
        return config.apply_d(index, repeat)

    def apply_f(
        self, config: "HorizontalConfiguration", index: int, repeat: int
    ) -> "HorizontalConfiguration":
        """Change "🔹" to: max_value + repeat."""
        return config.apply_f(index, repeat)

    def __str__(self):
        return f"{self.letter}_{self.index, self.repeat}"

    @classmethod
    def from_string(cls, letter: str) -> "Letter":
        """Returns a Letter from a string."""
        letter, index, repeat = letter.split("_")
        return cls(letter, int(index), int(repeat))


class HorizontalConfiguration(VerticalConfiguration):
    """A configuration is a mixture of points and slots.
    cperm is a list of values which form the start of the Cayley permutation.
    slots is a list of values where the slots currently are. If the value
    is a decimal then it is a normal slot between two values and if it is an
    integer it is a constant slot.

    The configuration with just a slot is HorizontalConfiguration(CayleyPermutation([]), [-0.5])
    """

    def __init__(self, cperm: CayleyPermutation, slots: Iterable[int]):
        self.cperm = cperm
        if not isinstance(cperm, CayleyPermutation):
            print(cperm, "is not a Cayley permutation.")
            raise ValueError("cperm must be a Cayley permutation.")
        self.slots = sorted(set(slots))

    def apply_m(self, index: int, repeat: int) -> "HorizontalConfiguration":
        new_cperm, slots, value_added = self.apply_letter(index, repeat)

        new_slots = (
            slots[:index] + [value_added - 0.5] + [value_added + 0.5] + slots[index:]
        )
        return self.__class__(new_cperm, new_slots)

    def apply_u(self, index: int, repeat: int) -> "HorizontalConfiguration":
        new_cperm, slots, value_added = self.apply_letter(index, repeat)
        new_slots = slots[:index] + [value_added - 0.5] + slots[index:]
        return self.__class__(new_cperm, new_slots)

    def apply_d(self, index: int, repeat: int) -> "HorizontalConfiguration":
        new_cperm, slots, value_added = self.apply_letter(index, repeat)
        new_slots = slots[:index] + [value_added + 0.5] + slots[index:]
        return self.__class__(new_cperm, new_slots)

    def apply_f(self, index: int, repeat: int) -> "HorizontalConfiguration":
        new_cperm, new_slots, _ = self.apply_letter(index, repeat)
        return self.__class__(new_cperm, new_slots)

    def apply_letter(self, index: int, repeat: int) -> "HorizontalConfiguration":
        """Find value of the slot at that index. To place a point, add that value
        to the end of the cperm and anything strictly larger than it increases by
        1 (if it was a constant slot then anything else on that level would not
        increase). - this is the same for all letters, maybe separate function.
        If slot was not a constant slot then ceil to next int.
        - also need to remove the slot from the list - if was a repeat then add
        a constant slot at the value added.

        For f, don't do anything else.
        For u, add a slot at value_added - 0.5.
        for d, add a slot at value_added + 0.5.
        For m, add a slot at value_added - 0.5 and value_added + 0.5.
        Make sure slots are always in increasing order (count slots from bottom up)."""
        value_to_add = self.slots[index]
        if value_to_add in self.cperm:
            new_cperm = list(self.cperm) + [value_to_add]
            slots = self.slots
        else:
            new_cperm = [
                val if val <= value_to_add else val + 1 for val in self.cperm
            ] + [ceil(value_to_add)]
            slots = [val if val <= value_to_add else val + 1 for val in self.slots]
        if repeat:
            new_slots = slots[:index] + [ceil(value_to_add)] + slots[index + 1 :]
        else:
            new_slots = slots[:index] + slots[index + 1 :]
        return CayleyPermutation(new_cperm), new_slots, ceil(value_to_add)

    def undo_last_ins(self) -> "HorizontalConfiguration":
        value_removing = self.cperm[-1]
        if value_removing in self.cperm[:-1]:
            # was a repeated element (more of that element in the cperm)
            new_cperm = self.cperm[:-1]
            new_slots = self.slots + [value_removing]
        else:
            # was not a repeated element (no more of that element in the cperm)
            new_cperm = [
                val if val < value_removing else val - 1 for val in self.cperm[:-1]
            ]
            remove_slots = [
                val
                for val in self.slots
                if val > value_removing + 0.5 or val < value_removing - 0.5
            ]
            if len(new_cperm) == 0:
                return self.__class__(CayleyPermutation(new_cperm), [-0.5])
            new_slots = [
                val if val < value_removing else val - 1 for val in remove_slots
            ] + [value_removing - 0.5]
        return self.__class__(CayleyPermutation(new_cperm), new_slots)

    def letter_of_last_ins(self) -> Letter:
        value_removing = self.cperm[-1]
        if value_removing in self.slots:
            idx2 = 1
        else:
            idx2 = 0
        count = 0
        for slot in self.slots:
            if slot < value_removing - 0.5:
                count += 1
        idx1 = count
        if value_removing - 0.5 in self.slots:
            if value_removing + 0.5 in self.slots:
                return Letter("m", idx1, idx2)
            return Letter("u", idx1, idx2)
        if value_removing + 0.5 in self.slots:
            return Letter("d", idx1, idx2)
        return Letter("f", idx1, idx2)

    def get_word(self) -> "Word":
        """
        Converts a configuration into a word.
        """
        configuration = self
        word: List[Letter] = []
        while configuration.cperm:
            letter = configuration.letter_of_last_ins()
            word = [letter] + word
            configuration = configuration.undo_last_ins()
        return Word(word)

    def cayley_perms(
        self, size: int, basis: Iterable[CayleyPermutation]
    ) -> Iterator[CayleyPermutation]:
        """Returns the next Cayley permutations up to length 'size'
        which avoid the basis from the configuration."""
        if size < len(self.cperm):
            return
        if not self.cperm.avoids(basis):
            return
        if self.is_cayley_perm():
            if self.cperm.avoids(basis):
                yield CayleyPermutation(self.cperm)
        for child in self.children():
            yield from child.cayley_perms(size, basis)

    def all_possible_letters(self) -> List[Letter]:
        letters = []
        for i, val in enumerate(self.slots):
            if isinstance(val, int):
                letters.append(Letter("f", i, 1))
                letters.append(Letter("f", i, 0))
            else:
                letters.append(Letter("f", i, 0))
                letters.append(Letter("u", i, 0))
                letters.append(Letter("m", i, 0))
                letters.append(Letter("d", i, 0))
                letters.append(Letter("f", i, 1))
                letters.append(Letter("u", i, 1))
                letters.append(Letter("m", i, 1))
                letters.append(Letter("d", i, 1))
        return letters

    def children(self) -> List["HorizontalConfiguration"]:
        return [letter.apply(self) for letter in self.all_possible_letters()]

    @classmethod
    def standardise(
        cls, config_cperm: List, config_slots: List
    ) -> "HorizontalConfiguration":
        """
        Standardises a configuration.
        If a slot is a constant slot, then assumed there should be an occurrence
        of the value in the Cayley permutation.
        """
        new_cperm = CayleyPermutation.standardise(config_cperm)
        standardisation_map = dict()
        for idx, val in enumerate(config_cperm):
            standardisation_map[val] = new_cperm[idx]
        new_slots = []
        for slot in config_slots:
            if isinstance(slot, int):
                if slot not in standardisation_map.keys():
                    raise ValueError(
                        "A constant slot must be a repeat of a value already in the Cayley permnutation."
                    )
                new_slots.append(standardisation_map[slot])
            else:
                if slot == -0.5:
                    new_slots.append(-0.5)
                else:
                    new_slots.append(
                        standardisation_map[
                            cls.closest_value_smaller(slot, config_cperm)
                        ]
                        + 0.5
                    )
        return cls(new_cperm, new_slots)

    def candidates_to_delete(self) -> List[int]:
        """Returns indices in the Cayley permutation which are repeated or are
        not directly adjacent to two slots

        Example: HorizontalConfiguration(CayleyPermutation([0, 1, 1, 2, 3]), [0.5, 1.5, 2]).candidates_to_delete()

        """
        candidates = []
        for idx, val in enumerate(self.cperm):
            if self.cperm.cperm.count(val) > 1:
                candidates.append(idx)
                continue
            if (
                idx + 0.5 in self.slots
                and idx - 0.5 in self.slots
                and idx not in self.slots
            ):
                candidates.append(idx)
        return candidates

    def delete_index(self, index):
        """Delete the index from the Cayley permutation part of the configuration."""
        val_deleted = self.cperm[index]
        new_cperm = self.cperm[:index] + self.cperm[index + 1 :]
        if val_deleted in new_cperm:
            new_slots = self.slots
        else:
            new_slots = [val if val < val_deleted else val - 1 for val in self.slots]
        return HorizontalConfiguration(
            CayleyPermutation.standardise(new_cperm), new_slots
        )

    def bound(self, basis: List[CayleyPermutation]) -> int:
        """How far need to check if can remove an index."""
        p = max(map(len, basis))
        k = len(self.slots) + len(self.cperm)
        return p + k - 2

    @classmethod
    def closest_value_smaller(cls, slot: float, cperm: List[int]) -> float:
        """
        Returns the closest value smaller than the given value.
        """
        for val in reversed(sorted(cperm)):
            if val < slot:
                return val
        return -1

    def is_cayley_perm(self) -> bool:
        return not self.slots

    def __len__(self):
        return len(self.cperm) + len(self.slots)

    def __eq__(self, other):
        return self.cperm == other.cperm and self.slots == other.slots

    def __repr__(self):
        return f"HorizontalConfiguration({self.cperm}, {self.slots})"

    def __hash__(self):
        return hash((self.cperm, tuple(self.slots)))

    def __str__(self):
        if len(self.cperm) == 0:
            return "🔹"
        all_rows = []
        if -0.5 in self.slots:
            middle_row = " " + " " * len(self.cperm)
            middle_row += "🔹"
            all_rows.append(middle_row)
        for row_number in range(max(self.cperm) + 1):
            row = " "
            for idx in range(len(self.cperm)):
                if self.cperm[idx] == row_number:
                    row += str(row_number)
                else:
                    row += " "
            if row_number in self.slots:
                row += "🔸"
            else:
                row += " "
            all_rows.append(row)
            if row_number + 0.5 in self.slots:
                middle_row = " " + " " * len(self.cperm)
                middle_row += "🔹"
                all_rows.append(middle_row)
        return "\n".join(reversed(all_rows))


class Word:
    """
    A Word is a list that begins empty and a list of Letters
    are added to it.

    Examples:
    >>> print(Word([Letter("m", 1, 1), Letter("l", 2, 1)]))
    m_(1, 1)l_(2, 1)
    >>> print(Word([Letter("r", 1, 1), Letter("f", 1, 0)]))
    r_(1, 1)f_(1, 0)
    """

    def __init__(self, letters: List[Letter]):
        self.letters = letters

    def cayley_permutation(
        self,
        config: HorizontalConfiguration = HorizontalConfiguration(
            CayleyPermutation([]), [-0.5]
        ),
    ) -> HorizontalConfiguration:
        """
        Applies the letters from a word to a configuration.
        If no configuration is given, it applies the letters to the empty configuration.
        """
        new_config = config
        for lett in self.letters:
            new_config = lett.apply(new_config)
        return new_config

    def max_index(self) -> int:
        """
        Returns maximum index of the letters in a word.

        Examples:
        >>> Word([Letter("m", 1, 1), Letter("l", 2, 1)]).max_index()
        2
        """
        var = 1
        for letter in self.letters:
            if letter.index > var:
                var = letter.index
        return var

    @classmethod
    def words_size_n(cls, av: Av, size: int) -> Iterator["Word"]:
        """
        Prints the words generating all Cayley permutations in Av(B) of 'size'.
        """
        for cperm in av.generate_cperms(size):
            config = HorizontalConfiguration(CayleyPermutation(cperm.cperm), [])
            yield config.get_word()

    @classmethod
    def max_index_in_av(cls, av: Av, size: int) -> int:
        """
        returns the maximum index of a letter in Av(B) for a word of length 'size'.

        Example:
        >>> Word.max_index_in_av(Av([CayleyPermutation([0, 1]), CayleyPermutation([1, 0])]), 3)
        1
        """
        var = 1
        for word in cls.words_size_n(av, size):
            max_index = word.max_index()
            if max_index > var:
                var = max_index
        return var

    def __len__(self):
        return len(self.letters)

    def __str__(self):
        return "".join(str(x) for x in self.letters)
