"""
Game objects
"""


class Item:
    """
    Represents an item that can be used to fight
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def display_details(self):
        """
        Prints a details about the item
        """
        print(f'The [{self.name}] is here - {self.description}')

    def use(self, room) -> bool:
        """
        Uses an item
        """
        print("This item can not be used")
        return False

    def __str__(self):
        return f"{self.name} - {self.description}"

    def __eq__(self, other):
        return self.name == other.name


class KeyItem(Item):
    """
    Represents an key item
    """

    def use(self, room) -> bool:
        """
        Unlocks a room if it is a such one
        """
        if not isinstance(room, LockedRoom):
            print("You can not use this item here")
            return False
        print("This location is successfully unlocked")
        room.unlocked = True
        return True


class ExchangeableItem(Item):
    """
    Item that can be exchanged for another item
    """

    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def use(self, room) -> bool:
        """
        Exchanges an item for another one
        """
        habitat = room.character
        if (not isinstance(habitat, Friend) or
                habitat.wanted != self or
                room.item is not None):
            print("You can not use this item here")
            return False
        print(f'In a respect for your gift {habitat.name} offered you '
              f'{habitat.reward.name}')
        room.item = habitat.reward
        return True


class Character:
    """
    Represents a game character
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.conversation = None

    def display_details(self):
        """
        Prints a details about the character
        """
        print(f'{self.name} is here!')
        print(self.description)

    def talk(self):
        """
        Prints a conversation
        """
        print(f"[{self.name} says]: {self.conversation}")


class Enemy(Character):
    """
    Represents an enemy to fight with
    """

    amount_defeated = 0

    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.weakness = None

    def display_details(self):
        """
        Prints a details about the enemy
        """
        print(f'Strange {self.name} is here - {self.description}')

    def fight(self, weapon: Item) -> bool:
        """
        Represents a fight
        """
        if weapon == self.weakness:
            Enemy.amount_defeated += 1
            print(f'You fend {self.name} off with the {weapon.name}')
            return False
        else:
            print(f"{self.name} crushes you, puny adventurer!")
            return True


class Boss(Enemy):
    """
    Represent a main enemy
    """

    def __init__(self, name: str, description: str, helpers_amount):
        super().__init__(name, description)
        self.helpers_amount = helpers_amount
        self.defeated = False

    def display_details(self):
        """
        Prints a details about the boss
        """
        print(f'Frightening {self.name} is here - {self.description}')

    def fight(self, weapon: Item) -> bool:
        """
        Represents a fight
        """
        if weapon == self.weakness:
            if Enemy.amount_defeated < self.helpers_amount:
                print(f"You was stained by {self.name}'s guard")
                return True
            self.defeated = True
            print(f'You fend {self.name} off with the {weapon.name}')
            return False
        else:
            print(f"{self.name} crushes you, puny adventurer!")
            return True


class Friend(Character):
    """
    Represents a friend
    """

    def __init__(self, name: str, description: str,
                 wants_item: Item, gives_item: Item):
        super().__init__(name, description)
        self.wanted = wants_item
        self.reward = gives_item

    def display_details(self):
        """
        Prints a details about the character
        """
        print(f'Friendly {self.name} is here - {self.description}')


