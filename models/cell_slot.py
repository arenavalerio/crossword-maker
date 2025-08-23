"""Represents a slot in the crossword (a sequence of cells for a word)."""

from .cell import Cell
from .direction import Direction


class CellSlot:
    """
    Represents a slot in the crossword (a sequence of cells for a word).
    """

    def __init__(self, main_char: Cell, previous_chars: list[Cell],
                 next_chars: list[Cell], direction: Direction):
        self.main_char = main_char
        self.previous_chars = previous_chars
        self.next_chars = next_chars
        self.direction = direction

    def is_written(self) -> bool:
        """
        Checks if all cells in the slot are filled (not blank).
        """
        for char in self.all_cells():
            if char.value == ' ':
                return False
        return True

    def length(self):
        """
        Returns the length of the slot (number of cells).
        """
        if self.main_char.value == '#':
            return 0
        return len(self.previous_chars) + 1 + len(self.next_chars)

    def all_cells(self) -> list[Cell]:
        """
        Returns a list of all cells in the slot.
        """
        return self.previous_chars + [self.main_char] + self.next_chars

    def first_cell(self) -> Cell:
        """
        Returns the first cell in the slot.
        """
        return self.previous_chars[0] if len(self.previous_chars) > 0 else self.main_char

    def is_first_cell(self) -> bool:
        """
        Checks if this is the first cell in the slot.
        """
        return len(self.previous_chars) == 0

    def get_regex(self) -> str:
        """
        Returns a regex string representing the current state of the slot.
        """
        if self.main_char.value == '#':
            raise ValueError("Cannot get regex for a black square.")
        regex_parts = []
        for char in self.previous_chars:
            regex_parts.append(char.get_regex_part())
        regex_parts.append(self.main_char.get_regex_part())
        for char in self.next_chars:
            regex_parts.append(char.get_regex_part())
        return ''.join(regex_parts)

    def get_tentative_regex(self, main_value: str) -> str:
        """
        Returns a regex string for the slot, tentatively replacing the main cell's value.
        :param main_value: The value to tentatively use for the main cell.
        """
        if main_value == '#':
            raise ValueError("Cannot get regex for a black square.")
        regex_parts = []
        for char in self.previous_chars:
            regex_parts.append(char.get_regex_part())
        regex_parts.append(main_value if main_value != ' ' else '.')
        for char in self.next_chars:
            regex_parts.append(char.get_regex_part())
        return ''.join(regex_parts)
