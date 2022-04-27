"""
polynomial.py
"""


class Polynomial:
    """
    Implementation of the Polynomial ADT using a sorted linked list.
    """

    def __init__(self, degree=None, coefficient=None):
        if degree is None:
            self._poly_head = None
        else:
            self._poly_head = _PolyTermNode(degree, coefficient)
        self._poly_tail = self._poly_head

    def degree(self):
        """
        Return the degree of the polynomial.
        """
        if self._poly_head is None:
            return -1
        else:
            return self._poly_head.degree

    def __getitem__(self, degree):
        assert self.degree() >= 0, \
            "Operation not permitted on an empty polynomial."
        cur_node = self._poly_head
        while cur_node is not None and cur_node.degree != degree:
            cur_node = cur_node.next

        if cur_node is None or cur_node.degree != degree:
            return 0.0
        else:
            return cur_node.coefficient

    def evaluate(self, scalar):
        """
        Evaluate the polynomial at the given scalar value.
        """
        assert self.degree() >= 0, \
            "Only non -empty polynomials can be evaluated."
        result = 0.0
        cur_node = self._poly_head
        while cur_node is not None:
            result += cur_node.coefficient * (scalar ** cur_node.degree)
            cur_node = cur_node.next
        return result

    def __add__(self, rhs_poly):
        return self.simple_add(rhs_poly)

    def __sub__(self, rhs_poly):
        new_poly = Polynomial()
        if self.degree() > rhs_poly.degree():
            max_degree = self.degree()
        else:
            max_degree = rhs_poly.degree()

        cur_degree = max_degree
        while cur_degree >= 0:
            value = self[cur_degree] - rhs_poly[cur_degree]
            new_poly._append_term(cur_degree, value)
            cur_degree -= 1
        return new_poly

    def __mul__(self, rhs_poly):
        new_poly = Polynomial()
        if self.degree() > rhs_poly.degree():
            max_degree = self.degree()
        else:
            max_degree = rhs_poly.degree()

        cur_degree = 2 * max_degree
        while cur_degree >= 0:
            value = 0
            start = min(max_degree, cur_degree)
            end = max(cur_degree - max_degree, 0)
            for first_degree in range(start, end - 1, -1):
                value += self[first_degree] * \
                         rhs_poly[cur_degree - first_degree]
            new_poly._append_term(cur_degree, value)
            cur_degree -= 1
        return new_poly

    def simple_add(self, rhs_poly):
        """
        Simple addition of two polynomials
        """
        new_poly = Polynomial()
        if self.degree() > rhs_poly.degree():
            max_degree = self.degree()
        else:
            max_degree = rhs_poly.degree()

        cur_degree = max_degree
        while cur_degree >= 0:
            value = self[cur_degree] + rhs_poly[cur_degree]
            new_poly._append_term(cur_degree, value)
            cur_degree -= 1
        return new_poly

    def _append_term(self, degree, coefficient):
        """
        Helper method for appending terms to the polynomial.
        """
        if coefficient != 0.0:
            new_term = _PolyTermNode(degree, coefficient)
            if self._poly_head is None:
                self._poly_head = new_term
            else:
                self._poly_tail.next = new_term
            self._poly_tail = new_term

    def __str__(self):
        res = ''
        cur = self._poly_head
        while cur is not None:
            res += f'{cur.coefficient}x^{cur.degree} + '
            cur = cur.next
        return res


class _PolyTermNode(object):
    """
    Class for creating polynomial term nodes used with the linked list.
    """

    def __init__(self, degree, coefficient):
        self.degree = degree
        self.coefficient = coefficient
        self.next = None

    def __str__(self):
        """
        Prints the value stored in self.
        __str__: Node -> Str
        """
        return str(self.coefficient) + "x" + str(self.degree)
