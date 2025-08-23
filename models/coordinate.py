"""Represents a coordinate in a crossword"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    """
    Represents a coordinate (x, y) in the crossword grid.
    """
    x: int
    y: int
