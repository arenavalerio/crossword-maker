"""A class to store and retrieve words"""

import random
import re

from words.file_reader import read_words_from_file

# pylint: disable=too-few-public-methods
class WordsRegexSet:
    """
    Manages the word list for the crossword, with regex and length-based lookup.
    """

    def __init__(self, file_path: str, size: int, randomize: bool):
        """
        Initialize the Words object.
        :param file_path: Path to the word list file.
        :param size: Max number of words to return per query.
        :param randomize: Whether to randomize the word list.
        """
        self.size = size
        self.randomize = randomize
        self._read_words(file_path)

    def get_words_with_regex(self, regex: str, length: int) -> list[str]:
        """
        Returns a list of words matching the regex and length.
        :param regex: Regex pattern to match.
        :param length: Desired word length.
        :return: List of matching words.
        """
        all_words = self.words_by_length[length]
        pattern = re.compile(regex)
        result = []
        result_count = 0
        for word in all_words:
            if pattern.fullmatch(word):
                result.append(word)
                result_count += 1
                if result_count >= self.size:
                    break
        return result


    def _read_words(self, file_path):
        """
        Reads words from the file and organizes them by length.
        :param file_path: Path to the word list file.
        """
        self.words_by_length = {}
        for word in read_words_from_file(file_path):
            word_length = len(word)
            if word_length not in self.words_by_length:
                self.words_by_length[word_length] = []
            self.words_by_length[word_length].append(word)
        if self.randomize:
            for _, word_list in self.words_by_length.items():
                random.shuffle(word_list)