class Room:
    """
    Represents a room to walk in
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.links: dict[str, Room] = {}
        self.description = description
        self.character: Character | None = None
        self.item: Item | None = None

    def link_room(self, room, direction: str):
        """
        Links this room to other in <direction> direction
        """
        if direction not in ["north", "south", "east", "west"]:
            raise ValueError("Direction must be one of the following:"
                             "north, south, east or west")
        opposite = {"north": "south",
                    "south": "north",
                    "east": "west",
                    "west": "east"}
        self.links[direction] = room
        room.links[opposite[direction]] = self

    def display_details(self):
        """
        Prints a details about the room
        """
        print(self.name)
        print('-' * 20)
        print(self.description)
        for direction, room in self.links.items():
            print(f"The {room.name} is {direction}")
        if self.character is not None:
            self.character.display_details()
        if self.item is not None:
            self.item.display_details()

    def move(self, direction):
        """
        Moves a character in a direction
        """
        if direction in self.links:
            return self.links[direction]
        else:
            print("There is nothing there...")
            return self

    def talk(self):
        """
        Provides a conversation in current location
        """
        if self.character is not None:
            self.character.talk()

    def has_enemy(self) -> bool:
        """
        Checks if there is an enemy in the location
        """
        return isinstance(self.character, Enemy)

    def fight(self, item: Item) -> bool:
        """
        Initiates a fight in current location
        """
        if not isinstance(self.character, Enemy):
            raise ValueError("This room has no enemy")
        return self.character.fight(item)


class LockedRoom(Room):
    """
    Represents a room that requires something to walk in
    """

    def __init__(self, name: str, description: str, key: KeyItem):
        super().__init__(name, description)
        self.key = key
        self.unlocked = False

    def display_details(self):
        """
        Prints a details about the room
        """
        print(self.name)
        print('-' * 20)
        print(self.description)
        for direction, room in self.links.items():
            print(f"The {room.name} is {direction}")
        if self.unlocked:
            if self.character is not None:
                self.character.display_details()
            if self.item is not None:
                self.item.display_details()
        else:
            print("This location is locked now")

    def talk(self):
        """
        Represents a conversation in a locked room
        """
        if self.unlocked:
            super().talk()
        else:
            print("This location is locked now")

    def has_enemy(self) -> bool:
        if self.unlocked:
            return super().has_enemy()
        return False

    def fight(self, item: Item) -> bool:
        if self.unlocked:
            return super().fight(item)
        else:
            print("This location is locked now")
            return False


def setup() -> tuple[Room, Boss]:
    badge = ExchangeableItem("badge", 'A shit of paper with a name Peter on it')
    lens = ExchangeableItem('lens', "A piece of curved glass "
                                    "laying on one of the shells")
    card = KeyItem("card", "A plastic card. Very similar to a bank one")
    bread = Item('bread', 'A piece of dry bread')
    broom = Item('broom', 'A very old but definitely recently used broom')

    street = Room("Street", "You've just arrived to an old styled house, that "
                            "is popular among tourists for its authenticity")
    hallway1 = Room("Hallway", "You entered a long hallway "
                               "that seems to be endless")
    dining_room = Room('Dining room', "You entered a dining room with a "
                                      "massive table placed in the center")
    kitchen = Room('Kitchen', "You entered an old fashioned kitchen with a lot "
                              "of cutlery scattered everywhere")
    antechamber = Room('Antechamber', "You entered a room with an old wardrobe")
    hallway2 = Room('Hallway', "You are still going through a long hallway")
    bedroom = Room('Bedroom', "You can see a huge old bed an owner was "
                              "sleeping om")
    bathroom = Room("Bathroom", "A simple a little bit decorated bathroom. "
                                "Nothing special")
    cabinet = Room('Cabinet', "A room that used to be a workplace")
    strong_room = LockedRoom('Strong room', 'A safe with a lot of jewelry left '
                                            'from previous owner', card)

    street.link_room(hallway1, 'north')
    hallway1.link_room(dining_room, 'west')
    dining_room.link_room(kitchen, 'north')
    hallway1.link_room(antechamber, 'east')
    hallway1.link_room(hallway2, 'north')
    hallway2.link_room(bedroom, 'east')
    bedroom.link_room(bathroom, 'north')
    hallway2.link_room(cabinet, 'north')
    cabinet.link_room(strong_room, 'west')

    cabinet.item = broom
    kitchen.item = bread
    antechamber.item = lens

    reporter = Friend('reporter', 'His company asked him to make an article '
                                  'about local sightseeing', lens, badge)
    guide = Friend("guide", "A person who really loves his job and can tell "
                            "anyone everything about this place", badge, card)
    homeless = Enemy('homeless', "An old person hold on you and murmurs "
                                 "something too quite too hear without "
                                 "listening attentively")
    tourist = Enemy('tourist', 'A young teenager that is constantly goes '
                               'through the red tape and touching '
                               'old furniture')
    scrub_woman = Boss('scrubwoman', 'Furious cleaner that was cleaning a safe '
                                     'before your appearance', 2)

    street.character = homeless
    hallway1.character = guide
    dining_room.character = tourist
    bathroom.character = reporter
    strong_room.character = scrub_woman

    reporter.conversation = "Ah... Hello! Imagine, I've come here from the " \
                            "opposite part of the city, and only here I " \
                            "realized that it is something wrong with my camera"
    guide.conversation = "Hi, I'm Peter! Do you want to " \
                         "know more about this place?"
    homeless.conversation = "Young man can you please help me?"
    tourist.conversation = "What? NO! I definitely didn't touched that " \
                           "thing! And even if so, you can do nothing about it"
    scrub_woman.conversation = "How dare you to came in?!! I've even placed " \
                               "a sign saying that cleaning in progress!"

    homeless.weakness = bread
    tourist.weakness = badge
    scrub_woman.weakness = broom

    return street, scrub_woman


def main():
    backpack: dict[str, Item] = {}
    dead = False
    current_room, boss = setup()

    while not dead and not boss.defeated:

        current_room.display_details()
        command = input("> ")

        if command in ["north", "south", "east", "west"]:
            # Move in the given direction
            current_room = current_room.move(command)
        elif command == "talk":
            # Talk to the inhabitant - check whether there is one!
            current_room.talk()
        elif command == "fight":
            if current_room.has_enemy():
                # Fight with the inhabitant, if there is one
                print("What will you fight with?")
                fight_with = input("> ")

                # Do I have this item?
                if fight_with in backpack:
                    dead = current_room.fight(backpack[fight_with])
                    current_room.character = None
                else:
                    print("You don't have a " + fight_with)
            else:
                print("There is no one here to fight with")
        elif command == "take":
            cur_item: Item | None = current_room.item
            if cur_item is not None:
                print("You put the " + cur_item.name + " in your backpack")
                backpack[cur_item.name] = cur_item
                current_room.item = None
            else:
                print("There's nothing here to take!")
        elif command == "use":
            print("Which item do you want to use?")
            item_to_use = input("> ")
            if item_to_use in backpack:
                if backpack[item_to_use].use(current_room):
                    del backpack[item_to_use]
            else:
                print("You don't have a " + item_to_use)
        elif command == "backpack":
            for item in backpack:
                print(item)
        else:
            print("I don't know how to " + command)
        print("\n")

    if dead:
        print("Unfortunately, you lost. But you still can try one more time")
    else:
        print("Congratulations!! You have won the game!")
