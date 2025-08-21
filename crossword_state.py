from crossword import Crossword, CrosswordSchema, CoordinateWithDirection

class WrittenWord:
    def __init__(self, coordinate: CoordinateWithDirection, word: str, score: int):
        self.word = word
        self.coordinate = coordinate
        self.score = score

class CrosswordState:

    def __init__(self, schema: CrosswordSchema, last_coordinate: CoordinateWithDirection, written_words: list[WrittenWord]):
        self.schema = schema
        self.last_coordinate = last_coordinate
        self.written_words = written_words

    @staticmethod
    def create_initial_state(schema: CrosswordSchema):
        return CrosswordState(schema, None, [])
    
    def score(self) -> int:
        return sum(word.score for word in self.written_words)
    
    def get_crossword(self) -> Crossword:
        crossword = Crossword(self.schema)
        for written_word in self.written_words:
            slot = crossword.get_slot(written_word.coordinate)
            crossword.write_word(written_word.word, slot)
        return crossword
    
    def new_state(self, word: WrittenWord):
        new_words = self.written_words.copy()
        new_words.append(word)
        new_state = CrosswordState(self.schema, word.coordinate, new_words)
        return new_state