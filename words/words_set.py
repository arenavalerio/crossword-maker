"""A class to store and retrieve words"""

import random

class WordsSet:
    """
    Stores a set of words of a fixed length and provides efficient retrieval
    based on character positions.

    Attributes:
        length (int): The fixed length of words in this set.
        words_by_char (dict[int, dict[str, set[str]]]): Maps character positions and characters to sets of words.
        all_words (set[str]): All words in the set.
    """

    def __init__(self, length: int):
        """
        Initializes a WordsSet for words of a specific length.

        Args:
            length (int): The length of words to store.
        """
        self.length = length
        self.words_by_char = {}
        self.all_words = set()

    def add_word(self, word: str):
        """
        Adds a word to the set, indexing it by character positions.

        Args:
            word (str): The word to add.

        Raises:
            ValueError: If the word length does not match the expected length.
        """
        if len(word) != self.length:
            raise ValueError(f"Word length {len(word)} does not match expected length {self.length}.")
        self.all_words.add(word)
        for i, char in enumerate(word):
            if i not in self.words_by_char:
                self.words_by_char[i] = {}
            if char not in self.words_by_char[i]:
                self.words_by_char[i][char] = set()
            self.words_by_char[i][char].add(word)

    def get_words(self, pattern: dict[int, str]) -> list[str]:
        """
        Retrieves all words matching a pattern of fixed characters at specific positions.

        Args:
            pattern (dict[int, str]): A mapping from character positions to required characters.

        Returns:
            list[str]: Words matching the pattern.
        """
        candidates: set = []
        for i in range(self.length):
            if i not in pattern:
                char_candidates = self.all_words
            else:
                char = pattern[i]
                char_candidates: set = self.words_by_char[i].get(char, set())
            if i == 0:
                candidates = char_candidates
            else:
                candidates = candidates & char_candidates
        return candidates


class Words:
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
        Retrieves words of a given length matching a regex-like pattern.

        Args:
            regex (str): A string pattern where fixed letters are specified and other positions are wildcards.
            length (int): The required word length.

        Returns:
            list[str]: A list of matching words, possibly randomized and limited in size.
        """
        pattern = self._get_pattern(regex)
        if length not in self.words_by_length:
            return []
        all_words = self.words_by_length[length].get_words(pattern)
        if self.randomize:
            all_words = list(all_words)
            random.shuffle(all_words)
        return all_words[:self.size] if len(all_words) > self.size else all_words

    def _get_pattern(self, regex: str) -> dict[int, str]:
        pattern: dict[int, str] = {}
        for i, char in enumerate(regex):
            if char.isalpha():
                pattern[i] = char
        return pattern
    
    def _read_words(self, file_path):
        """
        Reads words from the file and organizes them by length.
        :param file_path: Path to the word list file.
        """
        self.words_by_length: dict[int, WordsSet] = {}
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                stripped_word = line.strip()
                if stripped_word.startswith('#') or not stripped_word:
                    continue
                word_length = len(stripped_word)
                if word_length not in self.words_by_length:
                    self.words_by_length[word_length] = WordsSet(word_length)
                self.words_by_length[word_length].add_word(stripped_word)
