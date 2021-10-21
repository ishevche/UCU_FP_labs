from math import sqrt


def four_lines_area(k1: float, c1: float, k2: float, c2: float,
                    k3: float, c3: float, k4: float, c4: float) -> float:
    """Calculates four lines area"""
    a = lines_intersection(k1, c1, k2, c2)
    b = lines_intersection(k2, c2, k3, c3)
    c = lines_intersection(k3, c3, k4, c4)
    d = lines_intersection(k4, c4, k1, c1)
    if a is None or b is None or c is None or d is None:
        return 0
    return quadrangle_area(
        distance(a[0], a[1], b[0], b[1]),
        distance(b[0], b[1], c[0], c[1]),
        distance(c[0], c[1], d[0], d[1]),
        distance(a[0], a[1], d[0], d[1]),
        distance(a[0], a[1], c[0], c[1]),
        distance(b[0], b[1], d[0], d[1])
    )


def lines_intersection(k1: float, c1: float, k2: float, c2: float) -> tuple:
    """
    Calculates an intersection point of two lines:
    y = k1 * x + c1
    y = k2 * x + c2

    :param k1: float
    :param c1: float
    :param k2: float
    :param c2: float
    :return: tuple, containing two elements: x and y coordinate of the
        intersection point or None if lines are parallel

    >>> lines_intersection(0, 0, 1, 0)
    (0.0, 0.0)
    >>> lines_intersection(1, 1, 5, -5)
    (1.5, 2.5)
    """
    if k1 == k2:
        return None
    x = (c1 - c2) / (k2 - k1)
    y = k1 * x + c1
    return round(x, 2), round(y, 2)


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculates a distance between two points

    :param x1: x coordinate of the first point
    :param y1: y coordinate of the first point
    :param x2: x coordinate of the second point
    :param y2: y coordinate of the second point
    :return: a distance between two points

    >>> distance(0, 0, 1, 0)
    1.0
    >>> distance(0, 0, 0, 1)
    1.0
    >>> distance(0, 0, 3, 4)
    5.0
    """
    return round(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2), 2)


def quadrangle_area(a: float, b: float, c: float, d: float,
                    f1: float, f2: float) -> float:
    """Calculates area of quadrangle"""
    time_var = (4 * f1 ** 2 * f2 ** 2 -
                (b ** 2 + d ** 2 - a ** 2 - c ** 2) ** 2)
    if time_var < 0:
        return None
    return round(sqrt(time_var / 16), 2)
