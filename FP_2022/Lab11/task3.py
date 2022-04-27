"""
big_integer.py
"""
import random

VARIANT = 9


class BigInteger:
    """
    Represents a big decimal integer using linked lists
    """

    def __init__(self, int_value: str = ''):
        if int_value == '-0':
            int_value = '0'
        self._is_positive = True
        if int_value and int_value[0] == '-':
            self._is_positive = False
            int_value = int_value[1:]
        self._head = None
        self._tail = None
        self._degree = 0
        if int_value:
            while len(int_value) > 1 and int_value[0] == '0':
                int_value = int_value[1:]
            self._degree = len(int_value)
            self._head = Digit(int_value[0])
            self._tail = self._head
            int_value = int_value[1:]
            while int_value:
                next_digit = Digit(int_value[0])
                int_value = int_value[1:]
                self._tail.prev = next_digit
                next_digit.next = self._tail
                self._tail = next_digit

    def to_string(self):
        """
        Converts integer to string
        """
        number = '' if self._is_positive else '-'
        cur_digit = self._head
        while cur_digit is not None:
            number += str(cur_digit)
            cur_digit = cur_digit.prev
        return number

    def to_bitwise(self):
        """
        Transforms an integer to a boolean integer
        """
        if not self._is_positive:
            raise ValueError('Can not transform negative number')
        cur_val = self
        ans = ''
        while cur_val != '0':
            ans = f'{"1" if cur_val._tail.digit % 2 == 1 else "0"}{ans}'
            cur_val //= 2
        return BigInteger(ans)

    def from_bitwise(self):
        """
        Transforms a boolean integer to a decimal integer
        """
        ans = BigInteger('0')
        factor = BigInteger('1')
        cur_digit = self._tail
        while cur_digit is not None:
            ans += factor * cur_digit.digit
            factor *= 2
            cur_digit = cur_digit.next
        return ans

    def __str__(self):
        return self.to_string()

    def __neg__(self):
        self._is_positive = not self._is_positive
        ans = BigInteger(self.to_string())
        self._is_positive = not self._is_positive
        return ans

    def __le__(self, other):
        return self < other or self == other

    def __lt__(self, other):
        if not isinstance(other, BigInteger):
            raise ValueError('Can not compare BigInteger with not '
                             'BigInteger object')

        if not self._is_positive or not other._is_positive:
            # At least one negative
            if not self._is_positive and not other._is_positive:
                # -5 <= -2 <=> 2 <= 5
                return -other <= -self
            elif not self._is_positive:
                # -5 <= 2
                return True
            else:
                # 5 > -2
                return False

        if self._degree < other._degree:
            return True
        elif self._degree > other._degree:
            return False

        cur_self = self._head
        cur_other = other._head
        while cur_self is not None:
            if cur_self.digit < cur_other.digit:
                return True
            elif cur_other.digit < cur_self.digit:
                return False
            cur_self = cur_self.prev
            cur_other = cur_other.prev
        return False

    def __eq__(self, other):
        if isinstance(other, str):
            return self.to_string() == other
        if not isinstance(other, BigInteger):
            raise ValueError('Can not compare BigInteger with not '
                             'BigInteger object')
        if self._degree != other._degree or \
                self._is_positive != other._is_positive:
            return False
        cur_self = self._head
        cur_other = other._head
        while cur_self is not None:
            if cur_self.digit != cur_other.digit:
                return False
            cur_self = cur_self.prev
            cur_other = cur_other.prev
        return True

    def __add__(self, other):
        if not isinstance(other, BigInteger):
            raise ValueError('Can not add BigInteger to not '
                             'BigInteger object')
        if self._is_positive != other._is_positive:
            if self._is_positive:
                return self - -other
            else:
                return other - -self
        ans = ''
        cur_self = self._tail
        cur_other = other._tail
        overflow = 0
        while cur_self is not None and cur_other is not None:
            overflow, next_digit = divmod(cur_self.digit +
                                          cur_other.digit +
                                          overflow, 10)
            ans = f'{next_digit}{ans}'
            cur_self = cur_self.next
            cur_other = cur_other.next

        cur_left = cur_self if cur_other is None else cur_other
        while cur_left is not None:
            overflow, next_digit = divmod(cur_left.digit +
                                          overflow, 10)
            ans = f'{next_digit}{ans}'
            cur_left = cur_left.next

        if overflow:
            ans = f'{overflow}{ans}'
        if not self._is_positive:
            ans = f'-{ans}'
        return BigInteger(ans)

    def __sub__(self, other):
        if not isinstance(other, BigInteger):
            raise ValueError('Can not subtract BigInteger to not '
                             'BigInteger object')
        if self._is_positive != other._is_positive:
            if self._is_positive:
                return self + -other
            else:
                return self + -other
        if not self._is_positive:
            return -(-self - -other)
        if self < other:
            return -(other - self)
        ans = ''
        cur_self = self._tail
        cur_other = other._tail
        overflow = 0
        while cur_self is not None and cur_other is not None:
            overflow, next_digit = divmod(cur_self.digit -
                                          cur_other.digit +
                                          overflow, 10)
            ans = f'{next_digit}{ans}'
            cur_self = cur_self.next
            cur_other = cur_other.next

        cur_left = cur_self if cur_other is None else cur_other
        while cur_left is not None:
            overflow, next_digit = divmod(cur_left.digit +
                                          overflow, 10)
            ans = f'{next_digit}{ans}'
            cur_left = cur_left.next
        if overflow:
            if ans[0] == str(-overflow):
                ans = ans[1:]
            else:
                ans = f'{int(ans[0]) + overflow}{ans[1:]}'
        return BigInteger(ans)

    def __mul__(self, other):
        if isinstance(other, int):
            if other < 0:
                return -(self * -other)
            if not self._is_positive:
                return -(-self * other)
            ans = ''
            cur_self = self._tail
            overflow = 0
            while cur_self is not None:
                overflow, next_digit = divmod(cur_self.digit * other +
                                              overflow, 10)
                ans = f'{next_digit}{ans}'
                cur_self = cur_self.next
            if overflow:
                ans = f'{overflow}{ans}'
            return BigInteger(ans)
        if not isinstance(other, BigInteger):
            raise ValueError('Can not multiply BigInteger to not '
                             'BigInteger object')
        cur_self = self._head
        ans = BigInteger('0')
        while cur_self is not None:
            ans *= 10
            ans += other * cur_self.digit
            cur_self = cur_self.prev
        return ans if self._is_positive else -ans

    def __mod__(self, other):
        if isinstance(other, str):
            return self % BigInteger(other)
        if other == '0':
            raise ValueError('Can not get mod 0')
        if not isinstance(other, BigInteger):
            raise ValueError('Can not mod BigInteger to not '
                             'BigInteger object')
        if self._is_positive != other._is_positive:
            ans = self
            while ans._is_positive != other._is_positive and ans != '0':
                ans += other
            return ans
        if self._is_positive:
            ans = self
            while other <= ans:
                ans -= other
            return ans
        else:
            ans = self
            while ans <= other:
                ans -= other
            return ans

    def __floordiv__(self, other):
        if isinstance(other, int) and self._is_positive:
            ans = ''
            cur_digit = self._head
            overflow = 0
            while cur_digit is not None:
                next_digit, overflow = divmod(cur_digit.digit +
                                              10 * overflow, other)
                ans += f'{next_digit}'
                cur_digit = cur_digit.prev
            return BigInteger(ans)

    def __rshift__(self, other):
        if not isinstance(other, BigInteger):
            raise ValueError('Can not shift on non BigInteger amount of digits')
        value = str(self.to_bitwise())
        left = other
        one = BigInteger('1')
        while left != '0':
            value = value[:-1]
            left -= one
        if not value:
            value = '0'
        return BigInteger(value)

    def __and__(self, other):
        if not isinstance(other, BigInteger):
            raise ValueError('Can not perform bitwise and with '
                             'non BigInteger object')
        self_bin = self.to_bitwise()
        other_bin = other.to_bitwise()
        cur_self = self_bin._tail
        cur_other = other_bin._tail
        ans = ''
        while cur_self is not None and cur_other is not None:
            ans = \
                f'{cur_self.digit if cur_other.digit == cur_self.digit else 0}' \
                f'{ans}'
            cur_self = cur_self.next
            cur_other = cur_other.next
        return BigInteger(ans)


