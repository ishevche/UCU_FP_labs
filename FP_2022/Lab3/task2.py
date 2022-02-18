class Markets:
    """
    Class represent Markets
    """

    def __init__(self, name, area, categories):
        """
        Initializes class attributes
        """
        self.name = name
        self.area = area
        self.categories = categories

    def __str__(self):
        """
        Pretty representation
        """
        return f"Supermarket {self.name} has an area of {self.area} " \
               f"m2 and has the following categories: " \
               f"{', '.join(self.categories)}."
