"""Pascal"""


def generate_pascal_triangle(num: int) -> list:
    """
    Generates a pascal triangle
    :param num: rows to generate
    :return: list of list
        each sublist is a row of a triangle
    >>> generate_pascal_triangle(5)
    [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    """
    if num < 1:
        return []
    ans = [[1]]
    for row in range(1, num):
        ans += [[1]]
        for idx in range(1, row):
            ans[row] += [ans[row - 1][idx] + ans[row - 1][idx - 1]]
        ans[row] += [1]
    return ans
