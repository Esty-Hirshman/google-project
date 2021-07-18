class TrieNode:
    """The Suffix-tree's node. hole the char and set of children"""

    def __init__(self, char=""):
        self.__char = char
        self.__children = {}

    def get_char(self):
        return self.__char

    def set_char(self, new_char):
        self.__char = new_char

    def get_children(self):
        return self.__children

    def add_children(self, children, node):
        """
        add new children or end of suffix
        """
        self.__children[children] = node
        # if not end of suffix
        if children != '$':
            node.set_char(children)

    def get_sources(self):
        """
        get suffix sources
        """
        return self.__children["$"]

    def append_source(self, new_source):
        """
        add source to suffix
        """
        self.__children["$"].add(new_source)
