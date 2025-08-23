"""Represents a word in a crossword, with a score"""

from dataclasses import dataclass
from .coordinate_with_direction import CoordinateWithDirection

@dataclass(frozen=True)
class WrittenWord:
    """
    Represents a word written in the crossword, with its coordinate and score.
    """
    word: str
    coordinate: CoordinateWithDirection
    score: int
