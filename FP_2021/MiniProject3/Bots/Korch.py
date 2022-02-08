#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A bot for a programming project. Always puts a figure on the field
if possible, tries to restrict enemy's movement.
The algorithm is described in attached pdf file.
"""
import copy
from logging import DEBUG, debug, getLogger
getLogger().setLevel(DEBUG)


all_info = []


def parse_field_info():
    """
    Parse the info about the field.
    Returns a height of the field as string
    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    l = input()
    return l.split()[1:]


def parse_field(player: int, map_size: int):
    """
    Parse the field.
    Returns a list of lists filled with either dots or letters
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
    field = []
    for i in range(map_size + 1):
        l = input()
        l = l[4:]
        element = []
        for item in l:
            element.append(item)
        field.append(element)
    return field[1:]


def parse_figure():
    """
    Parse the figure.
    Returns a piece as list of rows of the figure.
    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **
    ..
    """
    l = input()
    l = l.split()
    piece = []
    height = int(l[1])
    for _ in range(height):
        l = input()
        piece.append(l)
    return piece


def where_is(field: list, who: str, point: tuple):
    """
    Returns a list of coordinates of 'who' sorted by distance to 'point'.
    Args:
        field (list): [[...]...]
        who (str): "X" or "O"
        point (tuple): (int, int)
    """
    height_f = len(field)
    length_f = len(field[0])
    coords = list()
    for row in range(height_f):
        for col in range(length_f):
            if field[row][col] == who:
                coords.append((row, col))
    closest = sorted(coords, key=lambda x: just_dist(x, point))
    return closest


def towards_centers(field: list, piece: list, my_assets: list, me: str):
    """
    Returns a coordinate (y, x) if possible to put on the field.
    Opposite case - (0, 0)
    Args:
        field (list): a map
        piece (list): list of lists
        my_assets (list): all possible coords
        me (str): "X" or "O"
    Returns:
        tuple: (y, x)
    """
    bests = []
    him = "O" if me == "X" else "X"
    destination = the_center(field, hislet=him)

    piece_cent = rel_center(piece)
    for item in my_assets:
        n_item = item[0] - piece_cent[0], item[1] - piece_cent[1]
        bests.append((just_dist(n_item, destination), item))
    if bests:
        res = sorted(bests, key=lambda x: x[0])[0][1]
        return res
    return (0, 0)


def rel_center(piece):
    """
    Finds a relative center of the piece.
    """
    height = len(piece)
    leng = len(piece[0])
    return height // 2, leng // 2


def diff_fs(field, hislet):
    """
    Finds and returns the average coords from last enemy's move.
    """
    coords = []
    then = only_enemy(all_info[-1], hislet)
    now = only_enemy(field, hislet)
    for row in range(len(now)):
        for item in range(len(now[0])):
            if now[row][item] != then[row][item]:
                coords.append((row, item))
    all_info.pop()
    if coords:
        return (sum([it[0] for it in coords]) / len(coords),
                sum([it[1] for it in coords]) / len(coords))
    return None


def only_enemy(field: list, his_let: str):
    """
    Returns a field with enemy letters.
    """
    new_field = [["." for i in range(len(field[0]))]
                 for i in range(len(field))]
    for row in range(len(field)):
        for col in range(len(field[0])):
            if field[row][col] == his_let:
                new_field[row][col] = his_let
    return new_field


def center_map(field):
    """
    Returns the center of the field. 
    """
    return (len(field) // 2, len(field[0]) // 2)


def is_free(field, pos):
    """
    Checks whether the position on the field is free.
    """
    for i in range(2):
        for j in range(2):
            try:
                if field[pos[0] + i][pos[1] + i] != ".":
                    return False
            except IndexError:
                continue
    return True


def calc_squares(field):
    """
    Returns the amount (quantity (number)) of free squares on the field.  
    """
    quan = 0
    for row in field:
        for item in row:
            if item == ".":
                quan += 1
    return quan


def field_divider(field, part="every", includes=[1, 2, 3, 4]):
    """
    Returna a divided field with the biggest number of free squares
    and its part on the original field.
    """
    if part == "every":
        a_count, b_count, c_count, d_count = 0, 0, 0, 0
        if 1 in includes:
            a = field_divider(field, part=1)
            a_count = calc_squares(a)
        if 2 in includes:
            b = field_divider(field, part=2)
            b_count = calc_squares(b)
        if 3 in includes:
            c = field_divider(field, part=3)
            c_count = calc_squares(c)
        if 4 in includes:
            d = field_divider(field, part=4)
            d_count = calc_squares(d)
        max_squares = max(a_count, b_count, c_count, d_count)
        if max_squares != 0:
            if max_squares == a_count:
                return a, 1
            elif max_squares == b_count:
                return b, 2
            elif max_squares == c_count:
                return c, 3
            else:
                return d, 4
        if "a" in locals():
            return a, 1
        elif "b" in locals():
            return b, 2
        elif "c" in locals():
            return c, 3
        elif "d" in locals():
            return d, 4
    new_f = []
    if part == 1:
        field = field[:len(field) // 2 + 1]
        for row in field:
            new_f.append(row[:len(row) // 2 + 1])
    elif part == 2:
        field = field[:len(field) // 2 + 1]
        for row in field:
            new_f.append(row[len(row) // 2:])
    elif part == 3:
        field = field[len(field) // 2:]
        for row in field:
            new_f.append(row[:len(row) // 2 + 1])
    elif part == 4:
        field = field[len(field) // 2:]
        for row in field:
            new_f.append(row[len(row) // 2:])
    return new_f


def the_center(field, hislet):
    """
    Returns a direction where the bot should go. Or the center of the map in worst case.
    Divides the field into four pieces.
    """
    cur_d = center_map(field)
    now = is_free(field, cur_d)
    if now:
        return cur_d
    else:
        apps, to_exclude = field_divider(field)
        new_dot = center_map(apps)
        check = is_free(apps, new_dot)
        if check:
            return calc_point(field, new_dot, to_exclude)
        else:
            to_include = [i for i in range(1, 5) if i != to_exclude]
            new_apps, to_exclude = field_divider(field,
                                                 part="every",
                                                 includes=to_include)
            new_dot = center_map(new_apps)
            check = is_free(new_apps, new_dot)
            if check:
                return calc_point(field, new_dot, to_exclude)
            else:
                to_include.remove(to_exclude)
                new_new_apps, to_exclude = field_divider(field,
                                                         part="every",
                                                         includes=to_include)
                new_dot = center_map(new_new_apps)
                check = is_free(new_new_apps, new_dot)
                if check:
                    return calc_point(field, new_dot, to_exclude)
                else:
                    place = diff_fs(field, hislet)
                    if place:
                        return avg_from(field, place)
                    return cur_d


def calc_point(field, relative_d, number):
    """
    Calculates the coord of point on the original field.
    'number' tells which part the dot belong to.
    """
    just_center = center_map(field)
    if number == 1:
        return just_center[0] - relative_d[0], just_center[1] - relative_d[1]
    elif number == 2:
        return just_center[0] - relative_d[0], just_center[1] + relative_d[1]
    elif number == 3:
        return just_center[0] + relative_d[0], just_center[1] - relative_d[1]
    elif number == 4:
        return just_center[0] + relative_d[0], just_center[1] + relative_d[1]


def avg_from(field, place):
    """
    Returns the average of enemy last move coords and the border. 
    """
    to_go = []
    for hey in range(len(field) - 1):
        for leng in range(len(field[0]) - 1):
            if (hey == 0 or leng == 0) and field[hey][leng] == ".":
                to_go.append((just_dist(place, (hey, leng)), (hey, leng)))
    if to_go:
        border = sorted(to_go, key=lambda x: x[0])[0][1]
    else:
        border = place
    return (place[0] + border[0]) / 2, (place[1] + border[1]) / 2


def borders_covered(field: list, him: str, my_pos: list):
    quan = 0
    for item in my_pos:
        if 0 in item:
            quan += 1
    return False if quan < 2 else True


def just_dist(point1: tuple, point2: tuple):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5


def brute_force(field: list, piece: list, me: str, him: str):
    """
    Returns a list of all possible coords where the piece can be put.
    """
    all_pos = []
    for i in range(len(field) - len(piece) + 1):
        for j in range(len(field[0]) - len(piece[0]) + 1):
            if put_checker(field=field,
                           piece=piece,
                           pos=(i, j),
                           my_let=me,
                           his_let=him):
                all_pos.append((i, j))
    return all_pos


def put_checker(field: list, piece: list, pos: tuple, my_let: str,
                his_let: str):
    """
    Checks whether the position is suitable to be put by rules.
    """
    p_hey = len(piece)
    p_leng = len(piece[0])
    quantity = 0
    start_h = pos[0]
    end_h = pos[0] + p_hey
    start_l = pos[1]
    end_l = pos[1] + p_leng
    for height in range(start_h, end_h):
        for length in range(start_l, end_l):
            ciple = piece[height - start_h][length - start_l]
            already_f = field[height][length]
            if ciple == ".":
                continue
            if ciple == "*":
                if already_f == my_let:
                    quantity += 1
                elif already_f == his_let:
                    return False
                elif already_f == ".":
                    continue
    return True if quantity == 1 else False


def where_to_put(figure: list, field: list, player: int):
    """
    Main function. Calculates the right move.
    Returns a tuple - coordiantes. 
    """
    mylet = "O" if player == 1 else "X"
    hislet = "O" if player == 2 else "X"
    all_pos = brute_force(field, figure, mylet, hislet)
    best_one = towards_centers(field, figure, all_pos, mylet)
    all_info.append(field)
    return best_one


def piece_cutter(piece: list):
    """
    Returns a sliced piece at the bottom and right sides.
    """
    new_piece = copy.copy(piece)
    while True:
        last_thing = set()
        for i in range(len(piece)):
            last_thing.add(piece[i][-1])
        if "*" in last_thing:
            break
        new_piece = []
        for row in piece:
            new_piece.append(row[:-1])
        piece = copy.copy(new_piece)
    while True:
        last_thing = set()
        for i in range(len(piece[0])):
            last_thing.add(piece[-1][i])
        if "*" in last_thing:
            break
        new_piece = []
        for row in piece:
            new_piece = piece[:-1]
        piece = copy.copy(new_piece)
    return new_piece


def piece_cutter_2(piece):
    """
    Returns a sliced piece and bias at the top and left sides.
    """
    y = 0
    x = 0
    new_piece = copy.copy(piece)
    while True:
        first_thing = set()
        for i in range(len(piece)):
            first_thing.add(piece[i][0])
        if "*" in first_thing:
            break
        new_piece = []
        x += 1
        for row in piece:
            new_piece.append(row[1:])
        piece = copy.copy(new_piece)
    while True:
        up_thing = set()
        for i in range(len(piece[0])):
            up_thing.add(piece[0][i])
        if "*" in up_thing:
            break
        new_piece = []
        y += 1
        for row in piece:
            new_piece = piece[1:]
        piece = copy.copy(new_piece)
    return piece, (y, x)


def step(player: int):
    """
    Perform one step of the game.
    :param player int: Represents whether we're the first or second player
    """
    map_height = int(parse_field_info()[0])
    field = parse_field(player, map_height)
    piece = parse_figure()
    how_much = (0, 0)
    piece = piece_cutter(piece)
    piece, how_much = piece_cutter_2(piece)
    res = where_to_put(piece, field, player)
    return (res[0] - how_much[0], res[1] - how_much[1])


def play(player: int):
    """
    Main game loop.
    :param player int: Represents whether we're the first or second player
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
