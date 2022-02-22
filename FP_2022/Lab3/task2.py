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
        >>> market_family_food = Markets('Family Food', 80, ['Bread and Bakery'\
        , 'Dairy', 'Beverages'])
        >>> print(market_family_food)
        Supermarket Family Food has an area of 80 m2 and has the following categories: \
Bread and Bakery, Dairy, Beverages.
        """
        return f"Supermarket {self.name} has an area of {self.area} " \
               f"m2 and has the following categories: " \
               f"{', '.join(self.categories)}."
