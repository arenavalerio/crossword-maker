import random
import re


class Words:

    def __init__(self, file_path: str, size: int, randomize: bool):
        self.size = size
        self.randomize = randomize
        self._read_words(file_path)
    
    def get_words_with_regex(self, regex: str, length: int) -> list[str]:
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
        self.words_by_length = {}
        with open(file_path, 'r') as file:
            for line in file:
                stripped_word = line.strip()
                if stripped_word.startswith('#') or not stripped_word:
                    continue
                word_length = len(stripped_word)
                if word_length not in self.words_by_length:
                    self.words_by_length[word_length] = []
                self.words_by_length[word_length].append(stripped_word)
        if self.randomize:
            for key in self.words_by_length.keys():
                random.shuffle(self.words_by_length[key])