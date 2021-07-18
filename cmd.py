import threading
from read_data import ReadData
from data_base import DataBase
from result_search import ResultSearch
from config import source_folder
from termcolor import colored
import time
import sys
import os


class Cmd:
    def __init__(self):
        self.__db = DataBase()
        self.__handle_command = ResultSearch(self.__db)

    def run(self):
        """
        run the cmd
        """
        rd = ReadData(source_folder, self.__db)
        # thread to show animation when loading files
        t1 = threading.Thread(target=self.load_animation(), args=(2,))
        # thread to load files
        t2 = threading.Thread(target=rd.scan_files(), args=(2,))
        t2.start()
        t1.start()
        print("\nThe system is ready. Enter your text")
        text = ""
        # get input from user and search for results
        while True:
            current_text = input(colored(text, "green"))

            # start new search
            if current_text == "#":
                text = ""
                print(colored("start a new search: ", "blue"))
                continue
            current_text = self.clear_text(current_text)
            if current_text == "":
                continue
            else:
                text += current_text
            print("results: ")
            results = self.__handle_command.get_best_k_completions(text)
            for i in range(len(results)):
                print(f"{i + 1}. {results[i]}")

    def clear_text(self, sentence):
        """
        clear the user text from punctuation
        """
        half_clear_sentence = sentence.lower()
        clear_sentence = ""
        for i in range(len(half_clear_sentence)):
            if half_clear_sentence[i].islower() or (
                    half_clear_sentence[i] == " " and half_clear_sentence[i - 1] != " "):
                clear_sentence += half_clear_sentence[i]
        return clear_sentence

    def load_animation(self):
        """
        show animation while loading files
        """
        load_str = "Loading the files and preparing the system..."
        ls_len = len(load_str)
        animation = "|/-\\"
        anicount = 0
        counttime = 0
        i = 0
        while (counttime != 600):
            time.sleep(0.075)
            load_str_list = list(load_str)
            x = ord(load_str_list[i])
            y = 0
            if x != 32 and x != 46:
                if x > 90:
                    y = x - 32
                else:
                    y = x + 32
                load_str_list[i] = chr(y)
            res = ''
            for j in range(ls_len):
                res = res + load_str_list[j]
            sys.stdout.write("\r" + colored(res, "blue") + animation[anicount])
            sys.stdout.flush()
            load_str = res

            anicount = (anicount + 1) % 4
            i = (i + 1) % ls_len
            counttime = counttime + 1
        os.system("cls")
