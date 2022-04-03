"""square_preceding.py"""


def square_preceding(values: list):
    """ (list of number) -> NoneType
    Replace each item in the list with square the value of the
    preceding item, and replace the first item with 0.
    >>> L = [1, 2, 3]
    >>> square_preceding(L)
    >>> L
    [0, 1, 4]

    >>> L = []
    >>> square_preceding(L)
    >>> L
    []
    """
    if values:
        temp = values[0]
        values[0] = 0
    else:
        return
    for i in range(1, len(values)):
        values[i], temp = temp ** 2, values[i]
