#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bot for the third miniproject
"""

from logging import DEBUG, debug, getLogger
getLogger().setLevel(DEBUG)


def parse_field_info():
    """Parse the info about the field.

    :return: field parameters
    :rtype: tuple
    """
    field_info = input()
    field_info = field_info.split(' ')
    height = int(field_info[1])
    width = int(field_info[2][:-1])
    return height, width


def parse_field(height):
    """Parses the field and saves it

    :param height: height of the field
    :type height: int
    :return: saved field by lines
    :rtype: list of lists
    """
    line = input()
    field = []
    for i in range(1, height+1):
        line = input()
        line = line[4:]
        field.append(line)
    return field


def parse_figure(player):
    """Parses the figure and saves it, replacing start with player's symbol

    :param player: number of the players
    :type player: int
    :return: saved figure by lines
    :rtype: list of lists
    """
    size = input()
    height = int(size.split()[1])
    figure = []
    if player == 1:
        symbol = 'o'
    else:
        symbol = 'x'
    for i in range(height):
        line = input()
        line = list(line)
        for j in range(len(line)):
            if line[j] == '*':
                line[j] = symbol
        line = ''.join(line)
        figure.append(line)
    return figure


def rules_check(field, figure, player, start):
    """Checks if the figure can be placed on the given coordinates

    :param field: game field
    :type field: list
    :param figure: given figure
    :type figure: list
    :param player: number of player
    :type player: int
    :param start: coordinate needed to be checked
    :type start: tuple
    :return: possibility of placing
    :rtype: bool
    """
    symbol = 'o'
    enemy_symbol = 'x'
    if player == 2:
        symbol, enemy_symbol = enemy_symbol, symbol
    f_height = len(figure)
    f_width = len(figure[0])
    intersection = 0
    for i in range(f_height):
        for j in range(f_width):
            if figure[i][j] != '.':
                try:
                    if figure[i][j].lower() == symbol == \
                                    field[i+start[0]][j+start[1]].lower():
                        intersection += 1
                    elif field[i+start[0]][j+start[1]].lower() \
                                    == enemy_symbol:
                        intersection = 2
                except IndexError:
                    intersection = 2
    if intersection == 1:
        return True
    return False


def options(field, figure, player):
    """Cuts the figure if neccessary and finds
    all posible positions to place it on the game field

    :param field: game field
    :type field: list
    :param figure: given figure
    :type figure: list
    :param player: number of player
    :type player: int
    :return: possible options of placing
    :rtype: set
    """
    j_cut = 0
    i_cut = 0
    while True:
        dot_begin = list(filter(lambda x: x[0] == '.', figure))
        if len(dot_begin) == len(figure):
            figure = list(map(lambda x: x[1:], figure))
            j_cut += 1
        else:
            break
    while True:
        dot_begin = list(filter(lambda x: x[-1] == '.', figure))
        if len(dot_begin) == len(figure):
            figure = list(map(lambda x: x[:-1], figure))
        else:
            break
    while True:
        if figure[0] == '.' * len(figure[0]):
            figure = figure[1:]
            i_cut += 1
        else:
            break
    while True:
        if figure[-1] == '.' * len(figure[0]):
            figure = figure[:-1]
        else:
            break
    possible_moves = set()
    for i in range(len(field)):
        for j in range(len(field[0])):
            if rules_check(field, figure, player, (i, j)):
                possible_moves.add((i-i_cut, j-j_cut))
    return possible_moves


def small_found(field, player):
    """Finds coordinates of the figure, placed by enemy last

    :param field: game field
    :type field: list
    :param player: number of player
    :type player: int
    :return: figure's coordinate
    :rtype: tuple
    """
    if player == 1:
        e_symb = 'x'
    else:
        e_symb = 'o'
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == e_symb:
                return i, j
    return False


def distance_count(coord, e_move):
    """Counts the manhetten distance between two points on the field

    :param coord: coordinate of player's point
    :type coord: tuple
    :param e_move: coordinate of enemy's point
    :type e_move: tuple
    :return: distance between the points
    :rtype: int
    """
    if e_move:
        distance = (abs(coord[0] - e_move[0]) + abs(coord[1] - e_move[1]))
        return distance
    return False


def move_choose(field, possible_moves, player):
    """Chooses the best move from possible

    :param field: field of the game
    :type field: list
    :param possible_moves: moves, which are legal
    :type possible_moves: set
    :param player: player's number
    :type player: int
    :return: coordinates of the best move
    :rtype: tuple
    """
    possible_moves = list(possible_moves)
    best = possible_moves[0]
    for coord in possible_moves:
        e_move = small_found(field, player)
        distance = distance_count(coord, e_move)
        if distance and (distance > distance_count(best, e_move)):
            best = coord
    return best


def step(player):
    """
    Perform one step of the game.

    :param player: Represents whether we're the first or second player
    :type player: int
    """
    field_info = parse_field_info()
    height = field_info[0]
    field = parse_field(height)
    figure = parse_figure(player)
    possible_moves = options(field, figure, player)
    if possible_moves == set():
        return ''
    return move_choose(field, possible_moves, player)


def play(player):
    """
    Main game loop.

    :param player: Represents whether we're the first or second player
    :type player: int
    """
    while True:
        move = step(player)
        print(*move)


def parse_info_about_player():
    """Parses the info about the player

    :return: player's number
    :rtype: int
    """
    player_info = input()
    if "exec p1 :" in player_info:
        return 1
    return 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
