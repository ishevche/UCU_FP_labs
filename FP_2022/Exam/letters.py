"""
letters.py
"""


class First:
    """
    Represents a class dealing with letters
    """

    def __init__(self, string):
        self.consonants = []
        self.vowels = []
        for letter in string:
            if letter in 'iauoey':
                self.vowels.append(letter)
            else:
                self.consonants.append(letter)

    def __str__(self):
        return f'First(consonants={self.consonants}, ' \
               f'vowels={self.vowels})'

    def __eq__(self, other):
        if not isinstance(other, First):
            return False
        return self.consonants == other.consonants

    def __ne__(self, other):
        return not self == other

    def clear_vowels(self):
        """
        Clears vowels
        """
        self.vowels = list()

    def cleared_vowels(self):
        """
        Returns new object without vowels
        """
        return First(self.consonants)

    def __hash__(self):
        return hash(self.consonants)


class Second(First):
    """
    Represents a class dealing with letters that can shift them
    """

    def __init__(self, string, shift):
        super().__init__(string)
        self.shift = shift

    def encoder(self):
        """
        Returns Caesar encod object
        """
        letters = list()
        for letter in self.consonants + self.vowels:
            num = ord(letter) - ord('a')
            length = ord('z') - ord('a') + 1
            num = (num + self.shift + length) % length
            num += ord('a')
            letters.append(chr(num))
        return Second(letters, -self.shift)
