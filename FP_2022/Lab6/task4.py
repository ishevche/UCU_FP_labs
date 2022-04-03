class Document:
    def __init__(self):
        self.characters = []
        self.cursor = Cursor(self)
        self.filename = ''

    def insert(self, character):
        if not isinstance(character, Character):
            character = Character(character)
        self.characters.insert(self.cursor.position,
                               character)
        self.cursor.forward()

    def delete(self):
        del self.characters[self.cursor.position]

    def save(self):
        if not self.filename:
            raise NoFileNameException()
        if not ''.join(self.characters):
            raise EmptyFileException()
        f = open(self.filename, 'w')
        f.write(''.join(self.characters))
        f.close()

    @property
    def string(self):
        return "".join((str(c) for c in self.characters))


class Cursor:
    def __init__(self, document):
        self.document = document
        self.position = 0

    def forward(self):
        if self.position == len(self.document.characters) - 1:
            raise EndOfFileException()
        self.position += 1

    def back(self):
        if self.position == 0:
            raise EndOfFileException()
        self.position -= 1

    def home(self):
        while self.document.characters[self.position - 1].character != '\n':
            self.position -= 1
            if self.position == 0:
                # Got to beginning of file before newline
                break

    def end(self):
        while self.position < len(self.document.characters) and \
                self.document.characters[
                    self.position].character != '\n':
            self.position += 1


class Character:
    def __init__(self, character,
                 bold=False, italic=False, underline=False):
        if len(character) != 1:
            raise NotCharacterException()
        self.character = character
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def __str__(self):
        bold = "*" if self.bold else ''
        italic = "/" if self.italic else ''
        underline = "_" if self.underline else ''
        return bold + italic + underline + self.character


class EndOfFileException(Exception):
    pass


class NoFileNameException(Exception):
    pass


class EmptyFileException(Exception):
    pass


class NotCharacterException(Exception):
    pass
