"""calculus.py"""
from functools import reduce


def find_max_1(function, points):
    """
    (function or str, list(number)) -> (number)

    Find and return maximal value of function f in points.

    >>> find_max_1('x ** 2 + x', [1, 2, 3, -1])
    12
    >>> find_max_1(lambda x: x ** 2 + x, [1, 2, 3, -1])
    12
    """
    if isinstance(function, str):
        function = 'lambda x: ' + function
        function = eval(function)
    return reduce(lambda x, y: max(x, function(y)),
                  points, function(points[0]))


def find_max_2(function, points):
    """
    (function or str, list(number)) -> (number)

    Find and return list of points where function f has the maximal value.

    >>> find_max_2('x ** 2 + x', [1, 2, 3, -1])
    [3]
    >>> find_max_2(lambda x: x ** 2 + x, [1, 2, 3, -1])
    [3]
    """
    if isinstance(function, str):
        function = 'lambda x: ' + function
        function = eval(function)
    answer = []
    cur_max = function(points[0])

    def update_answer(element):
        nonlocal answer, cur_max, function
        x_value = function(element)
        if x_value == cur_max:
            answer += [element]
        elif x_value > cur_max:
            answer = [element]
            cur_max = x_value

    list(map(update_answer, points))
    return answer


def compute_limit(seq):
    """
    (function or str) -> (number)

    Compute and return limit of a convergent sequence.

    >>> compute_limit('(n ** 2 + n) / n ** 2')
    1.0
    >>> compute_limit(lambda n: (n ** 2 + n) / n ** 2)
    1.0
    """
    if isinstance(seq, str):
        seq = eval('lambda n: ' + seq)
    prev = seq(1)
    cur = seq(10)
    i = 2
    while abs(cur - prev) >= 0.001:
        prev = cur
        cur = seq(10 ** i)
        i += 1
    return round(cur, 2)


def calculate(function, x_0, derx):
    """
    Calculates approximate derivative near <x_0>
    >>> calculate(lambda x: x, 1, 1)
    1.0
    >>> calculate(lambda x: x**2, 1, 0.001)
    2.0009999999996975
    """
    return (function(x_0 + derx) - function(x_0)) / derx


def compute_derivative(function, x_0):
    """
    (function or str, number) -> (number)

    Compute and return derivative of function f in the point x_0.

    >>> compute_derivative('x ** 2 + x', 2)
    5.0
    >>> compute_derivative(lambda x: x ** 2 + x, 2)
    5.0
    """
    if isinstance(function, str):
        function = eval('lambda x: ' + function)
    prev = calculate(function, x_0, 1)
    cur = calculate(function, x_0, 0.1)
    i = -2
    while abs(cur - prev) >= 0.001:
        prev = cur
        cur = calculate(function, x_0, 10 ** i)
        i -= 1
    return round(cur, 2)


def get_tangent(function, x_0):
    """
    (function or str, number) -> (str)

    Compute and return tangent line to function f in the point x_0.

    >>> get_tangent('x ** 2 + x', 2)
    '5.0 * x - 4.0'
    >>> get_tangent('- x ** 2 + x', 2)
    '- 3.0 * x + 4.0'
    >>> get_tangent(lambda x: x ** 2 + x, 2)
    '5.0 * x - 4.0'
    >>> get_tangent(lambda x: - x ** 2 + x, 2)
    '- 3.0 * x + 4.0'
    """
    if isinstance(function, str):
        function = eval('lambda x: ' + function)
    a_coef = compute_derivative(function, x_0)
    b_coef = round(function(x_0) - x_0 * a_coef, 2)
    answer = ''
    if a_coef < 0:
        answer = '- '
        a_coef *= -1
    answer += str(a_coef) + ' * x'
    if b_coef < 0:
        answer += ' - '
        b_coef *= -1
    else:
        answer += ' + '
    answer += str(b_coef)
    return answer


def get_root(function, start, end):
    """
    (function or str, number, number) -> (number)

    Compute and return root of the function f in the interval (a, b).

    >>> get_root('x', -1, 1)
    0.0
    >>> get_root(lambda x: x, -1, 1)
    0.0
    """
    if isinstance(function, str):
        function = eval('lambda x: ' + function)
    mid = (start + end) / 2
    mid_val = function(mid)
    if mid_val == 0:
        return round((start + end) / 2, 2)
    if mid_val > 0:
        if function(start) > 0:
            return get_root(function, mid, end)
        return get_root(function, start, mid)
    if function(start) > 0:
        return get_root(function, start, mid)
    return get_root(function, mid, end)
