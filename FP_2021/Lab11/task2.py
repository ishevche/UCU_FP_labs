"""fibonacci_factorial.py"""
import time


def numbers_time_test(num, function=0, realisation=0, verbose=False):
    """
    Compares time for recursion and cycles
    :param num: a number to find it's factorial or index of fibonachi's number
    :param function: 0 - factorial, 1 - fibonachi (def 0)
    :param realisation: 0 - recursion, 1 - cycle (def 0)
    :param verbose: display information (def False)
    :return:
    """
    funs = [[factorial_recursive, factorial_iterative],
            [fibonacci_recursive, fibonacci_iterative]]
    start = time.perf_counter()
    funs[function][realisation](num, verbose)
    end = time.perf_counter()
    return end - start


def factorial_recursive(num, verbose=False):
    """
    Calculates factorial using recursion
    :param num: a number to calculate
    :param verbose: display info (def False)
    :return: int
    >>> factorial_recursive(5)
    120
    """
    if num == 1:
        if verbose:
            print('1! = 1')
        return 1
    ans = factorial_recursive(num - 1, verbose) * num
    if verbose:
        print(f'{num}! = {ans}')
    return ans


def factorial_iterative(num, verbose=False):
    """
    Calculates factorial using cycles
    :param num: a number to calculate
    :param verbose: display info (def False)
    :return: int
    >>> factorial_iterative(5)
    120
    """
    cur_value = 1
    for cur_idx in range(1, num + 1):
        cur_value *= cur_idx
        if verbose:
            print(f'{cur_idx}! = {cur_value}')
    return cur_value


def fibonacci_recursive(index, verbose=False):
    """
    Calculates nth number of Fibonachi using recursion
    :param index: index
    :param verbose: display info (def=False)
    :return: int
    >>> fibonacci_recursive(5)
    8
    """
    if index == 1 or index == 0:
        if verbose:
            print(f'F({index}) = 1')
        return 1
    ans = fibonacci_recursive(index - 1, verbose) + \
          fibonacci_recursive(index - 2, verbose)
    if verbose:
        print(f'F({index}) = {ans}')
    return ans


def fibonacci_iterative(index, verbose=False):
    """
    Calculates nth number of Fibonachi using cycle
    :param index: index
    :param verbose: display info (def=False)
    :return: int
    >>> fibonacci_recursive(5)
    8
    """
    if verbose:
        print('F(0) = 1')
    if index == 0:
        return 1
    prevprev = 1
    prev = 1
    for cur_idx in range(1, index):
        if verbose:
            print(f'F({cur_idx}) = {prev}')
        cur_value = prev + prevprev
        prevprev = prev
        prev = cur_value
    if verbose:
        print(f'F({index}) = {prev}')
    return prev
