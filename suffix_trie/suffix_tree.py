from suffix_trie.trie_node import TrieNode


class SuffixTree:
    """
    suffix tree class to save sentences and get substrings in O(n)
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not SuffixTree.__instance:
            SuffixTree.__instance = object.__new__(cls)
        return SuffixTree.__instance

    def __init__(self):
        self.__root = TrieNode()

    def add_suffix(self, suffix, suffix_id):
        """
        add suffix to tree, in end of suffix put $ and array with the suffixes id
        """
        current_node = self.__root
        for char in suffix[:31]:
            if char not in current_node.get_children():
                current_node.add_children(char, TrieNode())
            current_node = current_node.get_children()[char]
            if '$' not in current_node.get_children():
                current_node.add_children('$', set())
            current_node.append_source(suffix_id)

    def add_sentence_to_tree(self, sentence, sentence_id):
        """
        add all sentence to tree
        """
        for i in range(len(sentence)):
            self.add_suffix(sentence[i:], sentence_id)

    def get_suffix_sources(self, substring):
        """
        get specific substring source by returning the array in the end - '$'
        return only 5 sources or less
        """
        index = 0
        score = 0
        node = self.__root
        while index < len(substring):
            if substring[index] in node.get_children():
                node = node.get_children()[substring[index]]
                score += 2
                index += 1
            else:
                break
        if index == len(substring):
            res = node.get_sources()
            if len(res) > 5:
                res = list(res)[:5]
                return [(i, score) for i in res]
            else:
                return [(i, score) for i in res]
        return []

    def get_replaced_suffix_sources(self, substring):
        """
        get substring source with the replacement of one letter, by returning the array in the end - '$'
        return only 5 sources or less
        """
        return self.search_if_changes(substring, 0)

    def get_added_suffix_sources(self, substring):
        """
        get substring source with  one letter added, by returning the array in the end - '$'
        return only 5 sources or less
        """
        if len(substring) == 1:
            return []
        res = []
        for i in range(len(substring) - 1, -1, -1):
            index = 0
            score = 0
            node = self.__root
            while index < len(substring):
                if index == i:
                    if i > 3:
                        score -= 2
                    elif i == 3:
                        score -= 4
                    elif i == 2:
                        score -= 6
                    elif i == 1:
                        score -= 8
                    elif i == 0:
                        score -= 10
                    index += 1
                elif substring[index] in node.get_children():
                    node = node.get_children()[substring[index]]
                    score += 2
                    index += 1
                else:
                    break
            if index == len(substring):
                current_sources = node.get_sources()
                for j in current_sources:
                    should_insert = True
                    for k in res:
                        if j == k[0]:
                            should_insert = False
                    if should_insert:
                        res.append((j, score))
                if len(res) >= 5:
                    return res[:5]
        return res

    def get_missing_suffix_sources(self, substring):
        """
        get substring source with  of one missing letter in substring, by returning the array in the end - '$'
        return only 5 sources or less
        """
        return self.search_if_changes(substring, 1)

    def search_if_changes(self, substring, range_index):
        """
        helper function to search substring with changes
        :param substring:
        :param range_index: Indicates whether it is a replacement (0) or a missing letter (1)
        :return:
        """
        index, score = 0, 0
        res = {}
        keep_search = True
        for i in range(range_index, len(substring)):
            node = self.__root
            idx_to_replace = len(substring) - 1 - i
            while index < idx_to_replace + range_index:
                if substring[index] in node.get_children():
                    node = node.get_children()[substring[index]]
                    score += 2
                    index += 1
                else:
                    keep_search = False
                    break
            if keep_search:
                for k in node.get_children().keys():
                    if k != "$" and k != substring[idx_to_replace]:
                        search_result = self.search_from_node(node.get_children()[k], substring[idx_to_replace + 1:])
                        if search_result:
                            # Conducts with the calculation of the score
                            for id in search_result[0]:
                                if idx_to_replace < 4:
                                    if range_index:
                                        score_culc = 10
                                        score_temp = 2
                                        temp2 = 1
                                    else:
                                        score_culc = 5
                                        score_temp = 1
                                        temp2 = 0
                                    res[id] = search_result[1] - (
                                            score_culc - (idx_to_replace + temp2) * score_temp) + score
                                else:
                                    res[id] = search_result[1] - 1 + score
                            if len(res) >= 5:
                                break
            index, score = 0, 0
            keep_search = True
            if len(res) >= 5:
                break
        return self.handle_result(res)

    def search_from_node(self, node, sub):
        """
        search given sub from given node in tree
        :return: score of the searching
        """
        index = 0
        score = 0
        node = node
        while index < len(sub):
            if sub[index] in node.get_children():
                node = node.get_children()[sub[index]]
                score += 2
                index += 1
            else:
                break
        if index == len(sub):
            return node.get_sources(), score

    def handle_result(self, res):
        """
        return the result in tuple array
        """
        result = []
        for i in range(min(5, len(res))):
            key = max(res, key=res.get)
            result.append((key, res[key]))
            del res[key]
        return result
