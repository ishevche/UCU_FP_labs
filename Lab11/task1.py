"""recursive_functions.py"""


def create_table(height, width):
    """
    Creates table n*m, a triangle of pascal
    :param height: a height of table
    :param width: a width of table
    :return: a table - list of lists
    >>> create_table(4, 6)
    [[1, 1, 1, 1, 1, 1], [1, 2, 3, 4, 5, 6], [1, 3, 6, 10, 15, 21],\
 [1, 4, 10, 20, 35, 56]]
    >>> create_table(1, 5)
    [[1, 1, 1, 1, 1]]
    >>> create_table(5, 1)
    [[1], [1], [1], [1], [1]]
    """
    if height == 1:
        return [[1] * width]
    if width == 1:
        return [[1]] * height
    ans = create_table(height - 1, width)
    ans += [[1]]
    for idx in range(1, width):
        ans[-1] += [ans[-1][-1] + ans[-2][idx]]
    return ans


def flatten(lst):
    """
    Flattens a list
    :param lst: list to make flat
    :return: a list
    >>> flatten(3)
    3
    >>> flatten([1, [2]])
    [1, 2]
    >>> flatten([1, 2, [3, [4, 5], 6], 7])
    [1, 2, 3, 4, 5, 6, 7]
    >>> flatten(['wow', [2,[[]]], [True]])
    ['wow', 2, True]
    >>> flatten([])
    []
    >>> flatten([[]])
    []
    """
    if not isinstance(lst, list):
        return lst
    ans = []
    for element in lst:
        sublist = flatten(element)
        if isinstance(sublist, list):
            ans += sublist
        else:
            ans.append(sublist)
    return ans
