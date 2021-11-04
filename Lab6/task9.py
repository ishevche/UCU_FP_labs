"""target_ua.py"""

import random
from typing import List


def generate_grid() -> List[str]:
    """
    Generates a list of letters
    :return: list of letters
    >>> random.seed(1);generate_grid()
    ['и', 'д', 'р', 'з', 'ї']
    """
    alphabet = 'абвгдежзийклмнопрстуфхцчшщьюяєіїґ'
    return random.sample(alphabet, 5)


def get_words(file, letters):
    """
    Reads words from file at <file>
    :param file: location of the file
    :param letters: letters to start with returned words
    :return: a list of words from dictionaru that starts on one of letters from
        <letters>
    >>> get_words("base.lst", [])
    []
    >>> get_words("base.lst", ['й'])
    [('йняти', 'verb'), ('йог', 'noun'), ('йога', 'noun'), ('йод', 'noun'), \
('йодат', 'noun'), ('йодид', 'noun'), ('йодил', 'noun'), ('йодит', 'noun'), \
('йодль', 'noun'), ('йола', 'noun'), ('йолоп', 'noun'), ('йомен', 'noun'), \
('йон', 'noun'), ('йорж', 'noun'), ('йорж', 'noun'), ('йот', 'noun'), \
('йота', 'noun'), ('йти', 'verb'), ('йтися', 'verb')]
    """
    answer = []
    with open(file, 'r') as file_object:
        for word_line in file_object.read().split('\n'):
            if len(word_line.split(' ')) < 2:
                continue
            word, word_part = word_line.split(' ')[:2]
            if len(word) > 5 or len(word) < 1 or word[0] not in letters:
                continue
            word_part = word_part.lstrip('/')
            if word_part.startswith('n') and not \
                    word_part.startswith('no'):
                answer += [(word, 'noun')]
            elif word_part.startswith('v'):
                answer += [(word, 'verb')]
            elif word_part.startswith('adv'):
                answer += [(word, 'adverb')]
            elif word_part.startswith('adj'):
                answer += [(word, 'adjective')]
    return answer


def check_user_words(user_words, language_part, letters, dict_of_words):
    """
    Checks user words
    :param user_words: words from user
    :param language_part: a part of language words should be
    :param letters: letters with which words should start
    :param dict_of_words: list from get_words function
    :return: two lists: first - guessed words, second - missed words
    >>> check_user_words(['ddvxvx', 'fesfsef'], 'noun', ['k'], \
    get_words("base.lst", ['й']))
    ([], [])
    """
    good_words = []
    missed_words = []
    for dict_word, word_part in dict_of_words:
        if word_part != language_part or dict_word[0] not in letters:
            continue
        if dict_word in user_words:
            good_words += [dict_word]
        else:
            missed_words += [dict_word]
    return good_words, missed_words
