class Bird:
    """
    Represents a flying creature
    """

    def __init__(self, type_name: str):
        self.type = type_name
        self.eggs = set()
        self.eggs_count = 0

    def fly(self) -> str:
        """
        Returns message about fly ability of a bird
        """
        return 'I can fly!'

    def count_eggs(self) -> int:
        """
        Returns count of left eggs
        """
        return self.eggs_count

    def lay_egg(self):
        """
        Left an egg
        """
        self.eggs.add(Egg())
        self.eggs_count += 1

    def get_eggs(self) -> set:
        """
        Returns a set of left eggs
        """
        return self.eggs

    def __repr__(self):
        return f"{self.type} has {self.eggs_count} egg" + \
               ('s' if self.eggs_count != 1 else '')


class Egg:
    """
    Represents an egg
    """


class Penguin(Bird):
    """
    Represents penguin
    """

    def fly(self):
        """
        Returns message about fly ability of a penguin
        """
        return "No flying for me."

    def swim(self):
        """
        Returns message about swim ability of a penguin
        """
        return "I can swim!"


class MessengerBird(Bird):
    """
    Represents a message bird
    """

    def __init__(self, name, message=""):
        super().__init__(name)
        self.message = message

    def deliver_message(self):
        """
        Delivers a message
        """
        return self.message


def get_local_methods(clss):
    import types
    # This is a helper function for the test function below.
    # It returns a sorted list of the names of the methods
    # defined in a class. It's okay if you don't fully understand it!
    result = []
    for var in clss.__dict__:
        val = clss.__dict__[var]
        if isinstance(val, types.FunctionType):
            result.append(var)
    return sorted(result)


def test_bird_classes():
    print("Testing Bird classes...", end="")
    # A basic Bird has a species name, can fly, and can lay eggs
    bird1 = Bird("Parrot")
    assert (type(bird1) == Bird)
    assert (isinstance(bird1, Bird))
    assert (bird1.fly() == "I can fly!")
    assert (bird1.count_eggs() == 0)
    assert (str(bird1) == "Parrot has 0 eggs")

    # here changes
    assert (bird1.lay_egg() is None)
    eggs = bird1.get_eggs()
    egg = eggs.pop()
    assert (type(egg) == Egg)
    assert (isinstance(egg, Egg))
    # here changes ends

    assert (bird1.count_eggs() == 1)
    assert (str(bird1) == "Parrot has 1 egg")
    bird1.lay_egg()
    assert (bird1.count_eggs() == 2)
    assert (str(bird1) == "Parrot has 2 eggs")
    assert (get_local_methods(Bird) == ['__init__', '__repr__', 'count_eggs',
                                        'fly', 'get_eggs', 'lay_egg'])

    # A Penguin is a Bird that cannot fly, but can swim
    bird2 = Penguin("Emperor Penguin")
    assert (type(bird2) == Penguin)
    assert (isinstance(bird2, Penguin))
    assert (isinstance(bird2, Bird))
    assert (bird2.fly() == "No flying for me.")
    assert (bird2.swim() == "I can swim!")
    bird2.lay_egg()
    assert (bird2.count_eggs() == 1)
    assert (str(bird2) == "Emperor Penguin has 1 egg")
    assert (get_local_methods(Penguin) == ['fly', 'swim'])

    # A MessengerBird is a Bird that can optionally carry a message
    bird3 = MessengerBird("War Pigeon", message="Top-Secret Message!")
    assert (type(bird3) == MessengerBird)
    assert (isinstance(bird3, MessengerBird))
    assert (isinstance(bird3, Bird))
    assert (not isinstance(bird3, Penguin))
    assert (bird3.deliver_message() == "Top-Secret Message!")
    assert (str(bird3) == "War Pigeon has 0 eggs")
    assert (bird3.fly() == "I can fly!")

    bird4 = MessengerBird("Homing Pigeon")
    assert (bird4.deliver_message() == "")
    bird4.lay_egg()
    assert (bird4.count_eggs() == 1)
    assert (get_local_methods(MessengerBird) == ['__init__', 'deliver_message'])
    print("Done!")


if __name__ == '__main__':
    test_bird_classes()
