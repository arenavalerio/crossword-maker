"""Represents a crossword cell"""

from dataclasses import dataclass
from .coordinate import Coordinate

@dataclass(frozen=True)
class Cell(Coordinate):
    """
    Represents a cell in the crossword grid, with a value (letter or blank).
    """
    value: str
    def get_regex_part(self) -> str:
        """
        Returns the regex part for this cell (the value or a wildcard).
        """
        return self.value if self.value != ' ' else '.'
