from enum import Enum


class Direction(Enum):
    """
    Enum for word direction in the crossword (horizontal or vertical).
    """
    HORIZONTAL = 1,
    VERTICAL = 2

    @staticmethod
    def opposite(direction):
        """
        Returns the opposite direction (horizontal <-> vertical).
        :param direction: Direction to invert.
        :return: Opposite Direction.
        """
        if direction == Direction.HORIZONTAL:
            return Direction.VERTICAL
        elif direction == Direction.VERTICAL:
            return Direction.HORIZONTAL
        else:
            raise ValueError("Invalid direction")