"""cmudict.txt.py"""


def dict_reader_tuple(file_dict):
    """
    Reads dictionary
    :param file_dict: path to a dictionary
    :return: list of tuples
    >>> str(dict_reader_tuple("cmudict.txt"))[:3]
    "[('"
    """
    with open(file_dict, 'r') as dictionary:
        ans = []
        for entry in dictionary:
            word, num, *lst = entry.split()
            ans += [(word, int(num), lst)]
    return ans


def dict_reader_dict(file_dict):
    """
    Reads dictionary
    :param file_dict: path to a dictionary
    :return: list of tuples
    >>> str(dict_reader_dict("cmudict.txt"))[:2]
    "{'"
    """
    with open(file_dict, 'r') as dictionary:
        ans = {}
        for entry in dictionary:
            word, _, *lst = entry.split()
            if ans.__contains__(word):
                ans[word].add(tuple(lst))
            else:
                ans[word] = {tuple(lst)}
    return ans


def dict_invert(dct):
    """

    :param dct:
    :return:

    >>> dict_invert({'WATER':{('W','A','T','E','R')}})
    {1: {('WATER', ('W', 'A', 'T', 'E', 'R'))}}
    >>> str(dict_invert({'AABERG': {('AA1', 'B', 'ER0', 'G')}, 'A.': \
    {('EY1',)}, 'A': {('EY1',), ('AH0',)}, 'A42128': {('EY1', 'F', 'AO1', \
    'R', 'T', 'UW1', 'W', 'AH1', 'N', 'T', 'UW1', 'EY1', 'T')},\
    'AAA': {('T', 'R', 'IH2', 'P', 'AH0', 'L', 'EY1')}}))[:3]
    '{1:'
    >>> dict_invert(dict_reader_tuple('cmudict.txt')) == \
    dict_invert(dict_reader_dict('cmudict.txt'))
    True
    """
    ans = {}
    if isinstance(dct, dict):
        for key, val in dct.items():
            num = len(val)
            val = list(val)
            if not ans.__contains__(num):
                ans[num] = set()
            for idx in range(num):
                ans[num].add((key, val[idx]))
        return ans
    elif isinstance(dct, list):
        help_dict = {}
        for word in dct:
            help_dict[word[0]] = help_dict.get(word[0], []) + [tuple(word[2])]
        ans_list = list(help_dict.items())
        ans_list.sort(key=lambda x: len(x[1]))
        ans_dict = {}
        for word in ans_list:
            if not ans_dict.__contains__(len(word[1])):
                ans_dict[len(word[1])] = set()
            for transcription in word[1]:
                ans_dict[len(word[1])].add((word[0], transcription))
        return ans_dict
