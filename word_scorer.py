from crossword import Crossword, CellSlot, Direction, Cell, CoordinateWithDirection
from words import Words
import logging


class WordScorer:

    failing_regexes = []

    def __init__(self, crossword: Crossword, slot: CellSlot, words: Words):
        self.crossword = crossword
        self.slot = slot
        self.words = words
        self.scorecard = {}

    def score_word(self, word: str) -> int:
        all_cells = self.slot.all_cells()
        length = self.slot.length()
        score = 0
        for i in range(length):
            cell = all_cells[i]
            value_char= word[i]
            fitting_count = self._get_fitting_words_count_for_char(self.crossword, cell, Direction.opposite(self.slot.direction), value_char)
            if fitting_count < 0:
                return -1
            score += fitting_count
        return score
    
    def _get_fitting_words_count_for_char(self, crossword: Crossword, cell: Cell, direction: Direction, value: str) -> int:
        slot = crossword.get_slot(CoordinateWithDirection(cell.x, cell.y, direction))
        if slot.is_written():
            logging.debug(f"Skipping ({cell.x}, {cell.y}) as it is already written.")
            return 0
        if slot.length() < 2:
            logging.debug(f"Skipping ({cell.x}, {cell.y}) due to insufficient length for word.")
            return 0
        regex = slot.get_tentative_regex(value)
        words_list = self.words.get_words_with_regex(regex, slot.length())
        if len(words_list) == 0:
            if regex not in self.failing_regexes:
                logging.debug(f"No words found for regex '{regex}' of length {slot.length()}.")
                self.failing_regexes.append(regex)
            logging.debug(f"No words found for regex '{regex}' of length {slot.length()}.")
            return -1
        return len(words_list)
        