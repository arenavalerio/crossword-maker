from crossword import Crossword, CrosswordSchema, CoordinateWithDirection

class WrittenWord:
    """
    Represents a word written in the crossword, with its coordinate and score.
    """
    def __init__(self, coordinate: CoordinateWithDirection, word: str, score: int):
        self.word = word
        self.coordinate = coordinate
        self.score = score

class CrosswordState:
    """
    Represents the state of the crossword at a given point in the solving process.
    """

    def __init__(self, schema: CrosswordSchema, last_coordinate: CoordinateWithDirection, written_words: list[WrittenWord]):
        """
        Initialize a CrosswordState.
        :param schema: The crossword schema.
        :param last_coordinate: The last coordinate used.
        :param written_words: List of WrittenWord objects written so far.
        """
        self.schema = schema
        self.last_coordinate = last_coordinate
        self.written_words = written_words

    @staticmethod
    def create_initial_state(schema: CrosswordSchema):
        """
        Create the initial crossword state from a schema.
        :param schema: The crossword schema.
        :return: CrosswordState with no words written.
        """
        return CrosswordState(schema, None, [])
    
    def score(self) -> int:
        """
        Returns the total score for the current state (sum of word scores).
        """
        return sum(word.score for word in self.written_words)
    
    def get_crossword(self) -> Crossword:
        """
        Returns a Crossword object representing the current state.
        """
        crossword = Crossword(self.schema)
        for written_word in self.written_words:
            slot = crossword.get_slot(written_word.coordinate)
            crossword.write_word(written_word.word, slot)
        return crossword
    
    def new_state(self, word: WrittenWord):
        """
        Returns a new CrosswordState with the given word added.
        :param word: The WrittenWord to add.
        :return: New CrosswordState.
        """
        new_words = self.written_words.copy()
        new_words.append(word)
        new_state = CrosswordState(self.schema, word.coordinate, new_words)
        return new_state