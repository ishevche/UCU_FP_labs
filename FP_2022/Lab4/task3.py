"""
furniture.py
"""


class Furniture:
    """
    Represents a furniture piece
    """

    def __init__(self, style, assign):
        """
        Initializes classes references
        """
        self.style = style
        self.assign = assign

    def __eq__(self, other):
        """
        Compares two animal objects
        """
        return (self.style == other.style and
                self.assign == other.assign)

    def __str__(self):
        """
        Pretty representation
        """
        return f'<furniture style is {self.style}>'


class Chair(Furniture):
    """
    Represents a chair
    """

    def __init__(self, style, assign, tipe):
        """
        Initializes classes references
        """
        super().__init__(style, assign)
        self.tipe = tipe

    def __str__(self):
        """
        Pretty representation
        >>> chair = Chair("empire", "bedroom", "armchair")
        >>> str(chair)
        '<This armchair furniture style is empire>'
        """
        return f'<This {self.tipe} {super().__str__()[1:]}'

    def get_assign(self):
        """
        Returns assigment
        """
        return self.assign
