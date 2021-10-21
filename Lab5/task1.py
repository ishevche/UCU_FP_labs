def total_occurrences(s1: str, s2: str, ch: str) -> int:
    """
    (str, str, str) -> int
    Precondition: len(ch) == 1
    Return the total number of times that ch occurs in s1 and s2.
    >>> total_occurrences('color', 'yellow', 'l')
    3
    >>> total_occurrences('red', 'blue', 'l')
    1
    >>> total_occurrences('green', 'purple', 'b')
    0
    >>> total_occurrences('', '', 'a')
    0
    """
    if len(ch) != 1:
        raise ValueError('Third parameter must be a single char')
    return s1.count(ch) + s2.count(ch)
