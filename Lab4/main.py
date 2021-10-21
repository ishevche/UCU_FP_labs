def get_number():
    """Specifies student number"""
    number = 22
    return number


# ****************************************
# Problem 5
# ****************************************
def type_by_sides(a, b, c):
    """
    (float, float, float) -> str
    Detect the type of triangle by it's sides and return type as string
    ("right angled triangle", "obutuse triangle", "acute triangle").
    If there is no triangle with such sides, then function should return None.

    >>> type_by_sides(3, 3, 3)
    'acute triangle'
    >>> type_by_sides(3, 4, 5)
    'right angled triangle'
    >>> type_by_sides(3, 5, 3)
    'obutuse triangle'
    >>> type_by_sides(3, 3, 2015)
    """
    a, b, c = sorted((a, b, c))
    if a + b <= c:
        return None
    if a**2 + b**2 > c**2:
        return 'acute triangle'
    if a**2 + b**2 == c**2:
        return 'right angled triangle'
    return 'obutuse triangle'


# ****************************************
# Problem 7
# ****************************************
def convert_to_column(s):
    """
    str -> str
    Convert string to a column of words.
    If argument is not a string function should return None.

    >>> print(convert_to_column("Revenge is a dish that tastes "
    ... "best when served cold."))
    revenge
    is
    a
    dish
    that
    tastes
    best
    when
    served
    cold
    >>> print(convert_to_column("Never hate your enemies. "
    ... "It affects your judgment."))
    never
    hate
    your
    enemies
    it
    affects
    your
    judgment
    >>> convert_to_column(2015)
    """
    ret = ""
    if not isinstance(s, str):
        return None
    for word in s.split():
        ret += word.lower().replace(".", "")
        if word != s.split()[-1]:
            ret += '\n'
    return ret


# ****************************************
# Problem 9
# ****************************************
def replace_with_stars(s):
    """
    str -> str
    Replace symbols in string with stars. If argument is not a string
    function should return None.

    >>> replace_with_stars("Revenge is a dish that tastes best "
    ... "when served cold.")
    '****************************************************'
    >>> replace_with_stars("Never hate your enemies. "
    ... "It affects your judgment.")
    '**************************************************'
    >>> replace_with_stars(2015)

    """
    if not isinstance(s, str):
        return None
    return "*" * len(s)


# ****************************************
# Problem 10
# ****************************************
def encrypt_message(s):
    """
    str -> str
    Replace all letters in string with next letters in aplhabet.
    If argument is not a string function should return None.

    >>> encrypt_message("Revenge is a dish that tastes best when served cold.")
    'Sfwfohf jt b ejti uibu ubtuft cftu xifo tfswfe dpme.'
    >>> encrypt_message("Never hate your enemies. It affects your judgment.")
    'Ofwfs ibuf zpvs fofnjft. Ju bggfdut zpvs kvehnfou.'
    >>> encrypt_message(2015)

    """
    if not isinstance(s, str):
        return None
    ans = ""
    for char in s:
        if not char.isalpha():
            ans += char
            continue
        if char == 'Z':
            ans += 'A'
        elif char == 'z':
            ans += 'a'
        else:
            cur_ord = ord(char)
            ans += chr(cur_ord + 1)
    return ans


# ****************************************
# Problem 12
# ****************************************
def exclude_letters(s1, s2):
    """
    (str, str) -> str
    Delete all letter from string s2 in string s1.
    If arguments aren't strings function should return None.

    >>> exclude_letters("aaabb", "b")
    'aaa'
    >>> exclude_letters("abcc", "cczzyy")
    'ab'
    >>> exclude_letters(2015, "sasd")

    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        return None
    for char in s2:
        s1 = s1.replace(char, "")
    return s1


# ****************************************
# Problem 13
# ****************************************
def create_string(lst):
    """
    list -> str
    Create and return string from histogrma of letters.
    If argument isn't list of 26 positive integer numbers
    function should return None.

    >>> create_string([0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ... 0, 0, 0, 0, 0, 0, 0])
    'bcc'
    >>> create_string([4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ... 0, 0, 0, 0, 0, 0, 4])
    'aaaazzzz'
    >>> create_string([4, 0, 0, 0, 0, 0])
    >>> create_string([4, 0, 0, 0, "0", 0])
    """
    try:
        ans = ""
        for i in range(ord('z') - ord('a') + 1):
            ans += chr(ord('a') + i) * lst[i]
        return ans
    except IndexError:
        return None
    except TypeError:
        return None


# ****************************************
# Problem 15
# ****************************************
def find_intersection(s1, s2):
    """
    (str, str) -> str
    Find and returs string of all letters in alphabetic order that
    are present in both strings. If arguments aren't strings function
    should return None.

    >>> find_intersection("aaabb", "bbbbccc")
    'b'
    >>> find_intersection("aZAbc", "zzYYxp")
    'z'
    >>> find_intersection("sfdfsdf", 2015)

    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        return None
    ans = ""
    s1 = s1.lower()
    s2 = s2.lower()
    for char in s1:
        if ans.__contains__(char):
            continue
        if s2.__contains__(char):
            ans += char
    return ''.join(sorted(ans))


