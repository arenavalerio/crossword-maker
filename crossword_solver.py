from crossword import Crossword, CrosswordSchema, CellSlot
from crossword_state import CrosswordState, WrittenWord
from word_scorer import WordScorer
from words import Words
import logging

CANDIDATE_WORDS = 100
RANDOMIZE_CANDIDATES = True

class CrosswordSolver:

    def __init__(self, words: Words, schema: CrosswordSchema):
        self.schema = schema
        self.words = words
        self.iterations = 0

    def solve(self) -> Crossword:
        initial_state = CrosswordState.create_initial_state(self.schema)
        final_state = self._solve(initial_state)
        if(final_state is None):
            raise ValueError('No solution found')
        print(f"Total iterations: {self.iterations}")
        return final_state.get_crossword()


    def _solve(self, crosswordState: CrosswordState) -> CrosswordState | None:
        self.iterations += 1
        if crosswordState.get_crossword().get_next_available_coordinate(crosswordState.last_coordinate) is None:
            return crosswordState
        if crosswordState.last_coordinate is not None:
            logging.debug(f"Position {crosswordState.last_coordinate.x}, {crosswordState.last_coordinate.y}")
        else:
            logging.debug("Initial position")
        if len(crosswordState.written_words) > 0:
            logging.debug(f"Searching for Candidates - Word {crosswordState.written_words[-1]}")
        else:
            logging.debug("Searching initial candidate")
        next_candidates = self._get_next_candidates(crosswordState)
        logging.debug(f"Found candidates {next_candidates}")
        for candidate in next_candidates:
            logging.debug(f"Evaluating candidate {candidate.word} - Score {candidate.score}")
            next_state = crosswordState.new_state(candidate)
            next_state.get_crossword().display()
            solution = self._solve(next_state)
            if solution is not None:
                return solution
        logging.debug(f"Solution is not valid - discarding")
        return None
            
    def _get_next_candidates(self, state: CrosswordState) -> list[WrittenWord]:
        crossword = state.get_crossword()
        next_coordinate = crossword.get_next_available_coordinate(state.last_coordinate)
        if next_coordinate is None:
            return None
        slot = crossword.get_slot(next_coordinate)
        available_words = self.get_available_words(slot)
        word_scorer = WordScorer(crossword, slot, self.words)
        written_words_by_score: dict[int, list[str]] = {}
        for word in available_words:
            score = word_scorer.score_word(word)
            written_word = WrittenWord(next_coordinate, word, score)
            if score < 0:
                continue
            if score not in written_words_by_score:
                written_words_by_score[score] = []
            written_words_by_score[score].append(written_word)
        result = []
        keys = sorted(written_words_by_score.keys(), reverse=True)
        for score in keys:
            for item in written_words_by_score[score]:
                result.insert(0, item)
                if len(result) >= CANDIDATE_WORDS:
                    return result
        return result

    def get_available_words(self, slot: CellSlot) -> list[str]:
        regex = slot.get_regex()
        available_words = self.words.get_words_with_regex(regex, slot.length())
        return available_words