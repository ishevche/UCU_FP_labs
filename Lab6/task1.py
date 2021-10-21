"""Has a function to get lucky numbers"""
from typing import List


def sieve_flavius(num: int) -> List[int]:
    """
    Returns a list of all lucky numbers up to n
    :param num: upperbound
    :return: a list containing all lucky numbers

    >>> sieve_flavius(100)
    [1, 3, 7, 9, 13, 15, 21, 25, 31, 33, 37, 43, 49, 51, 63, 67, 69, 73, 75, 79, 87, 93, 99]
    >>> sieve_flavius(10)
    [1, 3, 7, 9]
    >>> sieve_flavius(0)
    []
    """
    ans = [2 * i + 1 for i in range((num + 1) // 2)]
    cur_pos = 1
    while cur_pos < len(ans):
        del ans[ans[cur_pos] - 1::ans[cur_pos]]
        cur_pos += 1
    return ans
