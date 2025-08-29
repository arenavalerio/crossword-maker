"""
Module for reading words from a file, skipping comments and blank lines.
"""

from typing import Generator


def read_words_from_file(file_path: str) -> Generator[str, None, None]:
    """
    Yield words from a file, skipping lines that are empty or start with '#'.

    Args:
        file_path (str): Path to the file containing words.

    Yields:
        str: Each valid word from the file.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            stripped_word = line.strip()
            if stripped_word.startswith('#') or not stripped_word:
                continue
            yield stripped_word
