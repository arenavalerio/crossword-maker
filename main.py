"""Entry point"""

import logging
import sys
import time
from models import CrosswordSchema
from crossword_solver import CrosswordSolver
from words import Words


grid = [
    # The crossword grid layout, where '#' is a black square and ' ' is empty.
    [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' '],
    [' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' '],
    [' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' '],
    [' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' '],
    [' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ']
]

CANDIDATE_WORDS = 100
RANDOMIZE_WORDS = True

"""
Main entry point for the crossword solver application.
Loads the word list, initializes the crossword schema, and solves the puzzle.
"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_word_file>")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    words = Words(sys.argv[1], CANDIDATE_WORDS, RANDOMIZE_WORDS)
    schema = CrosswordSchema(grid)

    solver = CrosswordSolver(words, schema)
    start_time = time.perf_counter()
    crossword = solver.solve()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    crossword.display()
    print(f"Elapsed: {elapsed_time:.0f} seconds")
