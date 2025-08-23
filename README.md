# Crossword Maker

A Python application that automatically generates and solves crossword puzzles using backtracking and word scoring algorithms.

## Features

- Automatically fills crossword grids with words from a provided word list
- Uses backtracking algorithm for puzzle solving
- Implements word scoring based on available words
- Supports both horizontal and vertical word placement
- Customizable grid layouts
- Minimum word length enforcement (4 letters by default)
- Optional randomization of word selection
- Console-based grid display

## Requirements

- Python 3.x
- A text file containing the word list (one word per line)

## Installation

Clone the repository:

```bash
git clone https://github.com/arenavalerio/crossword-maker.git
cd crossword-maker
```

## Usage

Run the program with a word list file:

```bash
python main.py <path_to_word_file>
```

The word file should be a text file containing one word per line. Lines starting with '#' and empty lines are ignored.

## Grid Configuration

The crossword grid is configured in `main.py`. The grid is represented as a 2D array where:
- `' '` (space) represents an empty cell where letters can be placed
- `'#'` represents a black square (blocking cell)

Example grid configuration:
```python
grid = [
    [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' '],
    [' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' '],
    [' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ']
]
```

## How It Works

1. **Grid Initialization**: The program creates a crossword grid based on the provided schema.

2. **Word Selection**: Words are loaded from the provided word list and organized by length.

3. **Solving Algorithm**:
   - Uses backtracking to try different word combinations
   - Scores potential words based on how well they fit with crossing words
   - Prioritizes words that create valid crossings
   - Continues until a complete solution is found or all possibilities are exhausted

4. **Word Scoring**:
   - Evaluates each candidate word based on how many valid words it allows in crossing directions
   - Considers existing letters and constraints
   - Ranks words by their potential to create valid crossings

## Configuration Options

In `main.py`:
- `CANDIDATE_WORDS`: Maximum number of candidate words to consider (default: 100)
- `RANDOMIZE_WORDS`: Whether to randomize word selection (default: True)
- `MIN_WORD_LENGTH`: Minimum length for words (default: 4, defined in `models/crossword.py`)

## Project Structure

- `main.py`: Entry point and grid configuration
- `crossword_solver.py`: Core solving algorithm
- `word_scorer.py`: Word scoring implementation
- `words.py`: Word list management
- `models/`: Core data structures
  - `crossword.py`: Crossword grid representation
  - `crossword_schema.py`: Grid layout definition
  - `cell.py`: Individual cell representation
  - `cell_slot.py`: Word slot management
  - `coordinate.py`: Grid coordinate system
  - `direction.py`: Word direction handling