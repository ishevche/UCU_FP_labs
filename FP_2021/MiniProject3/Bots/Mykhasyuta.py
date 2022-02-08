#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Working bot with some logics
    By Maksym Mykhasyuta
"""

from math import sqrt
from logging import DEBUG, debug, getLogger

getLogger().setLevel(DEBUG)


def parse_field_info():
    """
    Parses the info about the field
    """

    l = input().split()
    return int(l[1]), int(l[2][:-1])


def parse_field(pf_info):
    """
    Function that parses the field
    """

    ans = []
    l = input()
    for _ in range(pf_info[0]):
        l = input()
        ans.append(l.split()[-1].strip())
    return ans


def find_borders(lst):
    """
    Finds all positions that are not '.'
    """

    ans = []
    for i, line in enumerate(lst):
        for j, elem in enumerate(line):
            if elem != '.':
                if elem == 'O' or elem == 'o':
                    ans.append((1, i, j))
                elif elem == 'X' or elem == 'x':
                    ans.append((2, i, j))
                else:
                    ans.append((0, i, j))
    return ans


def find_best_route(possible, enemy):
    """
    Finds the best route
    Main logic is located here
    but can be useful in making better logics
    """

    ans = set()
    for i in possible:
        for j in enemy:
            ans.add((sqrt((i[0] - j[0]) * (i[0] - j[0]) +
                    (i[1] - j[1]) * (i[1] - j[1])), i, j))
    for elem in sorted(ans, key=lambda x: x[0]):
        return elem[1]
    pass


def possible_answer(board, figure, player, pf_info, parse_f):
    """
    Finds possible answer
    uses find_best_route function
    If there is no place available to place
    the figure, returns False
    """

    ans = set()

    rc = parse_f[2] - parse_f[3][1] - 1
    lc = -parse_f[3][0]
    bc = parse_f[1] - parse_f[3][3] - 1
    tc = -parse_f[3][2]

    # debug(f'  R --->>> {rc}')
    # debug(f'  L --->>> {lc}')
    # debug(f'  B --->>> {bc}')
    # debug(f'  T --->>> {tc}')

    board_player = set()
    board_enemy = set()
    for elem in board:
        if elem[0] == player:
            board_player.add((elem[1], elem[2]))
        else:
            board_enemy.add((elem[1], elem[2]))
    board_union = board_player.union(board_enemy)
    # debug(f'   ===>>> {board_enemy}')
    for i in range(tc, pf_info[0] + bc - parse_f[1] + 1):
        for j in range(lc, pf_info[1] + rc - parse_f[2] + 1):
            new_fig = [(elem[1]+i, elem[2]+j) for elem in figure]
            pre_and = set(new_fig) & set(board_player)
            if len(pre_and) == 1:
                if len(pre_and & board_union) == 1:
                    a = list(pre_and)[0]
                    board_union.remove(a)
                if set(new_fig) & set(board_union) == set():
                    ans.add((i, j))
    if len(ans) != 0:
        return find_best_route(ans, board_enemy)
    return False


def parse_figure():
    """
    Parses the figure
    """

    l = input()
    spl = l.split()

    height = int(spl[1])
    width = int(spl[2][:-1])
    piece = []
    max_l = width
    max_r = 0
    max_t = height
    max_b = 0
    for i in range(height):
        l = input()
        pre_piece = []
        for index, elem in enumerate(l):
            if elem == '*':
                if index > max_r:
                    max_r = index
                if index < max_l:
                    max_l = index
                if i > max_b:
                    max_b = i
                if i < max_t:
                    max_t = i
            pre_piece.append(elem)
        piece.append(pre_piece)
    return piece, height, width, [max_l, max_r, max_t, max_b]


def step(player: int):
    """
    Performs one step of the game
    """

    pre_move = None
    pf_info = parse_field_info()
    pre_move = parse_field(pf_info)
    parse_f = parse_figure()
    figure = find_borders(parse_f[0])
    board = find_borders(pre_move)
    ans = possible_answer(board, figure, player, pf_info, parse_f)
    return ans


def play(player: int):
    """
    Main game loop
    """

    while True:
        move = step(player)
        print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player
    """

    i = input()
    return 1 if "p1 :" in i else 2


def main():
    """
    Main function
    """

    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
