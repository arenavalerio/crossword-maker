"""Classes to represents a crossword domain"""

import copy
from .cell import Cell
from .cell_slot import CellSlot
from .coordinate import Coordinate
from .coordinate_with_direction import CoordinateWithDirection
from .crossword_schema import CrosswordSchema
from .direction import Direction

MIN_WORD_LENGTH = 4

class Crossword:
    """
    Represents a crossword puzzle instance, with methods to write words and display the grid.
    """

    def __init__(self, schema: CrosswordSchema):
        """
        Initializes a Crossword instance with a given schema.
        :param schema: The CrosswordSchema object representing the grid layout.
        """
        self.schema = schema
        self.grid = copy.deepcopy(schema.grid)

    def write_word(self, word: str, slot: CellSlot):
        """
        Writes a word into the crossword grid at the specified slot.
        :param word: The word to write.
        :param slot: The CellSlot where the word should be written.
        :raises ValueError: If the word length does not match the slot
          or if writing over a black square.
        """
        if len(word) != slot.length():
            raise ValueError("The word length does not match the surrounding characters length.")
        all_cells = slot.all_cells()
        for i in range(slot.length()):
            grid_cell = all_cells[i]
            value = word[i]
            if grid_cell.value == '#':
                raise ValueError("Cannot write a word over a black square.")
            self.grid[grid_cell.x][grid_cell.y] = value

    def display(self):
        """
        Displays the current state of the crossword grid to the console.
        """
        for row in self.grid:
            for cell in row:
                print(f"[{cell}]", end=' ')
            print()
        print()

    def get_next_available_coordinate(self,
            initial_position: CoordinateWithDirection) -> CoordinateWithDirection | None:
        """
        Finds the next available coordinate in the grid for placing a word, 
        starting from the given position.
        :param initial_position: The starting coordinate with direction.
        :return: The next available CoordinateWithDirection or None if no available slot is found.
        """
        next_coordinate: CoordinateWithDirection = None
        if initial_position is None:
            next_coordinate = CoordinateWithDirection(0, 0, Direction.HORIZONTAL)
        else:
            next_coordinate = self._get_next_coordinate(initial_position)
        if next_coordinate is None:
            return None
        if self.is_available(next_coordinate):
            return next_coordinate
        return self.get_next_available_coordinate(next_coordinate)

    def is_available(self, coordinate: CoordinateWithDirection) -> bool:
        """
        Checks if a given coordinate is available for placing a word.
        :param coordinate: The coordinate with direction to check.
        :return: True if the slot is available, False otherwise.
        """
        slot = self.get_slot(coordinate)
        return slot.is_first_cell() and not slot.is_written() and slot.length() >= MIN_WORD_LENGTH

    def _get_next_coordinate(self, coordinate: CoordinateWithDirection) -> Coordinate | None:
        """
        Gets the next coordinate in the grid, switching direction if needed.
        :param coordinate: The current coordinate with direction.
        :return: The next CoordinateWithDirection or None if at the end of the grid.
        """
        if coordinate.direction == Direction.HORIZONTAL:
            return CoordinateWithDirection(coordinate.x, coordinate.y, Direction.VERTICAL)
        x = coordinate.x
        y = coordinate.y + 1
        if y >= self.schema.y_length:
            y = 0
            x += 1
        if x >= self.schema.x_length:
            return None
        return CoordinateWithDirection(x, y, Direction.HORIZONTAL)

    def get_slot(self, coordinate: CoordinateWithDirection) -> CellSlot:
        """
        Returns the CellSlot (sequence of cells) for a given coordinate and direction.
        :param coordinate: The coordinate with direction for which to get the slot.
        :return: The CellSlot object representing the word slot at the given position.
        """
        main_cell = Cell(coordinate.x, coordinate.y, self.grid[coordinate.x][coordinate.y])
        previous_cells = []
        following_cells = []
        if main_cell.value == '#':
            return CellSlot(main_cell, previous_cells, following_cells, coordinate.direction)
        if coordinate.direction == Direction.HORIZONTAL:
            current_y = coordinate.y - 1
            while current_y >= 0 and self.grid[coordinate.x][current_y] != '#':
                previous_cells.insert(0, Cell(coordinate.x, current_y,
                                self.grid[coordinate.x][current_y]))
                current_y -= 1
            current_y = coordinate.y + 1
            while current_y < self.schema.y_length and self.grid[coordinate.x][current_y] != '#':
                following_cells.append(Cell(coordinate.x, current_y,
                                self.grid[coordinate.x][current_y]))
                current_y += 1
        elif coordinate.direction == Direction.VERTICAL:
            current_x = coordinate.x - 1
            while current_x >= 0 and self.grid[current_x][coordinate.y] != '#':
                previous_cells.insert(0, Cell(current_x, coordinate.y,
                                self.grid[current_x][coordinate.y]))
                current_x -= 1
            current_x = coordinate.x + 1
            while current_x < self.schema.x_length and self.grid[current_x][coordinate.y] != '#':
                following_cells.append(Cell(current_x, coordinate.y,
                                self.grid[current_x][coordinate.y]))
                current_x += 1
        return CellSlot(main_cell, previous_cells, following_cells,
                        coordinate.direction)
