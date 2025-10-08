"""This module contains the Letter class, VerticalConfiguration class and the Word class."""

from typing import Iterator, List, Dict, Union
from cayley_permutations import Av, CayleyPermutation


class Letter:
    """
    A letter has three values where the first element is
    one of {m, l, r, f}, the second is the index of the slot,
    and the last dictates if the value should increase or not.

    Examples:
    >>> print(Letter("m", 1, 0))
    m_(1, 0)
    >>> print(Letter("l", 2, 1))
    l_(2, 1)
    """

    def __init__(self, letter: str, index: int, repeat: int):
        self.letter = letter
        self.index = index
        self.repeat = repeat
        if self.letter not in ("m", "l", "r", "f"):
            raise ValueError("Letter must be one of m, l, r, f.")

    def apply(self, config: "VerticalConfiguration") -> "VerticalConfiguration":
        """Applies a letter to a VerticalConfiguration.

        Examples:
        >>> print(Letter("l", 1, 0).apply(VerticalConfiguration([0, 1, "🔹", 2])))
        012🔹2
        >>> print(Letter("f", 1, 1).apply(VerticalConfiguration([0, 1, "🔹", 2])))
        0132
        """
        if self.letter == "m":
            return self.apply_m(config, self.index, self.repeat)
        if self.letter == "l":
            return self.apply_l(config, self.index, self.repeat)
        if self.letter == "r":
            return self.apply_r(config, self.index, self.repeat)
        if self.letter == "f":
            return self.apply_f(config, self.index, self.repeat)
        raise ValueError

    def apply_m(
        self, config: "VerticalConfiguration", index: int, repeat: int
    ) -> "VerticalConfiguration":
        """Change "🔹" to: "🔹", max_value + repeat, "🔹"."""
        return config.apply_m(index, repeat)

    def apply_l(
        self, config: "VerticalConfiguration", index: int, repeat: int
    ) -> "VerticalConfiguration":
        """Change "🔹" to: max_value + repeat, "🔹"."""
        return config.apply_l(index, repeat)

    def apply_r(
        self, config: "VerticalConfiguration", index: int, repeat: int
    ) -> "VerticalConfiguration":
        """Change "🔹" to: "🔹", max_value + repeat."""
        return config.apply_r(index, repeat)

    def apply_f(
        self, config: "VerticalConfiguration", index: int, repeat: int
    ) -> "VerticalConfiguration":
        """Change "🔹" to: max_value + repeat."""
        return config.apply_f(index, repeat)

    def __str__(self):
        return f"{self.letter}_{self.index, self.repeat}"

    @classmethod
    def from_string(cls, letter: str) -> "Letter":
        """Returns a Letter from a string.

        Examples:
        >>> print(Letter.from_string("m_1_0"))
        m_(1, 0)
        >>> print(Letter.from_string("l_2_1"))
        l_(2, 1)
        """
        letter, index, repeat = letter.split("_")
        return cls(letter, int(index), int(repeat))


