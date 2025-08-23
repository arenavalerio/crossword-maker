"""Represents a directed coordinate"""

from dataclasses import dataclass
from .coordinate import Coordinate
from .direction import Direction


@dataclass(frozen=True)
class CoordinateWithDirection(Coordinate):
    """
    Represents a coordinate with an associated direction (horizontal or vertical).
    """
    direction: Direction
