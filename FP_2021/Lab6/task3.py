"""Deals with happy numbers"""


def happy_number(number: int) -> bool:
    """
    Checks if number is happy
    :param number: number to check
    :return:
        True if number is happy
        False otherwise

    >>> happy_number(12345)
    False
    >>> happy_number(43211234)
    True
    >>> happy_number(191234)
    True
    """
    start, end = divmod(number, 10000)
    if (start <= 0 or end <= 0) and start != end:
        return False
    return start % 9 == end % 9


def count_happy_numbers(upper_bound: int) -> int:
    """
    Counts number of happy number from 0 up to upper_bound
    :param upper_bound: upperbound (inclusevly)
    :return: number of happy number from 0 up to upper_bound
    >>> count_happy_numbers(1)
    1
    """
    ans = 0
    for i in range(upper_bound + 1):
        if happy_number(i):
            ans += 1
    return ans


def happy_numbers(lower_bound: int, upper_bound: int) -> list:
    """
    Finds all happy numbers between lower_bound and upper_bound inclusively
    :param lower_bound: lower bound
    :param upper_bound: upper bound
    :return: list of all happy numbers between lower_bound and upper_bound
    >>> happy_numbers(0, 10001)
    [0, 10001]
    """
    ans = []
    for i in range(lower_bound, upper_bound + 1):
        if happy_number(i):
            ans += [i]
    return ans