# ****************************************
# Problem 16
# ****************************************
def find_union(s1, s2):
    """
    (str, str) -> str
    Find and return string of all letters in alphabetic order that
    are present in either strings. If arguments aren't strings function should
    return None.

    >>> find_union("aaabb", "bbbbccc")
    'abc'
    >>> find_union("aZAbc", "zzYYxp")
    'AYZabcpxz'
    >>> find_union("sfdfsdf", 2015)

    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        return None
    ans = ""
    for char in s1:
        if not ans.__contains__(char):
            ans += char
    for char in s2:
        if not ans.__contains__(char):
            ans += char
    return ''.join(sorted(ans))


# ****************************************
# Problem 21
# ****************************************
def polynomials_multiply(polynom1, polynom2):
    """
    >>> # (2x)*(3x) == 6
    >>> polynomials_multiply([2], [3])
    [6]
    >>> # (2x-4)*(3x+5) == 6x^2 -2x - 20
    >>> polynomials_multiply([2,-4],[3,5])
    [6, -2, -20]
    >>> # (2x^2-4)*(3x^3+2x) == (6x^5-8x^3-8x)
    >>> polynomials_multiply([2,0,-4],[3,0,2,0])
    [6, 0, -8, 0, -8, 0]

    """
    ans = [0] * (len(polynom1) + len(polynom2) - 1)
    for idx1, el1 in enumerate(polynom1):
        for idx2, el2 in enumerate(polynom2):
            ans[idx1 + idx2] += el1 * el2

    return ans


# ****************************************
# Problem 22
# ****************************************
def pattern_number(sequence):
    """
    >>> pattern_number([])
    >>> pattern_number([42])
    >>> pattern_number([1,2])
    >>> pattern_number([1,1])
    ([1], 2)
    >>> pattern_number([1,2,1])
    >>> pattern_number([1,2,3,1,2,3])
    ([1, 2, 3], 2)
    >>> pattern_number([1,2,3,1,2])
    >>> pattern_number([1,2,3,1,2,3,1])
    >>> pattern_number(list(range(10))*20)
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 20)
    >>> pattern_number('мама')
    ('ма', 2)
    >>> pattern_number('барабан')
    """
    for i in range(len(sequence)):
        div, mod = divmod(len(sequence), i + 1)
        if mod != 0 or div == 1:
            continue
        if sequence == sequence[:i + 1] * div:
            return sequence[:i + 1], div
    return None


# ****************************************
# Problem 24
# ****************************************
def numbers_Ulam(n):
    """
    >>> numbers_Ulam(10)
    [1, 2, 3, 4, 6, 8, 11, 13, 16, 18]
    >>> numbers_Ulam(2)
    [1, 2]
    >>> numbers_Ulam(1)
    [1]
    """
    ans = []
    for i in range(n):
        if i == 0:
            ans += [1]
            continue
        if i == 1:
            ans += [2]
            continue
        possible_sums = [0] * (ans[-1] + ans[-2] + 1)
        for idx1, el1 in enumerate(ans):
            for idx2 in range(idx1 + 1, len(ans)):
                el2 = ans[idx2]
                possible_sums[el1 + el2] += 1
        for idx, el in enumerate(possible_sums):
            if el == 1 and idx > ans[-1]:
                ans += [idx]
                break
    return ans


# ****************************************
# Problem 27
# ****************************************
def turn_over(n, lst):
    """
    Reverse first n items of the list and return it. If n <= 0, return
    the empty list. Do not consume MORE than n items of iterable.

    >>> turn_over(4, ['f', 'o', 'o', 't', 'b', 'a', 'l', 'l'])
    ['t', 'o', 'o', 'f', 'b', 'a', 'l', 'l']
    >>> turn_over(5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    [5, 4, 3, 2, 1, 6, 7, 8, 9, 10]
    >>> turn_over(10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> turn_over(-5, [])
    []
    """
    if n <= 0:
        return []
    n = min(n, len(lst))
    ans = []
    for i in range(1, n + 1):
        ans += [lst[n - i]]
    for i in range(n, len(lst)):
        ans += [lst[i]]
    return ans


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
