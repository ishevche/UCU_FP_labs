class Rational:
    """
    Represents a fraction
    """

    def __init__(self, nominator, denominator):
        self.nominator = nominator
        self.denominator = denominator

    def __str__(self):
        return f"{self.nominator}/{self.denominator}"

    def __add__(self, other):
        return Rational(self.nominator * other.denominator +
                        self.denominator * other.nominator,
                        self.denominator * other.denominator)

    def __sub__(self, other):
        return Rational(self.nominator * other.denominator -
                        self.denominator * other.nominator,
                        self.denominator * other.denominator)

    def __mul__(self, other):
        return Rational(self.nominator * other.nominator,
                        self.denominator * other.denominator)

    def __truediv__(self, other):
        return Rational(self.nominator * other.denominator,
                        self.denominator * other.nominator)


def test_rational():
    print("Testing class Rational ...")
    # This is an implementation of a Rational numbers
    # that consist of 2 parts - nominator and denominator.
    # You can imagine this Ratinal numbers as fractions
    # like 3/4
    rational1 = Rational(1, 4)
    assert (type(rational1) == Rational)
    assert (isinstance(rational1, Rational))
    assert (str(rational1) == "1/4")

    # here you can add two numbers
    rational2 = Rational(2, 5)
    assert (str(rational1 + rational2) == "13/20")

    # here is a substraction
    assert (str(rational1 - rational2) == "-3/20")

    # multiplication
    assert (str(rational1 * rational2) == "2/20")

    # division
    assert (str(rational1 / rational2) == "5/8")

    assert (type(rational1 + rational2) == Rational)
    assert (type(rational1 - rational2) == Rational)
    assert (type(rational1 * rational2) == Rational)
    assert (type(rational1 / rational2) == Rational)

    print("Done!")


if __name__ == '__main__':
    test_rational()
