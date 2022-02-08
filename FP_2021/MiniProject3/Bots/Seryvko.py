#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Project 3"""
import sys


def parse_info_about_player():
    """
    This function parses the info about the player:

        It can look like this:

        $$$ exec p2 : [./player1.py]
    """
    i = input()
    return 1 if "p1 :" in i else 2


def parse_field_info():
    """
    Parse the info about the field:

        However, the function doesn't do anything with it. Since the height of the field is
        hard-coded later, this bot won't work with maps of different height.

        The input may look like this:

        Plateau 15 17:
    """
    line = input()
    return line.split()[1], line.split()[2][:-1]


def parse_field(size):
    """ Parse the field:

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

        :param player int: Represents whether we're the first or second player
        """
    lst = []
    for i in range(int(size[0])+1):
        line = input()
        if i != 0:
            lst.append(list(line)[4:])
    return lst


def parse_figure():
    """
    Parse the figure:

        The function parses the height of the figure (maybe the width would be
        useful as well), and then reads it.
        It would be nice to save it and return for further usage.

        The input may look like this:

        Piece 2 2:
        **
        ..
    """
    line = input()
    figure = []
    height = int(line.split()[1])
    width = int(line.split()[2][:-1])
    counter = 0
    for _ in range(height):
        line = input()
        if counter != 0:
            if '*' in line:
                counter += 1
                figure.append(list(line.rstrip('.')))
        else:
            if '*' in line:
                counter += 1
            figure.append(list(line.rstrip('.')))

    counter = len(max(figure, key=len))
    for i in range(len(figure)):
        for _ in range(counter-len(figure[i])):
            figure[i].append('.')
    height = len(figure)
    width = len(figure[0])
    return height, width, figure


def step(player):
    """
    Perform one step of the game:

         :param player int: Represents whether we're the first or second player
    """

    size = parse_field_info()
    field = parse_field(size)

    move_list = []
    height, width, figure = parse_figure()
    for i in range(0, len(field)-height+1):
        lst = []
        for j in range(0, len(field[i])-width+1):
            checker = None
            for k in range(height):
                if player == 1:
                    if 'O' in field[i+k][j:j+width] or 'o' in field[i+k][j:j+width]:
                        lst.append((field[i+k][j:j+width], i, j))
                        checker = True
                    else:
                        lst.append((field[i+k][j:j+width], i, j))
                        if checker is None:
                            checker = False
                else:
                    if 'X' in field[i+k][j:j+width] or 'o' in field[i+k][j:j+width]:
                        lst.append((field[i+k][j:j+width], i, j))
                        checker = True
                    else:
                        lst.append((field[i+k][j:j+width], i, j))
                        if checker is None:
                            checker = False
            if checker:
                move_list.append(lst)
            lst = []
    counter_same = 0
    deletion_list = []
    for i in range(len(move_list)):
        figure_coord = 0
        for j in range(len(move_list[i])):
            for k in range(len(move_list[i][j][0])):
                if player == 1:
                    if move_list[i][j][0][k] in 'Oo' and figure[figure_coord][k] == '*':
                        counter_same += 1
                    if move_list[i][j][0][k] in 'Xx' and figure[figure_coord][k] == '*':
                        deletion_list.append(move_list[i])
                else:
                    if move_list[i][j][0][k] in 'Xx' and figure[figure_coord][k] == '*':
                        counter_same += 1

                    if move_list[i][j][0][k] in 'Oo' and figure[figure_coord][k] == '*':
                        deletion_list.append(move_list[i])
            figure_coord += 1
        if counter_same == 1:
            pass
        else:
            deletion_list.append(move_list[i])

        counter_same = 0
    move_list = [i for i in move_list if i not in deletion_list]
    center = (height//2, width//2)
    move_list = sorted(move_list, key=lambda x: (x[0][1]-center[0] if x[0][1] > center[0]
                                                 else x[0][1]+center[0], x[0][2]+center[1]
                                                 if x[0][2] > center[1] else x[0][2]-center[1]))
    if len(move_list) != 0:
        move = (move_list[0][0][1], move_list[0][0][2])
    else:
        return (0, 0)
    return move


def play(player: int):
    """
    Main game loop:

        :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        print(*move)


def main():
    """
    Run the game.
    """
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        print("Cannot get input. Seems that we've lost ):", file=sys.stderr)


if __name__ == "__main__":
    main()
