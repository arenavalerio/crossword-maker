from direction import Direction
from dataclasses import dataclass
import copy

MIN_WORD_LENGTH = 4

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

@dataclass(frozen=True)
class CoordinateWithDirection(Coordinate):
    direction: Direction

@dataclass(frozen=True)
class Cell(Coordinate):
    value: str    
    def get_regex_part(self) -> str:
        return self.value if self.value != ' ' else '.'

class CellSlot:
    def __init__(self, main_char: Cell, previous_chars: list[Cell], next_chars: list[Cell], direction: Direction):
        self.main_char = main_char
        self.previous_chars = previous_chars
        self.next_chars = next_chars
        self.direction = direction

    def is_written(self) -> bool:
        for char in self.all_cells():
            if char.value == ' ':
                return False
        return True
    
    def length(self):
        if self.main_char.value == '#':
            return 0
        return len(self.previous_chars) + 1 + len(self.next_chars)
    
    def all_cells(self) -> list[Cell]:
        return self.previous_chars + [self.main_char] + self.next_chars
    
    def first_cell(self) -> Cell:
        return self.previous_chars[0] if len(self.previous_chars) > 0 else self.main_char
    
    def is_first_cell(self) -> bool:
        return len(self.previous_chars) == 0
    
    def get_regex(self) -> str:
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
        if main_value == '#':
            raise ValueError("Cannot get regex for a black square.")
        regex_parts = []
        for char in self.previous_chars:
            regex_parts.append(char.get_regex_part())
        regex_parts.append(main_value if main_value != ' ' else '.')
        for char in self.next_chars:
            regex_parts.append(char.get_regex_part())
        return ''.join(regex_parts)

    def _get_regex_part(self, x: int, y: int) -> str:
        char = self.grid[y][x]
        return char if char != ' ' else '.'
    
class CrosswordSchema:
    def __init__(self, grid: list[list[str]]):
        self.x_length = len(grid)
        self.y_length = len(grid[0])
        self.grid = grid

class Crossword:
    
    def __init__(self, schema: CrosswordSchema):
        self.schema = schema
        self.grid = copy.deepcopy(schema.grid)

    def write_word(self, word: str, slot: CellSlot):
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
        for row in self.grid:
            for cell in row:
                print(f"[{cell}]", end=' ')
            print()
        print()

    def get_next_available_coordinate(self, initial_position: CoordinateWithDirection) -> CoordinateWithDirection | None:
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
        slot = self.get_slot(coordinate)
        return slot.is_first_cell() and not slot.is_written() and slot.length() >= MIN_WORD_LENGTH

    def _get_next_coordinate(self, coordinate: CoordinateWithDirection) -> Coordinate | None:
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