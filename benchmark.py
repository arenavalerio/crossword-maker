"""Benchmarking the new regex implementation against the old one."""

import argparse
import time
from words import Words
from words.words_regex import WordsRegexSet

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     "Benchmark regex implementations with a word list.")
    parser.add_argument('--words', type=str, default='words.txt',
                        help='Path to words.txt file')
    parser.add_argument('--regexes', type=str, default='regexes.txt',
                        help='Path to file containing regexes, one per line')
    args = parser.parse_args()

    with open(args.regexes, 'r', encoding='utf-8') as f:
        regexes = [line.strip() for line in f if not line.startswith('#')]

    words = Words(args.words, 100, True)
    start = time.perf_counter()
    for regex in regexes:
        result = words.get_words_with_regex(regex, len(regex))
    end = time.perf_counter()
    print("----- Search by char -----")
    print(f"Elapsed: {end - start:.2f} seconds")
    print("----- Search by regex -----")
    words_bkp = WordsRegexSet(args.words, 100, True)
    start_bkp = time.perf_counter()
    for regex in regexes:
        result_bkp = words_bkp.get_words_with_regex(regex, len(regex))
    end_bkp = time.perf_counter()
    print(f"Elapsed: {end_bkp - start_bkp:.2f} seconds")
