import os


class ReadData:
    def __init__(self, source, data_base):
        self.__source = source
        self.__db = data_base

    def scan_files(self):
        """
        scan given directory and it's file, and insert all data to DB
        """
        for dir_path, dirs, files in os.walk(self.__source):
            for filename in files:
                f_name = os.path.join(dir_path, filename)
                with open(f_name, encoding='utf-8') as my_file:
                    file_obj = my_file.read()
                    temp_strings_array = file_obj.split("\n")
                    for i in range(len(temp_strings_array)):
                        self.sentence_handler(temp_strings_array[i][:21], filename, i + 1)

    def sentence_handler(self, sentence, source, line_number):
        """
        clean sentence from file and insert it to db dict and to suffix tree
        :param sentence: sentence to insert
        :param source: the file where given sentence is
        :param line_number: sentence line number in file
        """
        sentence_id = self.__db.add_to_data_base(sentence, source, line_number)
        half_clear_sentence = sentence.lower()
        clear_sentence = ""
        for i in range(len(half_clear_sentence)):
            if half_clear_sentence[i].islower() or (sentence[i] == " " and sentence[i - 1] != " "):
                clear_sentence += sentence[i].lower()
        self.__db.add_to_suffix_tree(clear_sentence, sentence_id)
