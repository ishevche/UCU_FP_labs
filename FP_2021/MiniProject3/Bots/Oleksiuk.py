#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an example of a bot for the 3rd project.
...the best bot to be honest -_-
"""

#from logging import DEBUG, debug, getLogger
from math import sqrt

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

#getLogger().setLevel(DEBUG)


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    inf = input()
    size = inf.split(' ')[1]
    # debug(f"Description of the field: {l}")
    return int(size)


def parse_field(size):
    """
    Parse the field.

    First of all, this function is also responsible for determining the next
    move. Actually, this function should rather only parse the field, and return
    it to another function, where the logic for choosing the move will be.

    Also, the algorithm for choosing the right move is wrong. This function
    finds the first position of _our_ character, and outputs it. However, it
    doesn't guarantee that the figure will be connected to only one cell of our
    territory. It can not be connected at all (for example, when the figure has
    empty cells), or it can be connected with multiple cells of our territory.
    That's definitely what you should address.

    Also, it might be useful to distinguish between lowecase (the most recent piece)
    and uppercase letters to determine where the enemy is moving etc.

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

    param player int: Represents whether we're the first or second player
    """
    field = []
    line = input()
    # debug(f"Field: {l}")
    for _ in range(size):
        line = input()
        # debug(f"Field: {l}")
        field.append(list(line[4:].lower()))
    # debug(f"Field: {field}")
    return field


def parse_figure():
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
    line = input()
    # debug(f"Piece: {line}")
    height = int(line.split()[1])
    cut_piece = []
    counter_cut_row = 0
    first_o = int(line.split()[2][:1])
    last_o = 0
    for i in range(height):
        line = input()
        # debug(line)
        if '*' in line:
            cut_piece.append(list(line))
            lst_line = list(line)
            first = lst_line.index('*')
            lst_line.reverse()
            first_index_in_reversed = lst_line.index('*')
            last = len(lst_line) - 1 - first_index_in_reversed
            if first < first_o:
                first_o = first
            if last > last_o:
                last_o = last
        elif i == counter_cut_row:
            counter_cut_row += 1
    for row in range(len(cut_piece)):
        cut_piece[row] = cut_piece[row][first_o:last_o+1]
    return cut_piece, counter_cut_row, first_o


def find_valid_moves(player, field, piece):
    """
    Return list of coordinates of valid moves and opposite dangerous points
    """
    close_move = []
    counter_closest_opp = 0
    valid_move = []
    opp_good_pos = []
    hole = []
    your_symb = "o" if player == 1 else "x"
    opp_symb = "o" if player == 2 else "x"
    piece_height = len(piece)
    piece_width = len(piece[0])
    for row in range(len(field) - piece_height + 1):
        for column in range(len(field[0]) - piece_width + 1):

            if field[row][column] == opp_symb:
                around_symb = []
                for i in [row - 1, row + 1]:
                    for j in [column - 1, column + 1]:
                        if 0 <= i < len(field) and 0 <= j < len(field[0]):
                            around_symb.append(field[i][j])
                if '.' in around_symb:
                    opp_good_pos.append([row, column])

            counter_opp = 0
            changed_pos = []
            my_changed = []
            put_figure = []
            for p_row in range(piece_height):
                for p_column in range(piece_width):
                    if piece[p_row][p_column] != '.':
                        changed_pos.append(field[row + p_row][column + p_column])
                        put_figure.append([row + p_row, column + p_column])
                        if field[row + p_row][column + p_column] == your_symb:
                            my_changed = [row + p_row, column + p_column]
                    else:
                        if field[row + p_row][column + p_column] == opp_symb:
                            counter_opp += 1

            if changed_pos.count(opp_symb) == 0 and changed_pos.count(your_symb) == 1:
                valid_move.append([row, column])
                try:
                    if field[my_changed[0]][my_changed[1] - 1] == field[
                        my_changed[0] + 1][my_changed[1]] == '.' and field[my_changed[0] + 1][
                            my_changed[1] - 1] == your_symb:
                        if ([my_changed[0], my_changed[1] - 1] in put_figure) or (
                                [my_changed[0] + 1, my_changed[1]] in put_figure):
                            hole = [row, column]
                    if field[my_changed[0]][my_changed[1] + 1] == field[
                        my_changed[0] + 1][my_changed[1]] == '.' and field[my_changed[0] + 1][
                            my_changed[1] + 1] == your_symb:
                        if ([my_changed[0], my_changed[1] + 1] in put_figure) or (
                                [my_changed[0] + 1, my_changed[1]] in put_figure):
                            hole = [row, column]
                except IndexError:
                    pass

                if counter_opp > counter_closest_opp:
                    close_move = [row, column]
                    counter_closest_opp = counter_opp
    # debug(f'close{close_move}')
    # debug(f'valid moves: {valid_move}')
    if valid_move:
        return valid_move, opp_good_pos, close_move, hole
    print(valid_move[0])


def define_root(field, piece, valid_moves, opp_good_pos, close_move, hole):
    """
    Function define best move
    """
    abss = 1
    coordinate = []
    length = -10
    if hole:
        return hole
    if opp_good_pos:
        for j in [0, len(field[0]) - 1]:
            for i in range(len(field)):
                if field[i][j] == '.':
                    if j == 0 and (i in range(int(len(field) / 2))):
                        closest_yo = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , valid_moves)))
                        closest_op = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , opp_good_pos)))
                        diff = closest_op - closest_yo
                        if abss > diff > length:
                            length = diff
                            coordinate = [i, j]
                    elif j == 0 and i >= int(len(field) / 2):
                        closest_yo = min(
                            list(map(
                                lambda x: sqrt((int(x[0] + len(piece)) - i) ** 2 + (int(x[1]) - j) ** 2)
                                , valid_moves)))
                        closest_op = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , opp_good_pos)))
                        diff = closest_op - closest_yo
                        if abss > diff > length:
                            length = diff
                            coordinate = [i, j]
                    elif j == (len(field[0]) - 1) and (i in range(int(len(field) / 2))):
                        closest_yo = min(list(map(
                            lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) + len(piece[0]) - j) ** 2)
                            , valid_moves)))
                        closest_op = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , opp_good_pos)))
                        diff = closest_op - closest_yo
                        if abss > diff > length:
                            length = diff
                            coordinate = [i, j]
                    else:
                        closest_yo = min(list(map(lambda x: sqrt(
                            (int(x[0] + len(piece)) - i) ** 2 + (int(x[1]) + len(piece[0]) - j) ** 2),
                                                  valid_moves)))
                        closest_op = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , opp_good_pos)))
                        diff = closest_op - closest_yo
                        if abss > diff > length:
                            length = diff
                            coordinate = [i, j]
        for i in [0, len(field) - 1]:
            for j in range(1, len(field[0]) - 2):
                if field[i][j] == '.':
                    if i == 0 and (j in range(int(len(field[0]) / 2))):
                        closest_yo = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , valid_moves)))
                        closest_op = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , opp_good_pos)))
                        diff = closest_op - closest_yo
                        if 0.5 > diff > length:
                            length = diff
                            coordinate = [i, j]
                    elif i == 0 and j >= int(len(field[0]) / 2):
                        closest_yo = min(list(map(
                            lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) + len(piece[0]) - j) ** 2)
                            , valid_moves)))
                        closest_op = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , opp_good_pos)))
                        diff = closest_op - closest_yo
                        if abss > diff > length:
                            length = diff
                            coordinate = [i, j]
                    elif i == (len(field) - 1) and (j in range(int(len(field[0]) / 2))):
                        closest_yo = min(list(map(
                            lambda x: sqrt((int(x[0] + len(piece)) - i) ** 2 + (int(x[1]) - j) ** 2)
                            , valid_moves)))
                        closest_op = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , opp_good_pos)))
                        diff = closest_op - closest_yo
                        if abss > diff > length:
                            length = diff
                            coordinate = [i, j]
                    else:
                        closest_yo = min(list(map(lambda x: sqrt(
                            (int(x[0] + len(piece)) - i) ** 2 + (int(x[1]) + len(piece[0]) - j) ** 2)
                                                  , valid_moves)))
                        closest_op = min(
                            list(map(lambda x: sqrt((int(x[0]) - i) ** 2 + (int(x[1]) - j) ** 2)
                                     , opp_good_pos)))
                        diff = closest_op - closest_yo
                        if abss > diff > length:
                            length = diff
                            coordinate = [i, j]
        # debug(f'coor: {coordinate}')

        if coordinate:
            root = lambda x: sqrt((x[0] - coordinate[0]) ** 2 + (x[1] - coordinate[1]) ** 2)
            best_move = sorted(valid_moves, key=lambda value: root(value))[0]
            return best_move
        if close_move:
            return close_move

    lengths = list(map(lambda x: sqrt((int(x[0]) + len(piece) / 2 - len(field) / 2) ** 2 + (
            int(x[1]) + len(piece[0]) / 2 - len(field[0]) / 2) ** 2), valid_moves))
    index_min_lenght = lengths.index(min(lengths))
    return valid_moves[index_min_lenght]


def step(player: int):
    """
    Perform one step of the game.
    """
    size = parse_field_info()
    field = parse_field(size)
    piece_inf = parse_figure()
    cut_piece = piece_inf[0]
    change_row = piece_inf[1]
    change_column = piece_inf[2]
    information = find_valid_moves(player, field, cut_piece)
    valid_moves = information[0]
    opp_good_pos = information[1]
    close_move = information[2]
    hole = information[3]
    best_move = define_root(field, cut_piece, valid_moves, opp_good_pos, close_move, hole)
    best_move[0] -= change_row
    best_move[1] -= change_column
    return best_move


def play(player: int):
    """
    Main game loop.
    """
    while True:
        move = step(player)
        print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    # debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def main():
    """
    Main function
    """
    player = parse_info_about_player()
    try:
        play(player)
    except IndexError:
        pass
        #debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
