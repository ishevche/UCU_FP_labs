#!/usr/bin/python
# -*- coding: utf-8 -*-
from logging import DEBUG, debug, getLogger


def parse_field_info():
    field_info = input()
    debug(f"Description of the field: {field_info}")
    field_info = field_info.split()
    height = int(field_info[1])
    return height


def parse_field(height: int):
    board = []
    for iterator in range(height + 1):
        row = input()
        debug(f"Field: {row}")
        if row[0] != " ":
            board.append(list(row.split()[1]))
    return board


def parse_figure():
    piece = []
    piece_inf = input()
    debug(f"Piece: {piece_inf}")
    height = int(piece_inf.split()[1])
    for _ in range(height):
        row = input()
        debug(f"Piece: {row}")
        piece.append(list(row))
    return piece


def parse_info_about_player():
    player_info = input()
    debug(f"Info about the player: {player_info}")
    return 1 if "p1 :" in player_info else 2


def cut_figure(figure):
    horizontal_shift = 0
    vertical_shift = 0
    while True:
        if figure[0] == ["."] * len(figure[0]):
            figure = figure[1:]
            vertical_shift += 1
        else:
            break
    while True:
        if figure[-1] == ["."] * len(figure[-1]):
            figure = figure[:-1]
        else:
            break
    while True:
        remove_status = True
        for row in figure:
            if row[0] != '.':
                remove_status = False
                break
        if remove_status:
            for iterator, row in enumerate(figure):
                figure[iterator] = row[1:]
            horizontal_shift += 1
        else:
            break
    while True:
        remove_status = True
        for row in figure:
            if row[-1] != '.':
                remove_status = False
                break
        if remove_status:
            for iterator, row in enumerate(figure):
                figure[iterator] = row[:-1]
        else:
            break
    return figure, (vertical_shift, horizontal_shift)


def find_positions(field, figure, shifts, char, enemy):
    coordinates = []
    for row_num in range(len(field) - len(figure) + 1):
        for column_num in range(len(field[row_num]) - len(figure[0]) + 1):
            occurrences = 0
            status = True
            for fig_rows_num, figure_rows in enumerate(figure):
                for fig_column_num, element in enumerate(figure_rows):
                    if element == "*":
                        if field[row_num + fig_rows_num] \
                                [column_num + fig_column_num] == char:
                            occurrences += 1
                        elif field[row_num + fig_rows_num] \
                                [column_num + fig_column_num] == enemy:
                            status = False
            if occurrences == 1 and status:
                coordinates.append((row_num - shifts[0],
                                    column_num - shifts[1]))
    return coordinates


def find_enemies(enemy, field):
    enemies = []
    for row_num, row in enumerate(field):
        for column_num, element in enumerate(row):
            if element == enemy:
                enemies.append((row_num, column_num))
    return enemies


def find_best(positions, enemies, figure, shift):
    fig_positions = []
    for row_num, row in enumerate(figure):
        for column_num, element in enumerate(row):
            if element == "*":
                fig_positions.append((row_num + shift[0],
                                      column_num + shift[1]))
    best = positions[0]
    best_result = 0
    for position in positions:
        near_enemy = 0
        for fig_position in fig_positions:
            element = (position[0] + fig_position[0],
                       position[1] + fig_position[1])
            for enemy in enemies:
                if (abs(element[0] - enemy[0]) == 1 and
                    abs(element[1] - enemy[1]) == 0) or \
                        (abs(element[1] - enemy[1]) == 1 and
                         abs(element[0] - enemy[0]) == 0):
                    near_enemy += 1
                    break
        if near_enemy > best_result:
            best = position
            best_result = near_enemy
    if best_result == 0:
        min_dist = abs(positions[0][0] - enemies[0][0]) + \
                   abs(positions[0][1] - enemies[0][1])
        for position in positions:
            for fig_position in fig_positions:
                element = (position[0] + fig_position[0],
                           position[1] + fig_position[1])
                for enemy in enemies:
                    distance = abs(element[0] - enemy[0]) + \
                               abs(element[1] - enemy[1])
                    if distance < min_dist:
                        min_dist = distance
                        best = position
    debug(f"best: {best}")
    debug(f"first: {positions[0]}")
    return best


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


def play(player):
    while True:
        move = step(player)
        print(*move)


def step(player):
    if player == 1:
        char = "O"
        enemy = "X"
    else:
        char = "X"
        enemy = "O"
    height = parse_field_info()
    field = parse_field(height)
    figure = parse_figure()
    figure, shifts = cut_figure(figure)
    positions = find_positions(field, figure, shifts, char, enemy)
    enemies = find_enemies(enemy, field)
    if not positions:
        return 0, 0
    best_position = find_best(positions, enemies, figure, shifts)
    return best_position


if __name__ == "__main__":
    main()
