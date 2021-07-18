class AutoCompleteData:
    def __init__(self, sentence, source):
        self.__completed_sentence = sentence
        self.__source_text = source
        self.__offset = None
        self.__score = None

    def set_offset(self, offset):
        self.__offset = offset

    def set_score(self, score):
        self.__score = score

    def __str__(self):
        return f" {self.__completed_sentence} (file: {self.__source_text}, line: {self.__offset}, score: {self.__score})"
