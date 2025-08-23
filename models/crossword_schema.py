"""Represents the schema of a crossword"""

from dataclasses import dataclass


@dataclass()
class CrosswordSchema:
    """
    Represents the schema (layout) of the crossword grid.
    """
    grid: list[list[str]]
    def __post_init__(self):
        self.x_length = len(self.grid)
        self.y_length = len(self.grid[0])
