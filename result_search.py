from operator import itemgetter
from termcolor import colored
from auto_complete_data import AutoCompleteData


class ResultSearch:
    def __init__(self, db):
        self.__db = db

    def handle_command(self, text):
        """
        Returns the search-matching simplifiers with the highest score
        :param text: text to search for
        """

        # Looking for the input in its entirety
        res_regular = self.__db.get_suffix_tree().get_suffix_sources(text)
        # if not enough results
        if len(res_regular) < 5:
            # Looks for appropriate input phrases with one letter replaced
            res_replaced = self.__db.get_suffix_tree().get_replaced_suffix_sources(text)
            # Searches for appropriate input phrases with one missing letter
            res_missing = self.__db.get_suffix_tree().get_missing_suffix_sources(text)
            # Searches for appropriate input sentences with one redundant letter
            res_added = self.__db.get_suffix_tree().get_added_suffix_sources(text)
            res = res_regular + res_replaced + res_added + res_missing
            result = []
            i = 0
            while i < min(5, len(res)):
                max_score = max(res, key=itemgetter(1))
                if max_score[0] in [x[0] for x in result]:
                    i += 1
                    continue
                result.append(max_score)
                res.pop(res.index(max(res, key=itemgetter(1))))
                i += 1
            return result
        return res_regular

    def sort_result(self, result_array):
        """
        sort the sentences in result by lexicographic value
        """
        sorted_sentences = []
        for res in result_array:
            sorted_sentences.append((self.__db.get_by_id(res[0]), res[1]))
        return sorted(sorted_sentences)

    def get_best_k_completions(self, prefix):
        """
        create the result and return list of result objects
        with the required fields: the sentence, the score, the line in the file, the name of the file in which it is located
        :param prefix: prefix to search for
        """
        result_data = []
        res = self.handle_command(prefix)
        result_array = self.sort_result(res)
        if len(result_array) == 0:
            print(colored("not found", "red"))
        # create AutoCompleteData object from the result
        for i in range(len(result_array)):
            sentence = result_array[i]
            sentence_object = AutoCompleteData(sentence[0][0], sentence[0][1])
            sentence_object.set_score(sentence[1])
            sentence_object.set_offset(sentence[0][2])
            result_data.append(sentence_object)
            # print(f"{i + 1}. {sentence[0][0]} (file: {sentence[0][1]}, line: {sentence[0][2]}, score: {sentence[1]})")
        return result_data
