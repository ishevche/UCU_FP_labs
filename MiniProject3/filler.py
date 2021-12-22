#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module was written to play a filler game
"""
import collections
import re


def main():
    """
    Directs all program flow, contains main cycle
    """
    first_player = get_current_player()
    try:
        while True:
            make_move(first_player)
    except EOFError:
        pass


def get_current_player() -> bool:
    """
    Reads first line and finds the number of player to play
    :return: boolean variable that contains
        True if first and False if second
    """
    start_line = input()
    return 'p1 :' in start_line


def make_move(first_player: bool):
    """
    Main function of the module, that reads field, piece,
    and decides which move to make
    :param first_player: boolean variable
        True - first player
        False - second
    :return: None
    """
    field: list = []
    opponent_cells = read_field(field, first_player)
    for opponent_cell in opponent_cells:
        calculate_distance(field, opponent_cell)
    figure, figure_size, shift = get_piece()
    figure = choose_figure(field, figure, figure_size, first_player)
    print(f'{figure[0] - shift[0]} {figure[1] - shift[1]}')


def read_field(field: list, first_player: bool) -> set:
    """
    Reads a field from standard input
    :param field: variable to write field in
    :param first_player: boolean variable
        True - first player
        False - second
    :return: a set of opponent's cells
    """
    rows, cols = get_size()

    opponent_symbols = 'Xx' if first_player else 'Oo'

    input()  # header skip

    opponent_cells = set()

    for row_idx in range(rows):
        row = input()[4:]
        row_list = []
        for col_idx in range(cols):
            if row[col_idx] == '.':
                row_list.append(-1)
            else:
                row_list.append(row[col_idx].upper())
                if row[col_idx] in opponent_symbols:
                    opponent_cells.add((row_idx, col_idx))
        field.append(row_list)

    return opponent_cells


def get_size() -> tuple:
    """
    Reads standard input, finds out sizes of the following table
    :return: tuple (number of rows, number or cols)
    """
    field_size_str = input()
    rows, cols = re.findall(r'\w+\s+(\d+)\s+(\d+):',
                            field_size_str)[0]

    return int(rows), int(cols)


def calculate_distance(field: list, start: tuple):
    """
    BFS implementation. Calculates shortest distance
    to <start> point for every empty point on the map,
    reached by stepping up, down, right or left,
    without stepping on the filled cells
    :param field: field provided by vm
    :param start: a point a distance to which calculated
    :return: None
    """
    fifo_queue = collections.deque()
    fifo_queue.append(start)
    while fifo_queue:
        row, col = fifo_queue.popleft()
        distance = field[row][col]
        if isinstance(distance, str):
            distance = 0
        neighbors = get_empty_neighbors(field, row, col)
        for new_row, new_col in neighbors:
            if field[new_row][new_col] == -1 or \
                    field[new_row][new_col] > distance + 1:
                field[new_row][new_col] = distance + 1
                fifo_queue.append((new_row, new_col))


def get_empty_neighbors(field, row, col) -> set:
    """
    Returns a set of empty cells that have border in common
    with given
    :param field: field provided by vm
    :param row, col: coordinates of a cell
    :return: set
    """
    possible_answer = {(row + 1, col), (row, col + 1),
                       (row - 1, col), (row, col - 1)}
    answer = set()
    for cell in possible_answer:
        if 0 <= cell[0] < len(field) and 0 <= cell[1] < len(field[cell[0]]):
            if isinstance(field[cell[0]][cell[1]], int):
                answer.add(cell)
    return answer


def get_piece() -> tuple:
    """
    Reads piece table
    :return: tuple (
        figure cells (relative coordinates),
        figure size,
        shift (amount of empty rows and columns in figure)
    """
    rows, cols = get_size()

    min_row, max_row, min_col, max_col = rows - 1, 0, cols - 1, 0
    figure_cells = set()

    for row_idx in range(rows):
        row = input()
        for col_idx in range(cols):
            if row[col_idx] == '*':
                figure_cells.add((row_idx, col_idx))
                min_row = min(min_row, row_idx)
                max_row = max(max_row, row_idx)
                min_col = min(min_col, col_idx)
                max_col = max(max_col, col_idx)

    figure = set()
    for row, col in figure_cells:
        figure.add((row - min_row, col - min_col))
    figure_size = (max_row - min_row, max_col - min_col)
    figure_shift = (min_row, min_col)

    return figure, figure_size, figure_shift


def choose_figure(field, figure, size, first_player) -> tuple:
    """
    Looks through all possible figures and chooses the best one
    :param field: field provided by vm
    :param figure: figure cells
    :param size: figure size
    :param first_player: first_player: boolean variable
        True - first player
        False - second
    :return: relative coordinates - the best position
        for the figure
    """
    min_cost = -1
    best_figure = 0, 0
    for row in range(len(field) - size[0]):
        for col in range(len(field[row]) - size[1]):
            cost = get_cost(field, figure, row, col, first_player)
            if cost < 0:
                continue
            if cost < min_cost or min_cost == -1:
                min_cost = cost
                best_figure = row, col
    return best_figure


def get_cost(field, figure, row, col, first_player) -> int:
    """
    Calculates cost for figure placement
    :param field: field provided by vm
    :param figure: figure cells
    :param row, col: relative coords of figure placement
    :param first_player: first_player: boolean variable
        True - first player
        False - second
    :return: actual cost of placement
    """
    cost = 0
    has_collision = False
    collision_symbol = 'O' if first_player else 'X'

    for figure_row, figure_col in figure:
        actual_row = row + figure_row
        actual_col = col + figure_col
        actual_value = field[actual_row][actual_col]
        if isinstance(actual_value, int):
            if actual_value == -1:
                cost += len(field) * len(field[actual_row])
            else:
                cost += actual_value
        else:
            if has_collision:
                return -1
            if actual_value == collision_symbol:
                has_collision = True
            else:
                return -1

    return cost if has_collision else -1


if __name__ == "__main__":
    main()
