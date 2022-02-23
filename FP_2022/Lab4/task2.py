"""
cats.py
"""


class Animal:
    """
    Represents an animal
    """

    def __init__(self, phylum, clas):
        """
        Initializes classes references
        """
        self.phylum = phylum
        self.clas = clas

    def __str__(self):
        """
        Pretty representation of class data
        """
        return f'<animal class is {self.clas}>'

    def __eq__(self, other):
        """
        Compares two animal objects
        """
        return (other.clas == self.clas and
                other.phylum == self.phylum)


class Cat(Animal):
    """
    Represents a cat
    """

    def __init__(self, phylum, clas, genus):
        """
        Initializes classes references
        """
        super().__init__(phylum, clas)
        self.genus = genus

    def sound(self):
        """
        Represents a sound of cat
        """
        return "Meow"

    def __str__(self):
        """
        Pretty representation
        >>> cat1 = Cat("chordata", "mammalia", "felis")
        >>> str(cat1)
        '<This felis animal class is mammalia>'
        """
        return f'<This {self.genus} {super().__str__()[1:]}'
