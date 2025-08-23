from direction import Direction
from dataclasses import dataclass
import copy

MIN_WORD_LENGTH = 4

@dataclass(frozen=True)
class Coordinate:
    """
    Represents a coordinate (x, y) in the crossword grid.
    """
    x: int
    y: int

@dataclass(frozen=True)
class CoordinateWithDirection(Coordinate):
    """
    Represents a coordinate with an associated direction (horizontal or vertical).
    """
    direction: Direction

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

class CellSlot:
    """
    Represents a slot in the crossword (a sequence of cells for a word).
    """
    def __init__(self, main_char: Cell, previous_chars: list[Cell], next_chars: list[Cell], direction: Direction):
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
    
class CrosswordSchema:
    """
    Represents the schema (layout) of the crossword grid.
    """
    def __init__(self, grid: list[list[str]]):
        self.x_length = len(grid)
        self.y_length = len(grid[0])
        self.grid = grid

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
        :raises ValueError: If the word length does not match the slot or if writing over a black square.
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

    def get_next_available_coordinate(self, initial_position: CoordinateWithDirection) -> CoordinateWithDirection | None:
        """
        Finds the next available coordinate in the grid for placing a word, starting from the given position.
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
                previous_cells.insert(0, Cell(coordinate.x, current_y, self.grid[coordinate.x][current_y]))
                current_y -= 1
            current_y = coordinate.y + 1
            while current_y < self.schema.y_length and self.grid[coordinate.x][current_y] != '#':
                following_cells.append(Cell(coordinate.x, current_y, self.grid[coordinate.x][current_y]))
                current_y += 1
        elif coordinate.direction == Direction.VERTICAL:
            current_x = coordinate.x - 1
            while current_x >= 0 and self.grid[current_x][coordinate.y] != '#':
                previous_cells.insert(0, Cell(current_x, coordinate.y, self.grid[current_x][coordinate.y]))
                current_x -= 1
            current_x = coordinate.x + 1
            while current_x < self.schema.x_length and self.grid[current_x][coordinate.y] != '#':
                following_cells.append(Cell(current_x, coordinate.y, self.grid[current_x][coordinate.y]))
                current_x += 1
        return CellSlot(main_cell, previous_cells, following_cells, coordinate.direction)