import copy
import random
import time

import matplotlib.pyplot as plt

from linkedbst import LinkedBST


def demo_bst(path, words_amount=(10_000,)):
    words_list = read_dict(path)
    bst_random = LinkedBST(random.shuffle(words_list.copy()))
    bst_balanced = copy.deepcopy(bst_random)
    bst_balanced.rebalance()

    list_times = []
    random_times = []
    balanced_times = []

    for words_count in words_amount:
        words_to_find = random.sample(words_list, words_count)

        time_start = time.perf_counter()
        for word_to_find in words_to_find:
            word_to_find in words_list
        list_times += [time.perf_counter() - time_start]

        time_start = time.perf_counter()
        for word_to_find in words_to_find:
            word_to_find in bst_random
        random_times += [time.perf_counter() - time_start]

        time_start = time.perf_counter()
        for word_to_find in words_to_find:
            word_to_find in bst_balanced
        balanced_times += [time.perf_counter() - time_start]

    plt.plot(words_amount, list_times, label='sorted list')
    plt.plot(words_amount, random_times, label='random tree')
    plt.plot(words_amount, balanced_times, label='balanced tree')
    plt.yscale('log')
    plt.legend()
    plt.show()


def read_dict(path) -> list:
    ans = []
    with open(path, 'r') as dictionary:
        for word in dictionary:
            ans.append(word.replace('\n', ''))
    return ans


if __name__ == '__main__':
    demo_bst("words.txt", words_amount=range(0, 10000, 100))
