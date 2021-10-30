"""target_game.py"""
import copy
import random
import sys
from typing import List


def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    """
    ans = []
    for _ in range(3):
        ans += [[]]
        for _ in range(3):
            ans[-1] += [chr(random.choice(range(ord('A'), ord('Z') + 1)))]
    return ans


def get_words(file: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.
    >>> get_words("en", ["a", 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'])
    []
    >>> get_words('en', [element for element in 'wumrovkif'])
    ['fork', 'form', 'forum', 'four', 'fowk', 'from', 'frow', 'irok', 'komi', \
    'kori', 'miro', 'moki', 'ovum', 'work', 'worm', 'wouf']
    """
    ans = set()
    with open(file, 'r') as dict_file:
        for word in dict_file.read().split('\n'):
            word = word.lower()
            if check_word(word, letters):
                ans.add(word)
    return sorted(list(ans))


def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish.
    """
    ans = []
    for line in sys.stdin:
        ans += [line]
    return ans


def check_word(word: str, letters: List[str]) -> bool:
    """
    Checks if a word is according rules
    :param word: word to check
    :param letters: letters that word must consist of
    :return: True or False
    >>> check_word("stove", ['s', 't', 'o', 'v', 'e', 'a', 'a', 'a', 'a'])
    True
    """
    if letters[len(letters) // 2] not in word or len(word) < 4:
        return False
    letters_copy = copy.copy(letters)
    for word_letter in word:
        if word_letter not in letters_copy:
            return False
        else:
            letters_copy.remove(word_letter)
    return True


def get_pure_user_words(user_words: List[str], letters: List[str],
                        words_from_dict: List[str]) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    >>> get_pure_user_words(['a', 'aa', 'aaa'],\
    ["a", 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'], ['a', 'aa'])
    ['aaa']
    """
    dict_set = set(words_from_dict)
    ans = []
    for word in user_words:
        if check_word(word, letters):
            if word not in dict_set:
                ans += [word]
    return ans


def results():
    """
    Prints results
    :return: None
    >>> results()
    """
