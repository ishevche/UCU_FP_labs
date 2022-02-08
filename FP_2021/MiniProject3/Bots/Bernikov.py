#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""
from logging import DEBUG, debug, getLogger

from queue import PriorityQueue
from types import resolve_bases

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)     #-------------------------------------------------------------------------------------------------------------------------------


def parse_field_size():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    rows, columns = input().split()[1:]
    debug(f"Description of the field: {rows} : {columns[:-1]}")
    return int(rows), int(columns[:-1])

def check_position(field, figure, ind, player):
    """
    Check if figure can be place there
    """
    search_el = "o" if player==1 else "x"
    line, column = ind[0], ind[1] #+1
    if len(figure) > len(field)-line or len(figure[0]) > len(field[0]) - column:
        return False
    el_count = 0
    for figure_line_ind, figure_line in enumerate(figure):
        for tmp_ind in range(ind[1], ind[1]+len(figure_line)):
            if figure_line[tmp_ind-ind[1]] != '.' and field[ind[0]+figure_line_ind][tmp_ind]!=".":
                if field[ind[0]+figure_line_ind][tmp_ind]==search_el:
                    el_count +=1
                else:
                    return False
    return True if el_count==1 else False


def parse_field(player: int, rows: int, columns:int):
    """
    Parse the field.

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
    for i in range(rows+1):
        l = input()
        if i ==0:
            continue
        field.append([el.lower() for el in l.split()[1]])

    return field

        
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
    height = int(l.split()[1])
    figure = []
    vertical_change = 0
    horizontal_change = 0
    stop_checking = False
    for _ in range(height):
        l = input()
        if "*" not in l:
            if not stop_checking:vertical_change-=1
            continue
        stop_checking = True
        line = l.replace("*", "O") if player==1 else l.replace("*", "X")
        figure.append([el for el in line.lower()])
    trasnposed_figure = [[figure[j][i] for j in range(len(figure))] for i in range(len(figure[0]))]
    stop_checking = False
    final_transposed = []
    for line in trasnposed_figure:
        if "x" not in line and "o" not in line:
            if not stop_checking :horizontal_change-=1
            continue
        stop_checking = True
        final_transposed.append(line)
    final_figure = [[final_transposed[j][i] for j in range(len(final_transposed))] for i in range(len(final_transposed[0]))] 
    return final_figure, vertical_change, horizontal_change


def count_neighbours(field, figure, player, ind):
    """
    Count enemy elements around your figure
    """
    search_el = "x" if player==1 else "o"
    count = 0
    fig_len = len(figure)
    left_permission = True if ind[1]!=0 else False
    right_permission = not ind[1]+len(figure[0])>len(field[0])-1
    up_permission = True if ind[0]!=0 else False
    down_permission = not ind[0]+fig_len>len(field)-1
    for i in range(fig_len):
        if i==0 and up_permission:
            count += field[ind[0]-1][ind[1]:ind[1]+len(figure[0])].count(search_el) #up
        if left_permission: count += field[ind[0]+i][ind[1]-1].count(search_el) #left
        if right_permission: count += field[ind[0]+i][ind[1]+len(figure[0])].count(search_el) #right
        if i+1==fig_len and down_permission:
            count += field[ind[0]+i+1][ind[1]:ind[1]+len(figure[0])].count(search_el)
    return count
    
def count_your_neighbours(field, figure, player, ind):
    """
    Count your own elements around figure
    """
    search_el = "x" if player==1 else "o"
    count = 0
    fig_len = len(figure)
    left_permission = True if ind[1]!=0 else False
    right_permission = not ind[1]+len(figure[0])>len(field[0])-1
    up_permission = True if ind[0]!=0 else False
    down_permission = not ind[0]+fig_len>len(field)-1
    for i in range(fig_len):
        if i==0 and up_permission:
            line = field[ind[0]-1][ind[1]:ind[1]+len(figure[0])]
            for el_ind in range(len(line)):
                if line[el_ind]==search_el and figure[i][el_ind]!=".":
                    count += 1
        if left_permission and figure[i][0] != ".": count += field[ind[0]+i][ind[1]-1].count(search_el) #left
        if right_permission and figure[i][-1] != ".": count += field[ind[0]+i][ind[1]+len(figure[0])].count(search_el) #right
        if i+1==fig_len and down_permission:
            line = field[ind[0]+i+1][ind[1]:ind[1]+len(figure[0])]
            for el_ind in range(len(line)):
                if line[el_ind]==search_el and figure[i][el_ind]!=".":
                    count+=1
    return count



def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    rows, columns = parse_field_size()
    field = parse_field(player, rows, columns)
    figure, v_change, h_change = parse_figure(player)
    res = []
    for i in range(rows):
        for j in range(columns):
            ind = (i, j)
            if check_position(field, figure, ind, player):
                enemy = 1 if player == 2 else 2
                res.append((ind, count_neighbours(field, figure, player, ind), count_your_neighbours(field, figure, enemy, ind)))
    if any([el[1] for el in res]):
        move = sorted(res, key=lambda x:(x[1], -x[2]), reverse=True)[0][0]
    elif len(res)>0: 
        enemy_el = "x" if player==1 else "o"
        to_find_min_distance = PriorityQueue()
        enemy_inds = []
        for line_ind in range(len(field)):
            for col_ind in range(len(field[0])):
                if field[line_ind][col_ind] == enemy_el:
                    enemy_inds.append((line_ind, col_ind))
        for ind in res:
            diff = sum(map(lambda x: abs(x[0]-ind[0][0])+abs(x[1]-ind[0][1]), enemy_inds))
            to_find_min_distance.put((diff, ind[0]))
        move = to_find_min_distance.get()[-1]

    else:
        move = (0, 0)
    move = move[0]+v_change, move[1]+h_change
    return move


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
