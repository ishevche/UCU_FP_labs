"""algorithms.py"""


def linear_search(list_of_values, value):
    """
    Searches <value> in <list_of_values> linearly
    :param list_of_values: list to search in
    :param value: value to search
    :return: index of value, or -1 if not find
    >>> linear_search([1, 5, 3, 4], 1)
    0
    >>> linear_search([1, 5, 3, 4], 2)
    -1
    >>> linear_search([1, 5, 3, 4], 3)
    2
    >>> linear_search([1, 5, 3, 4], 4)
    3
    >>> linear_search([1, 5, 3, 4], 5)
    1
    """
    ans = -1
    for idx, val in enumerate(list_of_values):
        if val == value:
            ans = idx
            break
    return ans


def merge_sort(lst):
    """
    Sorts a list
    :param lst: list to sort
    :return: sorted list
    >>> merge_sort([])
    []
    >>> merge_sort([1])
    [1]
    >>> merge_sort([2, 4, 7, 1, 3, 1, 6, 8, 5])
    [1, 1, 2, 3, 4, 5, 6, 7, 8]
    """
    if len(lst) <= 1:
        return lst
    middle = len(lst) // 2
    ans = []
    left = merge_sort(lst[:middle])
    right = merge_sort(lst[middle:])
    left_idx = 0
    right_idx = 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            ans += [left[left_idx]]
            left_idx += 1
        else:
            ans += [right[right_idx]]
            right_idx += 1
    ans += left[left_idx:] + right[right_idx:]
    return ans


def binary_search(list_of_values, value):
    """
    Searches <value> in <list_of_values> using binary search
    :param list_of_values: list to search in
    :param value: value to search
    :return: index of value, or -1 if not find
    >>> binary_search([1, 3, 4, 5], 1)
    0
    >>> binary_search([1, 3, 4, 5], 2)
    -1
    >>> binary_search([1, 3, 4, 5], 3)
    1
    >>> binary_search([1, 3, 4, 5], 4)
    2
    >>> binary_search([1, 3, 4, 5], 5)
    3
    >>> binary_search([], 5)
    -1
    """
    start = 0
    end = len(list_of_values)
    while start + 1 < end:
        middle = (end + start) // 2
        if list_of_values[middle] <= value:
            start = middle
        else:
            end = middle
    if len(list_of_values) != 0 and list_of_values[start] == value:
        return start
    return -1


def selection_sort(lst):
    """
    Sorts a list
    :param lst: list to sort
    :return: sorted list
    >>> selection_sort([])
    []
    >>> selection_sort([1])
    [1]
    >>> selection_sort([2, 4, 7, 1, 3, 1, 6, 8, 5])
    [1, 1, 2, 3, 4, 5, 6, 7, 8]
    """
    cur_pos = 0
    while cur_pos != len(lst):
        min_val = lst[cur_pos]
        min_idx = cur_pos
        for idx, val in enumerate(lst[cur_pos:]):
            if val < min_val:
                min_val = val
                min_idx = cur_pos + idx
        lst[cur_pos], lst[min_idx] = lst[min_idx], lst[cur_pos]
        cur_pos += 1
    return lst


def quick_sort(lst):
    """
    Sorts a list
    :param lst: list to sort
    :return: sorted list
    >>> quick_sort([])
    []
    >>> quick_sort([1])
    [1]
    >>> quick_sort([2, 4, 7, 1, 3, 1, 6, 8, 5])
    [1, 1, 2, 3, 4, 5, 6, 7, 8]
    """
    if len(lst) < 2:
        return lst
    left_insert = 0
    cur_pos = len(lst) - 1
    while left_insert != cur_pos and lst[left_insert] <= lst[cur_pos]:
        left_insert += 1
    while cur_pos != left_insert:
        if cur_pos - 1 != left_insert:
            lst[cur_pos], lst[cur_pos - 1], lst[left_insert] = \
                lst[left_insert], lst[cur_pos], lst[cur_pos - 1]
            cur_pos -= 1
            while left_insert != cur_pos and lst[left_insert] <= lst[cur_pos]:
                left_insert += 1
        else:
            lst[cur_pos], lst[left_insert] = lst[left_insert], lst[cur_pos]
            cur_pos -= 1
    return quick_sort(lst[:cur_pos]) + \
           [lst[cur_pos]] + \
           quick_sort(lst[cur_pos + 1:])
