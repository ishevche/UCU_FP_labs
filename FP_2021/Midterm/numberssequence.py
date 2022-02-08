"""
numberssequence.py - contains function to calculate
modified Niven's numbers
"""


def niven_numbers(length: int) -> list:
    """
    calculate modified Niven's numbers
    :param length: amount of numbers to calculate
    :return: list of first <length> modified elements
    >>> niven_numbers(14)
    [1, 10, 27, 68, 125, 222, 343, 520, 729, 1002, 1740, 5850, 8020, 9277]
    >>> niven_numbers(1)
    [1]
    >>> niven_numbers(0)
    []
    """
    answer = []
    cur_number = 1
    while len(answer) < length:
        sum_cur_number_digits = 0
        cur_number_copy = cur_number
        while cur_number_copy > 0:
            sum_cur_number_digits += cur_number_copy % 10
            cur_number_copy //= 10
        if cur_number % sum_cur_number_digits == 0:
            answer += [cur_number | cur_number ** 3]
        cur_number += 1
    return answer
