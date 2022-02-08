#!/usr/bin/env python

# from logging import DEBUG, debug, getLogger
from math import hypot

# getLogger().setLevel(DEBUG)

previous_position = [None]

def parse_field_info() -> tuple:
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    field = input()

    #debug(f"Description of the field: {field}")

    return tuple(map(int, field[:-1].split()[1:]))


def parse_field(field_size: tuple) -> list:
    """
    Parse the field.

    The input may look like this:

        01234567890123456
    000 .................
    001 .................
    002 .................
    003 .................
    004 .................
    005 .................
    006 .................
    007 ..O..............
    008 ..OOO............
    009 .................
    010 .................
    011 .................
    012 ..............X..
    013 .................
    014 .................

    The output is just a list of lists of all the cells in the field.
    """
    input()

    field = [list(input()[4:]) for i in range(1, field_size[0]+1)]

    #debug(field)

    return field


def parse_figure() -> tuple:
    """
    Parse the figure.

    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **
    ..
    """
    piece_dimensions = tuple(map(int, input()[:-1].split()[1:]))
    #debug(f"Piece: {piece_dimensions}")

    piece = []

    for index in range(piece_dimensions[0]):
        line = input()
        #debug(f"Piece: {line}")
        piece.append(line)

    return piece, piece_dimensions


def step(player: int, field_previous: list, previous_position) -> tuple:
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    field_size = parse_field_info()

    field = parse_field(field_size)

    piece = parse_figure()

    offsets = crop_figure(piece[0], piece[1])

    #debug(offsets)

    possible_moves = find_possible_moves(player, piece[0], piece[1], field, field_size, offsets)

    move = pick_best_move(player, possible_moves, field, field_previous, field_size, offsets, previous_position, piece[1])

    return move, field


def find_possible_moves(player: int, piece: list, piece_dimensions: tuple, field: list, field_dimensions: tuple, offsets: tuple) -> list:
    """
    Finds all the places where a piece can be placed.
    The offsets argument is used to account for possible placements in the negative coordinates
    (If the piece is offset to the right and/or bottom);
    Or for cases when only the empty part of the piece is over the border
    (If the piece is offset to the left and/or up)
    Returns a list of tuples containing possible coordinates.
    """

    friendly_piece, enemy_piece = ("O", "X") if player==1 else ("X", "O")
    #debug(friendly_piece + enemy_piece)

    possible_moves = []

    for row in range(-offsets[0], field_dimensions[0]-piece_dimensions[0]+offsets[1]+1):
        for column in range(-offsets[2], field_dimensions[1]-piece_dimensions[1]+offsets[3]+1):

            overlap = 0

            for piece_row in range(offsets[0], piece_dimensions[0]-offsets[1]):
                for piece_column in range(offsets[2], piece_dimensions[1]-offsets[3]):

                    if field[row+piece_row][column+piece_column] == friendly_piece\
                            and piece[piece_row][piece_column] == "*":
                        overlap+=1

                    elif field[row+piece_row][column+piece_column] == enemy_piece\
                            and piece[piece_row][piece_column] == "*":
                        overlap=2
                        break

                else:
                    continue

                break

            if overlap == 1:
                #debug(f"found possible move at {(row, column)}")
                possible_moves.append((row, column))

    return possible_moves


def pick_best_move(player: int, possible_moves: list, field: list, field_previous: list, field_dimensions: tuple, offsets: tuple, previous_position, piece_dimensions) -> tuple:
    """
    Picks the position in which the piece would be closest to the enemy's pieces.
    Finds the move for which the distance to the enemy's center of mass is the shortest.
    Returns a tuple of coordinates considered the best move.
    """

    enemy_position = calculate_enemy_position(player, field, field_previous, field_dimensions)

    previous_position = enemy_position if previous_position== None else previous_position

    enemy_movement = (enemy_position[0] - previous_position[0], enemy_position[1] - previous_position[1])

    closest_distance = hypot(field_dimensions[0], field_dimensions[1])
    piece_center = ((offsets[0]+piece_dimensions[0]-offsets[1])/2, (offsets[2]+piece_dimensions[0]-offsets[3])/2)

    best_move = (0, 0)

    for move in possible_moves:

        distance = hypot(move[0] - enemy_position[0] - enemy_movement[0] + piece_center[0], move[1] - enemy_position[1] - enemy_movement[1] + piece_center[1])

        if distance<closest_distance:

            closest_distance = distance
            best_move = move

    previous_position = enemy_position

    return best_move

def calculate_enemy_position(player: int, field: list, field_previous: list, field_dimensions: tuple) -> tuple:
    """
    Calculates the center of mass of all enemy positions via arithmetic mean.
    Returns a the coordinates of the center of mass.
    """
    enemy_piece = "X" if player==1 else "O"

    row_count = 0
    row_sum = 0

    col_count = 0
    col_sum = 0

    field_is_empty = field_previous==[]

    for row in range(field_dimensions[0]):
        for column in range(field_dimensions[1]):
            if field[row][column] == enemy_piece:

                if field_is_empty:
                    # debug("fields are equal. counting piece")
                    row_count += 1
                    col_count += 1
                    row_sum += row
                    col_sum += column

                elif field[row][column] != field_previous[row][column]:
                    # debug("piece is differrent from last field")
                    row_count += 1
                    col_count += 1
                    row_sum += row
                    col_sum += column

    return row_sum/row_count if row_count!=0 else 0,\
        col_sum/col_count if col_count!=0 else 0


def crop_figure(piece: list, piece_dimensions: tuple) -> tuple:
    """
    The bigger figures can usually be cropped quite significantly.
    This function takes a piece and its dimensions and returns the offset to which it may be cropped.
    For a piece like the following the output would be (9, 2, 2, 8). This is used in find_possible_moves
    to account for possible negative placements and pieces reaching over the map border.
    ...............
    ...............
    ...............
    ...............
    ...............
    ...............
    ...............
    ...............
    ...............
    .....**........
    .....**........
    ..****.........
    .....*.........
    ...............
    ...............
    """
    top_offset = 0
    bottom_offset = 0
    left_offset = 0
    right_offset = 0
    final_row = 0
    final_col = 0

    for row in range(piece_dimensions[0]):
        if "*" not in piece[row]:
            top_offset += 1
        else:
            final_row = row
            break

    for row in range(final_row+1, piece_dimensions[0]):
        if "*" not in piece[row]:
            bottom_offset += 1

    for column in range(piece_dimensions[1]):
        if "*" not in (piece[row][column] for row in range(piece_dimensions[0])):
            left_offset += 1
        else:
            final_col = column
            break

    for column in range(final_col+1, piece_dimensions[1]):
        if "*" not in (piece[row][column] for row in range(piece_dimensions[0])):
            right_offset += 1

    return top_offset, bottom_offset, left_offset, right_offset


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    field = []

    previous_position = None

    while True:
        move, field = step(player, field, previous_position)
        print(*move)


def parse_info_about_player() -> int:
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    #debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def main() -> None:
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        pass
        #debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
