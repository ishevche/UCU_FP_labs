"""
crossword.py
Deals with crossword
"""


def read_crossword(path: str) -> list:
    """
    Extract crossword from a file located at <path>
    :param path: file location
    :return: a list of tuples, each of which is a column and row number
    >>> read_crossword("crossword_1_2.txt")[:5]
    [('c', (5, 1)), ('c', (6, 0)), ('u', (6, 1)), ('u', (2, 1)), ('u', (5, 6))]
    """
    answer = []
    with open(path, "r") as input_file:
        input_lines = input_file.read().split('\n')[:-1]
        cur_line = 0
        while cur_line < len(input_lines):
            cur_letter = input_lines[cur_line]
            coordinates = input_lines[cur_line + 1]
            cur_line += 2
            while len(coordinates) > 0:
                column = int(coordinates[0])
                row = int(coordinates[1])
                coordinates = coordinates[2:]
                answer += [(cur_letter, (column, row))]
    return answer


def crossword_words(crossword: list) -> list:
    """
    Returns a list of the smallest words in the crossword
    :param crossword: crossword list
    :return: a list of smallest words
    >>> crossword_words(read_crossword("crossword_1_2.txt"))
    ['cue', 'tra']
    """
    crossword_map = [[' '] * 10 for _ in range(10)]
    for entry in crossword:
        letter, coordinates = entry[0], entry[1]
        crossword_map[coordinates[1]][coordinates[0]] = letter
    smallest_word_length = 100
    vertical_words = []
    for row in range(10):
        for col in range(10):
            if crossword_map[row][col] == ' ':
                continue
            if row == 0 or crossword_map[row - 1][col] == ' ':
                cur_vertical_word = crossword_map[row][col]
                cur_row = row + 1
                while cur_row < 10 and crossword_map[cur_row][col] != ' ':
                    cur_vertical_word += crossword_map[cur_row][col]
                    cur_row += 1
                if len(cur_vertical_word) >= 3:
                    smallest_word_length = min(len(cur_vertical_word),
                                               smallest_word_length)
                    vertical_words += [cur_vertical_word]
            if col == 0 or crossword_map[row][col - 1] == ' ':
                cur_horizontal_word = crossword_map[row][col]
                cur_col = col + 1
                while cur_col < 10 and crossword_map[row][cur_col] != ' ':
                    cur_horizontal_word += crossword_map[row][cur_col]
                    cur_col += 1
                if len(cur_horizontal_word) >= 3:
                    smallest_word_length = min(len(cur_horizontal_word),
                                               smallest_word_length)
    return list(filter(lambda x: len(x) == smallest_word_length,
                       vertical_words))
