#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import DEBUG, debug, getLogger
import math

getLogger().setLevel(DEBUG)


def parse_step_info(player_char):
    """
    Module functions that parse all the information we get.
    :param player_char: the symbol used by the player's move
    :return: field, field_size, figure, possible, player_points, enemy_points
    """

    def parse_size():
        """
        Gets information about the size of the field.
        :return: field size.
        """
        size = input()

        size_split = size.split()
        height = int(size_split[1])
        width = int(size_split[2].replace(":", ""))
        debug(f"Size: {width} {height}")
        return width, height

    def parse_field():
        """
        This function parses the field.
        :return:field and its dimensions.
        """
        field = []
        width, height = parse_size()
        tmp = input()  # skip numbers header
        for _ in range(height):
            line_in_field = input()
            noHeader = line_in_field[4:width + 4]  # skip line header
            debug(f"Field: {noHeader}")
            field.append(noHeader)

        return field, (width, height)

    def parse_figure():
        """
        The function gets information about the figure and processes it.
        :return: figure.
        """
        figure = []
        width, height = parse_size()
        for _ in range(height):
            line_in_figure = input()
            figure.append(line_in_figure)
            debug(f"Figure: {line_in_figure}")
        return figure

    def is_matching(field, figure, check_x, check_y, symbol):
        """
        The function checks whether the set of rules for the figure and moves
        that can be made by it match.
        :param field: field where the game is going on.
        :param figure: figure that we want to put on the field.
        :param check_x: x point of the field to check.
        :param check_y:y point of the field to check.
        :param symbol: symbol that is used by player for a play.
        :return: 1 if all rules matches or False if we can not put the given figure on the field.
        """
        crosses = 0

        y = check_y - 1

        for f_line in figure:
            y += 1
            x = check_x - 1
            if y > len(field):
                return False
            for c in f_line:
                x += 1
                if c == '.':
                    continue
                if x > len(field[y]):
                    return False

                if field[y][x] != '.' and field[y][x].lower() != symbol:
                    return False
                if field[y][x].lower() == symbol:
                    crosses += 1

        return crosses == 1

    def all_possible_moves(field, symbol, figure):
        """
        The function looks for all possible moves that we can use to place the figure.
        :param field: field where the game is going on.
        :param symbol: symbol that is used by player for a play.
        :param figure: figure that we want to put on the field.
        :return: List of points where we can put our figure.
        """
        figure_height = len(figure)
        figure_width = len(figure[0])

        field_height = len(field)
        field_width = len(field[0])

        possible_moves = []
        for y in range(field_height - figure_height + 1):
            for x in range(field_width - figure_width + 1):
                # now we will check whether it is possible to put at a given point x, y our figure.
                if is_matching(field, figure, x, y, symbol):
                    possible_moves.append((x, y))
                    debug(f"possible {x} {y}")
        return possible_moves

    def get_points(field, player_char):
        """
        The function reads the field given to us and finds the coordinates that are occupied by the
        symbol that was transmitted during the call (or the symbol of our bot, or the enemy).
        :param field: field where the game is going on.
        :param player_char: symbol that is used by player for a play.
        :return: cords that are already filled with symbol that uses the player(enemy bot or our).
        """
        field_height = len(field)
        field_width = len(field[0])
        list_of_cord_used_by_player = []
        for y in range(field_height):
            for x in range(field_width):
                if field[y][x].lower() == player_char:
                    list_of_cord_used_by_player.append((x, y))
        return list_of_cord_used_by_player

    def get_enemy_char(player_char):
        """
        The function finds the symbol of the opponent's bot.
        :param player_char: the symbol used by our bot.
        :return: the symbol used by enemy bot.
        """
        if player_char.lower() == 'x':
            return 'o'
        return 'x'

    field, field_size = parse_field()
    figure = parse_figure()
    possible = all_possible_moves(field, player_char, figure)
    enemy_char = get_enemy_char(player_char)
    player_points = get_points(field, player_char)
    enemy_points = get_points(field, enemy_char)
    return field, field_size, figure, possible, player_points, enemy_points


def analyze_points(points):
    def find_center(points):
        """
        The function looks for the center of the biomass
        (a figure that has already been built before)
        :param points: all occupied coordinates
        :return: center of the figure
        """
        x_values = [v[0] for v in points]
        y_values = [v[1] for v in points]

        x_center = sum(x_values) / len(x_values)
        y_center = sum(y_values) / len(y_values)
        return x_center, y_center

    center = find_center(points)

    return center


def vector_sub(final_v, initial_v):
    """
    The function searches for two coordinates
    :param final_v: final vector
    :param initial_v: initial vector
    :return: coordinates of the middle of these points
    """
    return final_v[0] - initial_v[0], final_v[1] - initial_v[1]


def vector_dot(first_vector, second_vector):
    """
    Function finds dot product of vectors.
    :param first_vector: first_vector.
    :param second_vector: second vector.
    :return: dot product of vectors
    """
    return sum(x * y for x, y in zip(second_vector, first_vector))


def vector_len(v):
    """
    The function calculates the length of the vector
    :param v: vector coordinates
    :return: length of the vector
    """
    return math.sqrt(sum(i * i for i in v))


def vector_normalize(vector):
    """
    The function reduces the vector to 1 while maintaining the ratio.
    :param vector:
    :return: shortened vector.
    """
    length = vector_len(vector)
    return vector[0] / length, vector[1] / length


def step(player_char, step_id):
    """
    The function decides how to make a move.
    :param player_char: the symbol used by our bot
    :return: coordinates for the move
    """
    (field, field_size, figure, possible_moves, player_points, enemy_points) = parse_step_info(player_char)

    if len(possible_moves) == 0:
        return "giveup"
    # debug(f"player points {player_points}")
    player_center = analyze_points(player_points)

    (width, height) = field_size
    field_center = (width / 2, height / 2)

    attack_direction = vector_sub(field_center, player_center)
    normalized_attack_direction = vector_normalize(attack_direction)

    best_move_candidate = possible_moves[0]
    best_alignment = -10  # to trigger change on first iteration

    for moves in possible_moves:
        possible_direction = vector_sub(moves, player_center)

        # checking is center of biomass is at the same place as possible move
        dir_len = vector_len(possible_direction)
        if dir_len < 0.0001:  # float comparation should not be done by ==
            if best_alignment < 0:  # if move to the center is best that we have for now - take it
                best_alignment = 0
                best_move_candidate = moves
            continue  # skipping all future checks since this move does not have vector

        # debug(f"dir len {dir_len}")

        normalized_possible_direction = vector_normalize(possible_direction)

        alignment = vector_dot(normalized_attack_direction, normalized_possible_direction)*dir_len

        # debug(f"move {moves} alignment:{alignment}")

        if alignment > best_alignment:
            best_alignment = alignment
            best_move_candidate = moves
    pick = best_move_candidate
    debug(f"pick {pick}")
    return pick[1], pick[0]  # switch (x,y) to (y,x)


def play(player_char):
    """
    The function provides the functions required to make the game.
    :param player_char: symbol that the bot will use.
    """
    counter = 0
    while True:
        move = step(player_char, counter)
        counter += 1
        print(*move)


def parse_info_about_player():
    """
    The function receives information from the input and displays
    which player our bot will be.
    :return: symbol that the bot will use.
    """
    i = input()
    debug(f"Info about the player: {i}")
    return 'o' if "p1 :" in i else 'x'


def main():
    """
    The function launches the program.
    """
    player_char = parse_info_about_player()
    try:
        play(player_char)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
