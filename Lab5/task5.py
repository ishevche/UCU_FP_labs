import sys


def return_digits(number: str) -> str:
    """
    Returns number printed in a specific way

    :param number: number to print
    :return: printed number

    >>> print(return_digits("41072819"))
       4   1   000  77777 222  888  1  9999
      44  11  0   0     72   28   811 9   9
     4 4   1 0     0   7 2  2 8   8 1 9   9
    4  4   1 0     0  7    2   888  1  9999
    444444 1 0     0 7    2   8   8 1     9
       4   1  0   0 7    2    8   8 1     9
       4  111  000  7    22222 888 111    9
    """
    ans = ""
    row = 0
    while row < 7:
        line = ""
        column = 0
        while column < len(number):
            digit = int(number[column])
            digit_array = Digits[digit]
            line += digit_array[row].replace("*", str(digit))
            column += 1
        ans += line
        row += 1
        if row != 7:
            ans += '\n'
    return ans


Zero = ["  ***  ",
        " *   * ",
        "*     *",
        "*     *",
        "*     *",
        " *   * ",
        "  ***  "]
One = [" * ", "** ", " * ", " * ", " * ", " * ", "***"]
Two = [" *** ", "*   *", "*  * ", "  *  ", " *   ", "*    ", "*****"]
Three = [" *** ", "*   *", "    *", "  ** ", "    *", "*   *", " *** "]
Four = ["   *  ", "  **  ", " * *  ", "*  *  ", "******", "   *  ", "   *  "]
Five = ["*****", "*    ", "*    ", " *** ", "    *", "*   *", " *** "]
Six = [" *** ", "*    ", "*    ", "**** ", "*   *", "*   *", " *** "]
Seven = ["*****", "    *", "   * ", "  *  ", " *   ", "*    ", "*    "]
Eight = [" *** ", "*   *", "*   *", " *** ", "*   *", "*   *", " *** "]
Nine = [" ****", "*   *", "*   *", " ****", "    *", "    *", "    *"]
Digits = [Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine]

try:
    digits = sys.argv[1]
    print(return_digits(digits))
except IndexError:
    print("usage: bigdigits.py <number>")
except ValueError as err:
    print(err, "in", digits)
