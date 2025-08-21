from enum import Enum


class Direction(Enum):
    HORIZONTAL = 1,
    VERTICAL = 2

    @staticmethod
    def opposite(direction):
        if direction == Direction.HORIZONTAL:
            return Direction.VERTICAL
        elif direction == Direction.VERTICAL:
            return Direction.HORIZONTAL
        else:
            raise ValueError("Invalid direction")