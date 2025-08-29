"""Entry point"""

import argparse
import logging
import time
from models import CrosswordSchema
from crossword_solver import CrosswordSolver
from words import Words

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     "Crossword maker from a schema and a list of words")
    parser.add_argument('--words', type=str, default='words.txt',
                        help='Path to words file')
    parser.add_argument('--grid', type=str, default='grid.json',
                        help='Path to grid file')
    parser.add_argument('--candidate-words-count', type=int, default=10,
                        help='Number of candidate words to consider per slot')
    parser.add_argument('--randomize', type=bool, default=True,
                        help='Whether to randomize the word list')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    import json
    with open(args.grid, 'r', encoding='utf-8') as f:
        grid = json.load(f)
    words = Words(args.words, args.candidate_words_count, args.randomize)
    schema = CrosswordSchema(grid)

    solver = CrosswordSolver(words, schema)
    start_time = time.perf_counter()
    crossword = solver.solve()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    crossword.display()
    print(f"Elapsed: {elapsed_time:.0f} seconds")
