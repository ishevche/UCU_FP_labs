#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Bot for a game"""


from logging import ERROR
import math
import sys
from logging import DEBUG, debug, getLogger
getLogger().setLevel(DEBUG)


def player_info():
    """Scan info about player

    Returns:
        int: player number
    """
    i = input()
    # debug(f"Info about the player: {i}")
    return 0 if "p1 :" in i else 1


def rule_checker(coord_i, coord_j, enemy_places, my_places, figure):
    """check if coordinates are suitable for the figure

    Args:
        coord_i (int): first coordinate in the field which I check 
        coord_j (int): second coordinate in the field which I check 
        enemy_places (set): set with coordinates of enemy places
        my_places (set): set with coordinates of my places
        figure (set): set with coordinates of figure (stars)

    Returns:
        bool: False if coord is not suitable, ant True if it is
    """
    star_coords = set()
    for i, j in figure:
        star_coords.add((coord_i+i, coord_j+j))
    if star_coords & enemy_places or len(star_coords & my_places) != 1:
        return False
    return True


def places_for_figure(field, figure_coords, enemy_places, my_places, figure_height, figure_length):
    """Scan and choose places which are suitable for the figure

    Args:
        field (list): list of lists with the rows of the field
        figure_coords (set): set with coordinates of figure (stars)
        enemy_places (set): set with coordinates of enemy places
        my_places (set): set with coordinates of my places
        figure_height (int): size of figure
        figure_length (int): size of figure

    Returns:
        set: set with the coords which are suitasble for the figure
    """
    valid_coords = set()
    for i in range(len(field)-figure_height+1):
        for j in range(len(field[0])-figure_length+1):
            if rule_checker(i, j, enemy_places, my_places, figure_coords):
                valid_coords.add((i, j))
    if not valid_coords:
        valid_coords.add((5, 5))
    return valid_coords


def places(player, field):
    """Find places of X or O

    Args:
        player (int): player 0 - if 'O', and 1 - if 'X'
        field (list): list of lists with the rows of the field

    Returns:
        set: set with coordinates of places
    """
    places = set()
    for i in range(len(field)):
        for j in range(len(field[i])):
            if player == 0 and field[i][j] == 'O':
                places.add((i, j))
            if player == 1 and field[i][j] == 'X':
                places.add((i, j))
    return places


def parse_figure(board):
    """Scan figure

    Args:
        board (str): The whole board which input gives

    Returns:
        tuple: tuple, where:
        1. figure_coords (set): set with coordinates of figure (stars)
        2. figure_length (int): length of the figure
    """
    figure_coords = []
    figure = board.split('\n')

    for i in range(len(figure)):
        if figure[i].startswith('Piece'):
            values = figure[i].split()
            figure_length = (int(values[1]), int(values[2][:-1]))
            break
    figure = figure[i+1:]
    for i in range(len(figure)):
        for j in range(len(figure[i])):
            if figure[i][j] == '*':
                figure_coords.append((i, j))
    return figure_coords, figure_length


def parse_field(board):
    """ Scan field

    Args:
        board (str): The whole board which input gives

    Returns:
        List: list of lists with the rows of the field
    """
    new_field = []
    field = board.split('\n')
    field.pop(0)
    for i in range(len(field)):
        if field[i].startswith('Piece'):
            break
        new_field.append(field[i].split()[1])
    return new_field


def read_board():
    """ Read all lines from input

    Returns:
        str: The whole board which input gives
    """
    plateau = input()
    board = plateau
    plateau = plateau.split()
    board_height = int(plateau[1])
    board_width = int(plateau[2][:-1])
    input()
    for i in range(board_height):
        board += '\n'+input()
    piece = input()
    board += '\n'+piece
    piece = piece.split()
    piece_rows = int(piece[1])
    for j in range(piece_rows):
        board += '\n'+input()
    return board


def check_position(my_places, enemy_places):
    """Check position who is higher ('x' or 'o') to help algorythm

    Args:
        enemy_places (set): set with coordinates of enemy places
        my_places (set): set with coordinates of my places

    Returns:
        int: 1 if 'x' is higher and 2 if 'o' is higher
    """
    my_place = my_places.pop()
    enemy_place = enemy_places.pop()
    if my_place[0] >= enemy_place[0]:
        return 1
    else:
        return 0


def find_nearest_to_center(point, sort_places):
    """Find the best point which is nearer to the corner(some point)

    Args:
        point (tuple): coords
        sort_places (list): list of places of valid points for figure

    Returns:
        tuple: point
    """
    min_distance = math.sqrt(
        (sort_places[0][0]-point[0])**2+(sort_places[0][1]-point[1])**2)
    result = sort_places[0]
    for i in range(len(sort_places)):
        distance = math.sqrt(
            (sort_places[i][0]-point[0])**2+(sort_places[i][1]-point[1])**2)
        if distance < min_distance:
            min_distance = distance
            result = sort_places[i]
    return result


I = 0


def best_place(valid_places, field, checker):
    """Makes final decision where to put the figure

    Args:
        valid_places (set): valid point for the figure
        field (list): list of lists with the rows of the field
        checker (int): 1 if 'x' is higher and 2 if 'o' is higher

    Returns:
        tuple: coordinates where to put the figure
    """
    import random
    global I
    if checker == 0:
        sort_places = sorted(valid_places)
        while I != len(field)//2:
            biggest = []
            for i in sort_places:
                if i[0] == sort_places[-1][0]:
                    biggest.append(i)
            I += 1
            return biggest[-1]
        center1 = (len(field), 0)
        center2 = (0, len(field[0]))
        possible = [find_nearest_to_center(
            center1, sort_places), find_nearest_to_center(center2, sort_places)]
        result = random.choice(possible)
        return result
    if checker == 1:
        sort_places = sorted(valid_places)
        while I != len(field)//2:
            biggest = []
            for i in sort_places:
                if i[0] == sort_places[0][0]:
                    biggest.append(i)
            I += 1
            return biggest[0]
        center1 = (len(field), 0)
        center2 = (0, len(field[0]))
        possible = [find_nearest_to_center(
            center1, sort_places), find_nearest_to_center(center2, sort_places)]
        result = random.choice(possible)
        return result


def main():
    try:
        player = player_info()
        k = 1
        while True:
            board = read_board()
            # читання файлу
            field = parse_field(board)
            # only field
            figure = parse_figure(board)

            figure_coords = figure[0]
            figure_height = figure[1][0]
            figure_length = figure[1][1]
            # only figure
            my_places = places(player, field)
            enemy_places = places(not player, field)
            # enemy places
            valid_places = places_for_figure(
                field, figure_coords, enemy_places, my_places, figure_height, figure_length)
            if k == 1:
                checker = check_position(my_places, enemy_places)
                k = 2
            best_place_for_figure = best_place(valid_places, field, checker)
            if valid_places == set():
                print(*valid_places.pop())
            else:
                print(*best_place_for_figure)
    except EOFError:
        print('The end', file=sys.stderr)


main()
