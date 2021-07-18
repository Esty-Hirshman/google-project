from suffix_trie import SuffixTree


class DataBase:
    __instance = None
    __next_id = 0
    __dictionary = {}
    __suffix_tree = SuffixTree()

    def __new__(cls, *args, **kwargs):
        if not DataBase.__instance:
            DataBase.__instance = object.__new__(cls)
        return DataBase.__instance

    def add_to_data_base(self, sentence, source, line_number):
        """
        add sentence to dict with given parameters
        :param sentence:
        :param source:
        :param line_number:
        """
        self.__dictionary[DataBase.__next_id] = (sentence, source, line_number)
        DataBase.__next_id += 1
        return DataBase.__next_id - 1

    def get_by_id(self, id_number):
        """
        get sentence from dict by id
        :param id_number: id
        :return: tuple with sentence, source,line number
        """
        return self.__dictionary[id_number]

    def add_to_suffix_tree(self, clear_sentence, sentence_id):
        """
        add the sentence to suffix tree
        :param clear_sentence: sentence in cleared form
        :param sentence_id: sentence id in db dict
        """
        self.__suffix_tree.add_sentence_to_tree(clear_sentence, sentence_id)

    def get_suffix_tree(self):
        """
        get all suffix tree data
        """
        return self.__suffix_tree