class Digit:
    """
    Represent a digit node in a big integer linked list
    """

    def __init__(self, digit):
        if isinstance(digit, str):
            if len(digit) != 1 or ord(digit) < ord('0') or \
                    ord(digit) > ord('9'):
                raise ValueError(f'{digit} is not a digit')
            self.digit = ord(digit) - ord('0')
        elif isinstance(digit, int):
            if digit < 0 or digit > 9:
                raise ValueError(f'{digit} is not a digit')
            self.digit = digit
        self.next = None
        self.prev = None

    def __str__(self):
        return str(self.digit)


if __name__ == '__main__':
    # ['<=', '=='] ['*', '%'] ['>>', '&']
    assert BigInteger('12340').to_string() == '12340'
    assert BigInteger('-56789').to_string() == '-56789'
    assert BigInteger('1234') == BigInteger('1234')
    assert BigInteger('123') != BigInteger('1234')
    assert BigInteger('-1234') != BigInteger('1234')
    assert BigInteger('-5678') <= BigInteger('1234')
    assert BigInteger('-123456') <= BigInteger('1234')
    assert BigInteger('234') <= BigInteger('1234')
    assert BigInteger('1122') <= BigInteger('1211')
    assert BigInteger('-1211') <= BigInteger('-1122')
    assert (BigInteger("10") & BigInteger("2")).to_string() == '10'
    for _ in range(1_000):
        a = random.randint(-1000000, 1000000)
        b = random.randint(-1000000, 1000000)
        if a >= 0:
            n = random.randint(1, 100)
            assert BigInteger(str(a)) // 2 == str(a // 2), f'{a}'
            assert BigInteger(str(a)).to_bitwise() == bin(a)[2:], f'{a}'
            assert BigInteger(str(a)) >> BigInteger(str(n)) == str(bin(a >> n)[2:]), \
                f'{a}, {n}'
        if b >= 0:
            assert BigInteger(str(b)) // 2 == str(b // 2), f'{b}'
        if a >= 0 and b >= 0:
            assert BigInteger(str(a)) & BigInteger(str(b)) == str(bin(a & b)[2:]), \
                f'{a}, {b} -> {BigInteger(str(a)) & BigInteger(str(b))}'
        if b != 0:
            assert BigInteger(str(a)) % BigInteger(str(b)) == str(a % b), \
                f'{a}, {b}'
        assert BigInteger(str(a)) * BigInteger(str(b)) == str(a * b), \
            f'{a}, {b}'
        assert BigInteger(str(a)) + BigInteger(str(b)) == str(a + b), \
            f'{a}, {b}'
        assert BigInteger(str(a)) - BigInteger(str(b)) == str(a - b), \
            f'{a}, {b}'
        assert (BigInteger(str(a)) == BigInteger(str(b))) == (a == b), \
            f'{a}, {b}'
        assert (BigInteger(str(a)) <= BigInteger(str(b))) == (a <= b), \
            f'{a}, {b}'
