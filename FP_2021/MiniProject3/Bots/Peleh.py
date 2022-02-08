#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    l = input()
    debug(f"Description of the field: {l}")
    return int(l.split()[1]), int(l.split()[2][:-1])


def parse_field(player: int, n: int, m: int):
    """
    Parse the field and return the next move.

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
    field = []
    for i in range(n+1):
        l = input()
        if i > 0:
            splitted = l.split()
            if len(splitted) > 1:
                splitted[1] = splitted[1].replace('o', 'O')
                splitted[1] = splitted[1].replace('x', 'X')
                field.append(splitted[1])
            # debug(splitted[1])
    figure = parse_figure(player)
    if player == 1:
        ch_pl = 'O'
        ch_no_pl = 'X'
    else: 
        ch_pl = 'X'
        ch_no_pl = 'O'
    ls1 = []
    ls2 = []
    for i in range(len(field) - len(figure)+1):
        for j in range(len(field[i]) - len(figure[0])+1):
            count = 0
            flag = True
            count_near = 0
            for i2 in range(len(figure)):
                for j2 in range(len(figure[0])):
                    if figure[i2][j2] == ch_pl and field[i+i2][j+j2] == ch_pl:
                        count += 1
                        if j+j2 + 1 < len(field):
                            if field[i+i2][j+j2 + 1] ==  ch_no_pl:
                                count_near+=1
                        if j+j2 - 1 >= 0:
                            if field[i+i2][j+j2 - 1] ==  ch_no_pl:
                                count_near+=1
                        if i+i2 + 1 < len(field):
                            if field[i+i2-1][j+j2] ==  ch_no_pl:
                                count_near+=1
                        if i+i2 - 1 >= 0:
                            if field[i+i2+1][j+j2] ==  ch_no_pl:
                                count_near+=1
                    if figure[i2][j2] == ch_pl and field[i+i2][j+j2] != '.' and field[i+i2][j+j2] == ch_no_pl:
                        flag = False
            if count == 1 and flag == True:
                ls1.append([1000000000, [i, j]])
                ls2.append([count_near, [i, j]])
    if len(ls2) == 0:
        return
    ls2.sort(key = lambda x: x[0])
    if ls2[len(ls2)-1][0] != 0: return ls2[len(ls2)-1][1]
    else:
        for i in range(len(field)):
            for j in range(len(field[i])):
                for k in ls1:
                    k[0] = min(abs(k[1][0]-i)^2 + abs(k[1][1]-j)^2, k[0])
    ls1.sort(key = lambda x: x)
    return ls1[0][1]

    # if len(ls) != 1:
    #     numb = random.randint(0, len(ls) - 1)
    #     return ls[numb]
    # elif len(ls) == 1:
    #     return ls[0]
    # else: 
    #     debug('END')
    #     return


def parse_figure(player):
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
    l = input()
    # debug(f"Piece: {l}")
    figure = []
    height = int(l.split()[1])
    width = int(l.split()[2][:-1])
    for _ in range(height):
        l = input().replace('*', 'O') if player == 1 else input().replace('*', 'X')
        a = []
        for i in range(len(l)):
            a.append(l[i])
        figure.append(a)
        # debug(f"Piece: {l}")
    return figure
    


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    move = None
    a = parse_field_info()
    move = parse_field(player, a[0], a[1])
    return move


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        if move == None:
            debug('Erorr')
        print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
