#!/usr/bin/python
# -*- coding: utf-8 -*
# -
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger

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
    line = l.split()
    line_2 = line[2]
    line_2 = line_2[:-1]
    height, length = int(line[1]), int(line_2)
    return height, length


def available_moves(field, figure):
    """
    Parse the figure.
    0 - nothing
    1 - *
    2 - .

    Parsing field
    0 == "."
    1 == friendly element
    2 == opponent element
    """
    available_moves = []
    for cur_hei_field in range(len(field)):
        for cur_len_field in range(len(field[cur_hei_field])):
            counter_1s = 0
            can_take = True
            for cur_hie_figure in range(len(figure)):
                for cur_len_figure in range(len(figure[cur_hie_figure])):
                    if figure[cur_hie_figure][cur_len_figure] == 1:
                        try:
                            if field[cur_hei_field + cur_hie_figure][cur_len_field + cur_len_figure] == 2:
                                can_take = False
                            elif field[cur_hei_field + cur_hie_figure][cur_len_field + cur_len_figure] == 1:
                                counter_1s += 1
                        except IndexError:
                            can_take = False
            if counter_1s == 1 and can_take:
                available_moves.append((cur_hei_field, cur_len_field))
    return available_moves


def parse_field_2(player: int, field_y, field_x: int):
    """
    :param player int: Represents whether we're the first or second player
    """
    """
    Parsing field
    0 == "."
    1 == friendly element
    2 == opponent element
    """
    enemy_fields = set()
    field_list = []
    for i in range(field_y + 1):
        line = input()
        if i == 0:
            continue
        field_list.append([piece.lower() for piece in line.split()[1]])
    for i in range(len(field_list)):
        for j in range(len(field_list[i])):
            if field_list[i][j] == ".":
                field_list[i][j] = 0
            if player == int(1):
                if field_list[i][j] == "o":
                    field_list[i][j] = 1
                elif field_list[i][j] == "x":
                    enemy_fields.add((i, j))
                    field_list[i][j] = 2
            elif player == int(2):
                if field_list[i][j] == "o":
                    field_list[i][j] = 2
                    enemy_fields.add((i, j))
                elif field_list[i][j] == "x":
                    field_list[i][j] = 1
    figure = parse_figure()
    figure, delta_y, delta_x = change_figure(figure)
    move = available_moves(field_list, figure)
    # assert move is not None
    # choose the best move from all available
    if len(move) != 0:
        # min_way, min_ways_amount = find_min_way(move[0][0], move[0][1], enemy_fields, figure)
        best_move = move[0]
        min_ways_record = 1000000
        min_ways_amount_max = 0
        for i in range(1, len(move)):
            #min_way, min_ways_amount = find_min_way(move[i][0], move[i][1], enemy_fields, figure)
            min_way = find_min_way(move[i][0], move[i][1], enemy_fields, figure)
            if min_way < min_ways_record:
                min_ways_record = min_way
                #min_ways_amount_max = min_ways_amount
                best_move = move[i]
            # if min_way == min_ways_record:
            #     if min_ways_amount_max < min_ways_amount:
            #         min_ways_amount_max = min_ways_amount
            #         best_move = move[i]
        best_move = (best_move[0] - delta_y, best_move[1] - delta_x)
        return best_move
    else:
        return -1, -1


def find_min_way(y_pos, x_pos, enemy_fields, figure):
    """
    finds and returns minimal length to enemy's element
    """
    min_way_record: int = 100000
    min_way_amount = 0
    for i in range(len(figure)):
        for j in range(len(figure[i])):
            if figure[i][j] == 1:
                for k in enemy_fields:
                    enemy_y = k[0]
                    enemy_x = k[1]
                    min_way = abs(enemy_y - (y_pos + i)) + abs(enemy_x - (x_pos + j))
                    if min_way < min_way_record:
                        min_way_record = min_way
                        #min_way_amount = 1
                    # elif min_way == min_way_record:
                    #     min_way_amount += 1
    #return min_way_record, min_way_amount
    return min_way_record

def change_figure(figure: list):
    """
    :param figure: input figure
    :return: new figure / old, if we can't change
    >>> change_figure([[2, 2, 2, 2], [2, 2, 2, 1]])
    ([[1]], 1, 3)
    >>> change_figure([[2, 2, 1, 2], [2, 1, 2, 2], [2, 2, 2, 1]])
    ([[2, 1, 2], [1, 2, 2], [2, 2, 1]], 0, 1)
    >>> change_figure([[1, 2, 1, 2], [2, 1, 2, 2], [2, 2, 2, 1]])
    ([[1, 2, 1, 2], [2, 1, 2, 2], [2, 2, 2, 1]], 0, 0)

    """
    delta_y = 0
    delta_x = 0
    number_line = 0
    flag = True
    # delete empty rows from upside
    while True:
        for i in range(len(figure[number_line])):
            if figure[number_line][i] == 1:
                flag = False
                break
        if flag:
            delta_y += 1
            number_line += 1
        else:
            break
    if delta_y != 0:
        del figure[0:delta_y]
    # delete empty columns (starting from left)
    number_colums = 0
    flag = True
    while True:
        for i in range(len(figure)):
            if figure[i][number_colums] == 1:
                flag = False
                break
        if flag:
            delta_x += 1
            number_colums += 1
        else:
            break
    if delta_x != 0:
        for i in range(len(figure)):
            del figure[i][0:delta_x]
    return figure, delta_y, delta_x


def parse_figure():
    """
    Parse the figure.
    0 - nothing
    1 - *
    2 - .
    """
    line = input()
    line = line.split()
    piece_y = int(line[1])
    piece_x = line[2]
    piece_x = piece_x[:-1]
    piece_x = int(piece_x)
    figura_lst = [[str(0)] * piece_x for i in range(piece_y)]
    for i in range(piece_y):
        line = input()
        line += ' ' * piece_x
        for j in range(piece_x):
            if line[j] == '.':
                figura_lst[i][j] = 2
            elif line[j] == '*':
                figura_lst[i][j] = 1
    return figura_lst


def step(player: int):
    """
    Perform one step of the game.
    :param player: Represents whether we're the first or second player
    """
    y, x = parse_field_info()
    move = parse_field_2(player, y, x)
    return move


def play(player: int):
    """
    Main game loop.

    :param player: Represents whether we're the first or second player
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
    return 1 if "p1 :" in i else 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
