"""
Game objects
"""


class Character:
    """
    Represents a game character
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.conversation = None

    def set_conversation(self, conversation: str):
        """
        Writes down a conversation of the character
        """
        self.conversation = conversation

    def describe(self):
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
    
    defeated = 0

    def set_weakness(self, weakness: str):
        """
        Writes down a weakness of the enemy
        """
        self.weakness = weakness

    def fight(self, weapon: str) -> bool:
        """
        Represents a fight
        """
        if weapon == self.weakness:
            Enemy.defeated += 1
            print(f'You fend {self.name} off with the {weapon}')
            return True
        else:
            print(f"{self.name} crushes you, puny adventurer!")
            return False
        
    @staticmethod
    def get_defeated() -> int:
        """
        Returns amount of defeated enemies
        """
        return Enemy.defeated


class Friend(Character):
    """
    Represents a friend
    """


class Item:
    """
    Represents an item that can be used to fight
    """

    def __init__(self, name: str):
        self.name = name
        self.description = None

    def set_description(self, description: str):
        """
        Writes down a description of the item
        """
        self.description = description

    def describe(self):
        """
        Prints a details about the item
        """
        print(f'The [{self.name}] is here - {self.description}')

    def get_name(self) -> str:
        """
        Returns item name
        """
        return self.name


class Room:
    """
    Represents a room to walk in
    """

    def __init__(self, name: str):
        self.name = name
        self.links = {}
        self.description = None
        self.character = None
        self.item = None

    def set_description(self, description: str):
        """
        Writes down a description of the room
        """
        self.description = description

    def link_room(self, room, direction: str):
        """
        Links this room to other in <direction> direction
        """
        if direction not in ["north", "south", "east", "west"]:
            raise ValueError("Direction must be one of the following:"
                             "north, south, east or west")
        self.links[direction] = room

    def set_character(self, character: Character):
        """
        Writes down a character located in this room
        """
        self.character = character

    def set_item(self, item: Item):
        """
        Writes down an item located in this room
        """
        self.item = item

    def get_details(self):
        """
        Prints a details about the room
        """
        print(self.name)
        print('-'*20)
        print(self.description)
        for direction, room in self.links.items():
            print(f"The {room.name} is {direction}")

    def get_character(self) -> Character:
        """
        Returns a character located in the room
        """
        return self.character

    def get_item(self) -> Item:
        """
        Returns an item located in the room
        """
        return self.item

    def move(self, direction):
        """
        Moves a character in a direction
        """
        if direction in self.links:
            return self.links[direction]
        else:
            return self
