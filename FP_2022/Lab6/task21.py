"""flower.py"""


class Flower:
    """
    Represents a flower
    """

    def __init__(self, color, petals, price):
        self.color = color
        self.petals = petals
        self.price = price
        if (not isinstance(color, str) or
                not isinstance(petals, int) or
                not isinstance(price, int) or
                petals < 0 or price < 0):
            raise ValueError('Wrong arguments')

    def __hash__(self):
        return hash((self.color, self.petals, self.price))


class Tulip(Flower):
    """
    Represents a tulip
    """

    def __init__(self, petals, price):
        super().__init__('pink', petals, price)


class Rose(Flower):
    """
    Represents a rose
    """

    def __init__(self, petals, price):
        super().__init__('red', petals, price)


class Chamomile(Flower):
    """
    Represents a chamomile
    """

    def __init__(self, petals, price):
        super().__init__('white', petals, price)


class FlowerSet:
    """
    Represents a flower set
    """

    def __init__(self):
        self.set = set()

    def add_flower(self, flower: Flower):
        """
        Adds flower to a set
        """
        self.set.add(flower)

    def total_price(self) -> int:
        """
        Calculates total price of the set
        """
        ans = 0
        for flower in self.set:
            ans += flower.price
        return ans


class Bucket:
    """
    Represents a bucket
    """

    def __init__(self):
        self.sets = list()

    def add_set(self, flower_set: FlowerSet):
        """
        Adds a flower set to a bucket
        """
        self.sets.append(flower_set)

    def total_price(self) -> int:
        """
        Calculates total price of the bucket
        """
        ans = 0
        for flower_set in self.sets:
            ans += flower_set.total_price()
        return ans
