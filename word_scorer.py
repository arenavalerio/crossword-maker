"""A scorer of words within a crossword"""

import logging
from models import Crossword, CellSlot, Direction, Cell, CoordinateWithDirection, MIN_WORD_LENGTH
from words import Words

# pylint: disable=too-few-public-methods
class WordScorer:
    """
    Scores candidate words for a crossword slot based on fitting constraints.
    """

    def __init__(self, crossword: Crossword, slot: CellSlot, words: Words):
        """
        Initialize the WordScorer.
        :param crossword: The Crossword object.
        :param slot: The CellSlot to score for.
        :param words: The Words object for word lookup.
        """
        self.crossword = crossword
        self.slot = slot
        self.words = words
        self.scorecard = {}

    def score_word(self, word: str) -> int:
        """
        Scores a word for the current slot.
        :param word: The word to score.
        :return: Integer score (higher is better, -1 if not fitting).
        """
        all_cells = self.slot.all_cells()
        length = self.slot.length()
        if length != len(word):
            raise ValueError("Word length does not match slot length.")
        score = 0
        for i in range(length):
            cell = all_cells[i]
            value_char = word[i]
            fitting_count = self._get_fitting_words_count_for_char(
                self.crossword, cell, Direction.opposite(self.slot.direction), value_char)
            if fitting_count < 0:
                return -1
            score += fitting_count
        return score

    def _get_fitting_words_count_for_char(self, crossword: Crossword,
                                          cell: Cell, direction: Direction, value: str) -> int:
        """
        Returns the number of fitting words for a cell and direction with a given value.
        :param crossword: The Crossword object.
        :param cell: The Cell to check.
        :param direction: The direction to check.
        :param value: The value to fit.
        :return: Number of fitting words, or -1 if none.
        """
        slot = crossword.get_slot(CoordinateWithDirection(cell.x, cell.y, direction))
        if slot.is_written():
            logging.debug("Skipping (%d, %d) as it is already written.", cell.x, cell.y)
            return 0
        if slot.length() < MIN_WORD_LENGTH:
            logging.debug("Skipping (%d, %d) due to insufficient length for word.", cell.x, cell.y)
            return 0
        regex = slot.get_tentative_regex(value)
        words_list = self.words.get_words_with_regex(regex, slot.length())
        if len(words_list) == 0:
            logging.debug("No words found for regex '%s' of length %d.", regex, slot.length)
            return -1
        return len(words_list)