class VerticalConfiguration:
    """
    A VerticalConfiguration is a list where the values are integers or the
    slot represented by "🔹".

    Examples:
    >>> print(VerticalConfiguration([0, 1, "🔹", 2]))
    01🔹2
    """

    # pylint: disable=too-many-public-methods

    def __init__(self, config: List):
        self.config = config

        for elm in self.config:
            if not isinstance(elm, int) and elm != "🔹":
                raise ValueError(
                    "VerticalConfiguration must be a list of integers or '🔹'."
                )

        if len(self.config) > 1:
            values = [x for x in self.config if x != "🔹"]
            for val in range(max(values)):
                if val not in values:
                    raise ValueError(
                        "Values in VerticalConfiguration must be consecutive and zero based."
                    )

    def apply_m(self, index: int, repeat: int) -> "VerticalConfiguration":
        """
        Change "🔹" to: "🔹", max_value + repeat, "🔹".

        Example:
        >>> print(VerticalConfiguration([0, 1, "🔹", 2]).apply_m(1, 1))
        01🔹3🔹2
        """
        idx = self.find_slot_index(index)
        max_value = self.max_value() + repeat
        return self.__class__(
            self.config[:idx] + ["🔹", max_value, "🔹"] + self.config[idx + 1 :]
        )

    def apply_l(self, index: int, repeat: int) -> "VerticalConfiguration":
        """
        Change "🔹" to: max_value + repeat, "🔹".

        Example:
        >>> print(VerticalConfiguration([0, 1, "🔹", 2]).apply_l(1, 1))
        013🔹2
        """
        idx = self.find_slot_index(index)
        max_value = self.max_value() + repeat
        return self.__class__(
            self.config[:idx] + [max_value, "🔹"] + self.config[idx + 1 :]
        )

    def apply_r(self, index: int, repeat: int) -> "VerticalConfiguration":
        """
        Change "🔹" to: "🔹", max_value + repeat.

        Example:
        >>> print(VerticalConfiguration([0, 1, "🔹", 2]).apply_r(1, 1))
        01🔹32
        """
        idx = self.find_slot_index(index)
        max_value = self.max_value() + repeat
        return self.__class__(
            self.config[:idx] + ["🔹", max_value] + self.config[idx + 1 :]
        )

    def apply_f(self, index: int, repeat: int) -> "VerticalConfiguration":
        """
        Change "🔹" to: max_value + repeat.

        Example:
        >>> print(VerticalConfiguration([0, 1, "🔹", 2]).apply_f(1, 1))
        0132
        """
        idx = self.find_slot_index(index)
        max_value = self.max_value() + repeat
        return self.__class__(self.config[:idx] + [max_value] + self.config[idx + 1 :])

    def find_slot_index(self, index: int) -> int:
        """
        Returns the index in the VerticalConfiguration as a list of
        the nth slot where n is the input 'index'.

        Examples:
        >>> print(VerticalConfiguration([0, "🔹", 1, "🔹", 2]).find_slot_index(1))
        1
        >>> print(VerticalConfiguration([0, "🔹", 1, "🔹", 2]).find_slot_index(2))
        3
        >>> print(VerticalConfiguration([0, "🔹", 1]).find_slot_index(1))
        1
        """
        count = 0
        for idx, val in enumerate(self.config):
            if val == "🔹":
                count += 1
            if count == index:
                return idx
        raise ValueError

    def max_value(self) -> int:
        """Returns the largest value in the VerticalConfiguration, ignoring slots.
        If the VerticalConfiguration is a single slot, returns 0

        Examples:
        >>> VerticalConfiguration([0, 1, "🔹", 2]).max_value()
        2
        """
        if self.config == ["🔹"]:
            return -1
        return max(elm for elm in self.config if elm != "🔹")

    def has_increased(self) -> bool:
        """Returns True if the last letter applied increased the maximum value.
        (True if there is more than one of the maximum value in the VerticalConfiguration)

        Examples:
        >>> print(VerticalConfiguration([0, 1, "🔹", 2]).has_increased())
        True
        >>> print(VerticalConfiguration([0, 2, 1, "🔹", 2]).has_increased())
        False
        """
        count = 0
        for elm in self.config:
            if elm != "🔹":
                if elm == self.max_value():
                    count += 1
        if count > 1:
            return False
        if count == 1:
            return True
        raise ValueError

    def index_of_max(self) -> int:
        """Returns the index of the rightmost maximum value.

        Example:
        >>> VerticalConfiguration([0, 1, 1, "🔹", 2]).index_of_max()
        4
        """
        if VerticalConfiguration(["🔹"]) == self:
            return 1
        max_val = self.max_value()
        for idx, val in reversed(list(enumerate(self.config))):
            if val == max_val:
                return idx
        return 0

    def letter_of_last_insertion(self) -> Letter:
        """Returns the letter of the last insertion.

        Example:
        >>> print(VerticalConfiguration([0, 2, 1, "🔹", 2]).letter_of_last_insertion())
        f_(1, 0)
        """
        index = self.index_of_max()
        if index != 0 and self.config[index - 1] == "🔹":
            if index != len(self.config) - 1 and self.config[index + 1] == "🔹":
                letter = "m"
            else:
                letter = "r"
            slots = self.counting_slots(index)
        elif index != len(self.config) - 1 and self.config[index + 1] == "🔹":
            letter = "l"
            slots = self.counting_slots(index) + 1
        else:
            letter = "f"
            slots = self.counting_slots(index) + 1
        new_max = 1 if self.has_increased() else 0
        return Letter(letter, slots, new_max)

    def counting_slots(self, index: int) -> int:
        """Counts and returns the number of slots to the left of index.

        Examples:
        >>> VerticalConfiguration([0, "🔹", 2, 1, "🔹", 2]).counting_slots(2)
        1
        >>> VerticalConfiguration([0, "🔹", 2, 1, "🔹", 2]).counting_slots(5)
        2
        """
        count = 0
        for idx, val in enumerate(self.config):
            if idx == index:
                break
            if val == "🔹":
                count += 1
        return count

    def undoing_last_ins(self, letter: Letter) -> "VerticalConfiguration":
        """Returns the VerticalConfiguration before the last letter was applied.

        Example:
        >>> print(VerticalConfiguration([0, 2, 1, "🔹", 2]).undoing_last_ins(Letter("f", 1, 0)))
        0🔹1🔹2
        """
        index = self.index_of_max()
        if letter.letter == "m":
            return self.__class__(self.config[:index] + self.config[index + 2 :])
        if letter.letter in ("r", "l"):
            return self.__class__(self.config[:index] + self.config[index + 1 :])
        if letter.letter == "f":
            return self.__class__(
                self.config[:index] + ["🔹"] + self.config[index + 1 :]
            )
        raise ValueError

    def max_slots_of_evolution(self) -> int:
        """Return the maximum number of slots in a configuration in the
        evolution."""
        slots = 0
        curr_config = self
        while len(curr_config) > 1:
            letter = curr_config.letter_of_last_insertion()
            config = curr_config.undoing_last_ins(letter)
            slots = max(slots, config.number_of_slots())
            curr_config = config
            if len(curr_config) == 1:
                break
        return slots

    def get_word(self) -> "Word":
        """
        Converts a VerticalConfiguration into a word.

        Example:
        >>> print(VerticalConfiguration([0, 2, 1, "🔹", 2]).get_word())
        l_(1, 1)m_(1, 1)r_(2, 1)f_(1, 0)
        """
        v_config = self
        word: List[Letter] = []
        while v_config != self.__class__(["🔹"]):
            letter = v_config.letter_of_last_insertion()
            word = [letter] + word
            v_config = v_config.undoing_last_ins(letter)
        return Word(word)

    @classmethod
    def standardise(cls, config: List) -> "VerticalConfiguration":
        """Standardises a VerticalConfiguration by replacing the numbers with the
        smallest possible numbers that give the same relative sequence.

        Example:
        >>> print(VerticalConfiguration.standardise([2, "🔹", 3]))
        0🔹1
        """
        key = sorted(set(x for x in config if x != "🔹"))
        stand: Dict[Union[str, int], Union[str, int]] = {}
        stand["🔹"] = "🔹"
        for i, v in enumerate(key):
            stand[v] = i
        return cls([stand[pat] for pat in config])

    def delete_index(self, index: int) -> "VerticalConfiguration":
        """Removing the element at index 'index' from the VerticalConfiguration and standardise

        Examples:
        >>> print(VerticalConfiguration([0, 1, "🔹", 2]).delete_index(1))
        0🔹1
        >>> print(VerticalConfiguration([0, 1, "🔹", 2]).delete_index(3))
        01🔹
        """
        return self.__class__.standardise(
            self.config[:index] + self.config[index + 1 :]
        )

    def candidates_to_delete(self) -> List[int]:
        """Returns indices that aren't a slot or next to two slots.

        Example:
        >>> VerticalConfiguration([0, 1, "🔹", 2,"🔹", 1]).candidates_to_delete()
        [0, 1, 5]
        """
        candidates = []
        max_index = self.index_of_max()
        for idx, val in enumerate(self.config):
            if idx == max_index:
                continue
            if val != "🔹":
                if idx in (0, len(self.config) - 1):
                    candidates.append(idx)
                elif self.config[idx - 1] != "🔹" or self.config[idx + 1] != "🔹":
                    candidates.append(idx)
        return candidates

    def can_be_deleted(self, idx: int, basis: List[CayleyPermutation]) -> bool:
        """Returns True if the VerticalConfiguration can be deleted
        at index 'idx' and still avoid the basis."""
        return all(
            cperm.avoids_same_after_deleting(
                basis, self.cperm_idx_from_config_idx(cperm, idx)
            )
            for cperm in self.cayley_perms(self.bound(basis), [])
        )

    def deleteable_indices(self, basis: List[CayleyPermutation]) -> List[int]:
        """Returns list of indices from candidates to delete that the
        VerticalConfiguration still avoids the basis after being deleted."""
        # pylint: disable=duplicate-code
        indices = self.candidates_to_delete()
        to_remove = []
        for idx in indices:
            if self.can_be_deleted(idx, basis):
                to_remove.append(idx)
        return to_remove

    def bound(self, basis: List[CayleyPermutation]) -> int:
        """How far need to check if can remove an index."""
        p = max(map(len, basis))
        k = len(self.config)
        return p + k - 2

    def cperm_idx_from_config_idx(
        self, cperm: CayleyPermutation, config_idx: int
    ) -> int:
        """Returns the index in a Cayley permutation given the
        index of the VerticalConfiguration it was obtained from

        Examples:
        >>> VerticalConfiguration([0, "🔹", 1, 2]).cperm_idx_from_config_idx(
        ...    CayleyPermutation([0, 3, 2, 1, 2]), 2)
        3
        >>> VerticalConfiguration([0, "🔹", 1, 2]).cperm_idx_from_config_idx(
        ...    CayleyPermutation([0, 3, 2, 1, 2]), 3)
        4
        """
        number_idx = 0
        for idx, val in enumerate(self.config):
            if idx == config_idx:
                break
            if val != "🔹":
                number_idx += 1
        first_k = cperm.first_k_entries(self.number_of_numbers())
        cperm_idx = first_k[number_idx]
        return cperm_idx

    def cayley_perms(
        self, size: int, basis: List[CayleyPermutation]
    ) -> Iterator[CayleyPermutation]:
        """
        Returns the next Cayley permutations up to length 'size'
        which avoid the basis from the VerticalConfiguration.

        Example:
        >>> c = VerticalConfiguration([0, 1, "🔹"])
        >>> for config in c.cayley_perms(4, [CayleyPermutation([1, 0])]):
        ...     print(config)
        012
        0123
        0122
        """
        # pylint: disable=duplicate-code
        if size < len(self.config):
            return
        if not self.avoids_basis(basis):
            return
        if self.is_cayley_perm():
            if self.avoids_basis(basis):
                yield CayleyPermutation(self.config)
        for child in self.children():
            yield from child.cayley_perms(size, basis)

    def count(self, size: int, basis: List[CayleyPermutation]):
        """
        Prints the number of Cayley permutations of each length
        up to length 'size' which avoid the basis from the VerticalConfiguration.

        Example:
        >>> VerticalConfiguration([0, 1, "🔹"]).count(4, [CayleyPermutation([1, 0])])
        0,0,0,1,2,
        """
        counts: Dict[int, List[CayleyPermutation]] = {}
        for i in range(size + 1):
            counts[i] = []
        for perm in self.cayley_perms(size, basis):
            counts[len(perm)].append(perm)
        for i in range(size + 1):
            print(len(counts[i]), end=",", flush=True)

    def number_of_slots(self) -> int:
        """Returns the number of slots in the VerticalConfiguration.

        Example:
        >>> VerticalConfiguration([0, "🔹", 1, "🔹", 2]).number_of_slots()
        2
        """
        count = 0
        for val in self.config:
            if val == "🔹":
                count += 1
        return count

    def number_of_numbers(self) -> int:
        """Returns the number of numbers in the VerticalConfiguration
        (total length minus number of slots)."""
        return len(self.config) - self.number_of_slots()

    def all_possible_letters(self) -> List[Letter]:
        """Returns a list of all possible letters that can be
        inserted into the VerticalConfiguration.

        Examples:
        >>> for letter in VerticalConfiguration([0, 1, "🔹", 2]).all_possible_letters():
        ...     print(letter)
        f_(1, 1)
        l_(1, 1)
        m_(1, 1)
        r_(1, 1)

        >>> for letter in VerticalConfiguration(["🔹"]).all_possible_letters():
        ...     print(letter)
        f_(1, 1)
        l_(1, 1)
        m_(1, 1)
        r_(1, 1)
        """
        letters = []
        idx = self.index_of_max()
        left = self.counting_slots(idx)
        right = self.number_of_slots() - left

        for i in range(left + 1, right + left + 1):
            letters.append(Letter("f", i, 0))
            letters.append(Letter("l", i, 0))
            letters.append(Letter("m", i, 0))
            letters.append(Letter("r", i, 0))

        letters.extend(self._new_max_letters(left, right))
        return letters

    def _new_max_letters(self, left: int, right: int) -> List[Letter]:
        """Returns a list of letters that can be inserted into the
        VerticalConfiguration with a new maximum value."""
        for i in range(1, right + left + 1):
            return [
                Letter("f", i, 1),
                Letter("l", i, 1),
                Letter("m", i, 1),
                Letter("r", i, 1),
            ]
        return []

    def children(self) -> List["VerticalConfiguration"]:
        """Returns a list of all VerticalConfigurations that can be obtained
        by applying one letter to the starting VerticalConfiguration.

        Examples:
        >>> for config in VerticalConfiguration([0, 1, "🔹", 2]).children():
        ...     print(config)
        0122
        012🔹2
        01🔹2🔹2
        01🔹22
        0132
        013🔹2
        01🔹3🔹2
        01🔹32
        >>> for config in VerticalConfiguration(["🔹"]).children():
        ...     print(config)
        0
        0🔹
        🔹0🔹
        🔹0
        """
        children = []
        letters = self.all_possible_letters()
        for let in letters:
            config_new = let.apply(self)
            children.append(config_new)
        return children

    def avoids_basis(self, basis: List[CayleyPermutation]) -> bool:
        """Returns True if the values in the VerticalConfiguration avoids the basis.

        Examples:
        >>> VerticalConfiguration([0, 1, 2, "🔹", 2]).avoids_basis([CayleyPermutation([1, 0])])
        True
        >>> VerticalConfiguration([0, 1, 3, "🔹", 2]).avoids_basis([CayleyPermutation([1, 0])])
        False
        """
        new_config = []
        for val in self.config:
            if val != "🔹":
                new_config.append(val)
        child_new = CayleyPermutation(new_config)
        if not child_new.contains(basis):
            return True
        return False

    def is_cayley_perm(self) -> bool:
        """Returns True if the VerticalConfiguration is a Cayley permutation (has no slots)."""
        for val in self.config:
            if val == "🔹":
                return False
        return True

    def __str__(self):
        return "".join(
            (str(x) if not isinstance(x, int) else str(x) if x < 10 else f"({x})")
            for x in self.config
        )

    def __len__(self):
        return len(self.config)

    def __hash__(self):
        return hash(tuple(self.config))

    def __eq__(self, other):
        return self.config == other.config


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

    def __init__(self, letters: List):
        self.letters = letters

    def cayley_permutation(
        self, config: VerticalConfiguration = VerticalConfiguration(["🔹"])
    ) -> VerticalConfiguration:
        """
        Applies the letters from a word to a VerticalConfiguration.
        If no VerticalConfiguration is given, it applies the letters
        to the empty VerticalConfiguration.

        Examples:
        >>> print(Word([Letter("m", 1, 1), Letter("l", 2, 1)]).permutation())
        🔹01🔹
        >>> print(Word([Letter("r", 1, 1), Letter("f", 1, 0)]).permutation())
        00
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
            var = max(var, letter.index)
        return var

    @classmethod
    def words_size_n(cls, av: Av, size: int) -> Iterator["Word"]:
        """
        Prints the words generating all Cayley permutations in Av(B) of 'size'.
        """
        for cperm in av.generate_cperms(size):
            config = VerticalConfiguration(list(cperm))
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
            var = max(var, word.max_index())
        return var

    def __len__(self):
        return len(self.letters)

    def __str__(self):
        return "".join(str(x) for x in self.letters)
