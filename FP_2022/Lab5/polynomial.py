import math
from copy import copy


class Polynomial:
    """
    Represents a polynomial equation
    """

    def __init__(self, coeffs: list | tuple):
        if isinstance(coeffs, tuple):
            self.coeffs = list(coeffs)
        else:
            self.coeffs = copy(coeffs)
        first_non_zero_coeff = 0
        while first_non_zero_coeff < len(coeffs) and \
                self.coeffs[first_non_zero_coeff] == 0:
            first_non_zero_coeff += 1
        self.coeffs = self.coeffs[first_non_zero_coeff:]
        if not self.coeffs:
            self.coeffs = [0]

    def degree(self):
        """
        Returns degree of the polynomial object
        >>> Polynomial([1, 2, 3]).degree()
        2
        """
        return len(self.coeffs) - 1

    def coeff(self, idx: int):
        """
        Returns coefficient for x**i
        >>> Polynomial([1, 2, 3]).coeff(2)  # x**2 + 2x + 3
        1
        """
        return self.coeffs[-idx - 1]

    def evalAt(self, point: float):
        """
        Returns value of polynomial in given point
        >>> Polynomial([1, 2, 3]).evalAt(1)
        6
        """
        cur_pow = 1
        ans = 0
        for coeff in reversed(self.coeffs):
            ans += coeff * cur_pow
            cur_pow *= point
        return ans

    def scaled(self, scale: float):
        """
        Returns a new polynomial with all the coefficients
        multiplied by the given scale
        >>> Polynomial([1, 2, 3]).scaled(10) == Polynomial([10, 20, 30])
        True
        """
        return Polynomial([x * scale for x in self.coeffs])

    def derivative(self):
        """
        Returns a new polynomial that is the derivative of the original
        >>> Polynomial([1, 2, 3]).derivative() == Polynomial([2, 2])
        True
        """
        return Polynomial([self.coeffs[-idx - 1] * idx
                           for idx in reversed(range(len(self.coeffs)))][:-1])

    def addPolynomial(self, other):
        """
        Returns a polynomial - a sum of two given ones
        >>> Polynomial([1, 2, 3]).addPolynomial(Polynomial([1])) == \
        Polynomial([1, 2, 4])
        True
        >>> Polynomial([1]).addPolynomial(Polynomial([1, 2, 3])) == \
        Polynomial([1, 2, 4])
        True
        """
        if not isinstance(other, Polynomial):
            return

        self_length = len(self.coeffs)
        other_length = len(other.coeffs)
        if self_length > other_length:
            new_coeffs = copy(self.coeffs)
            for idx in range(other_length):
                new_coeffs[-idx - 1] += other.coeffs[-idx - 1]
        else:
            new_coeffs = copy(other.coeffs)
            for idx in range(self_length):
                new_coeffs[-idx - 1] += self.coeffs[-idx - 1]
        return Polynomial(new_coeffs)

    def multiplyPolynomial(self, other):
        """
        Return a polynomial - a product of given ones
        >>> Polynomial([1, 2, 3]).multiplyPolynomial(Polynomial([1, 2])) == \
        Polynomial([1, 4, 7, 6])
        True
        """
        answer = Polynomial([])
        for idx in range(len(other.coeffs)):
            answer = answer.addPolynomial(
                self.add_power(idx).scaled(other.coeffs[-idx - 1])
            )
        return answer

    def add_power(self, power: int):
        """
        Returns a polynomial multiplied on x**power
        >>> Polynomial([1, 2, 3]).add_power(2) == Polynomial([1, 2, 3, 0, 0])
        True
        >>> Polynomial([1, 2, 3]).add_power(0) == Polynomial([1, 2, 3])
        True
        """
        return Polynomial(self.coeffs + ([0] * power))

    def __str__(self):
        return f'Polynomial(coeffs={self.coeffs})'

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return other.coeffs == self.coeffs
        elif isinstance(other, int):
            return len(self.coeffs) == 1 and \
                   self.coeffs[0] == other

    def __hash__(self):
        return hash(tuple(self.coeffs))


class Quadratic(Polynomial):
    """
    Represents quadratic polynomial
    """

    def __init__(self, coeffs: list | tuple):
        super().__init__(coeffs)
        if len(self.coeffs) != 3:
            raise ValueError('Quadratic equation must have '
                             'exactly 3 coefficients')

    def discriminant(self):
        """
        Calculates a discriminant of the quadratic equation
        >>> Quadratic([1, 2, 3]).discriminant()
        -8
        """
        return self.coeffs[1] ** 2 - 4 * self.coeffs[0] * self.coeffs[2]

    def numberOfRealRoots(self):
        """
        Returns amount of real roots of quadratic equation
        >>> Quadratic([1, 2, 1]).numberOfRealRoots()
        1
        """
        discriminant = self.discriminant()
        if discriminant < 0:
            return 0
        elif discriminant == 0:
            return 1
        else:
            return 2

    def getRealRoots(self):
        """
        Gets real roots of the quadratic equation
        >>> Quadratic([1, 5, 6]).getRealRoots()
        [-3.0, -2.0]
        """
        disc = self.discriminant()
        if disc < 0:
            return []
        elif disc == 0:
            return [-self.coeffs[1] / (2 * self.coeffs[0])]
        else:
            return [(-self.coeffs[1] - math.sqrt(disc)) / (2 * self.coeffs[0]),
                    (-self.coeffs[1] + math.sqrt(disc)) / (2 * self.coeffs[0])]

    def __str__(self):
        return f"Quadratic(a={self.coeffs[0]}, " \
               f"b={self.coeffs[1]}, c={self.coeffs[2]})"
