#!/usr/bin/env python3
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

""" parse given objects """
def parse_field_info():
    """
    Got:
    Plateau 15 17
    Return:
    (15, 17)
    """
    l = input()
    # # debug(f'1 parse fielf info{l}')
    # debug(f"Description of the field: {l}")
    return int(l.split()[1]), int(l.split()[2][:-1])

def parse_field(field_inf: tuple):
    """
    Got:
        01234567
    000 .X......
    001 ........
    002 .....O..
    Return:
    [list('.X......'), list('........'), list('.....O..')] field in handy way
    """
    # move = None
    field = []
    for i in range(int(field_inf[0])+1):
        l = input()
        # debug(f"Field: {l}")
        if i == 0:
            pass
        else:
            field.append(list(l[4:]))
        # if move is None:
        #     c = l.lower().find("o" if player == 1 else "x")
        #     if c != -1:
        #         move = i - 1, c - 4
    # assert move is not None
    return field

def parse_figure():

    """
    Got:
    Piece 2 3:
    ***
    ...
    Return:
    ((2, 3), ['***', '...']) everything about the piece
    """
    l = input()
    # # debug(f'parse_figure{l}')
    l = l.split()
    # # debug(l)
    dimen = int(l[1]), int(l[2][:-1])
    # debug(f"Piece: {l}")
    height = int(l[1])
    figure = []
    for _ in range(height):
        l = input()
        figure.append(l)
        # debug(f"Piece: {l}")
    return dimen, figure
# for taking figure without dots
def real_fig(ever):
    dimen, figure = ever[0], ever[1]
    height = 0
    width = 0
    col_del = []
    ln_del = []

    for col in range(dimen[1]):
        flag = False
        for line in figure:
            if line[col] == '*':
                flag = True
                width += 1
                break
        if not flag:
            col_del.append(col)

    for line in range(dimen[0]):
        if '*' in figure[line]:
            height += 1
        else:
            ln_del.append(line)

    # debug(f'{col_del, ln_del}')
    # min_ln = [ln_del[i] for i in range(len(ln_del)) if ln_del[0]==1 and (ln_del[i] if i > 0) ]
    min_ln = 0
    if len(ln_del) != 0:
        if ln_del[0] == 0:
            min_ln = 1
            # debug(f'hahhh{len(ln_del), ln_del}')
            for i in range(1, len(ln_del)):
                # debug(f'{i}')
                if ln_del[i]-1 == ln_del[i-1]:
                    min_ln += 1
                else:
                    break

    min_row = 0
    if len(col_del) != 0:
        if col_del[0] == 0:
            min_row = 1
            # debug(f'eeej{len(col_del), col_del}')
            for i in range(1, len(col_del)):
                # debug(f'{i, col_del, col_del[i-1], col_del[i]-1}')
                if (col_del[i]-1) == col_del[i-1]:
                    min_row += 1
                else:
                    break

    # debug(f'=={min_ln, min_row}')

    for line in reversed(ln_del):
        del figure[line]
    # debug(f'{figure}')
    for line in range(height):
        for col in reversed(col_del):
            # debug(f'{figure[line], col}')
            figure[line] = figure[line][:col]+ figure[line][col+1:]
    # debug(f'{(height, width), figure}')
    return (height, width), figure, (min_ln, min_row)

""" Srategy0 """
# every dot of the oppponent
def ev_dots(player, field, fld_dim, oppponent = True, symb='dva'):
    if oppponent:
        player = 1 if player == 2 else 2
    symb = 'o' if player == 1 else 'x'
    elems = (symb.upper() or symb) if symb == 'dva' else (symb,)
    # debug(f'{elems}')
    for row in field:
        if row.count(symb.upper() or symb) > 1:
            opp_dots = [(row, col, ) for col in range(fld_dim[1]) for row in range(fld_dim[0]) if field[row][col] in (elems)]
    else:
        opp_dots = [(row, col, ) for col in range(fld_dim[1]) for row in range(fld_dim[0]) if field[row][col] in (symb.upper() or symb)]
    # debug(f'{opp_cords}')
    return opp_dots

# the lower and the hithest border
def borders(dots: list):
    dots.sort(key=lambda x: (x[0], x[1]))
    roof = dots[0]
    floor = dots[-1]
    avarage_roof = [dot[1] for dot in dots if dot[0] == roof[0]]
    avarage_roof = roof[0], round(sum(avarage_roof)/len(avarage_roof))
    avarage_floor = [dot[1] for dot in dots if dot[0] == floor[0]]
    avarage_floor = floor[0], round(sum(avarage_floor)/len(avarage_floor))
    # debug(f'roof = {avarage_roof}, floor = {avarage_floor}')
    return avarage_floor, avarage_roof

# len from one dot to another
def len_dot(dts):
    dt1, dt2 = dts[0], dts[1]
    return ((dt1[0]-dt2[0])**2+(dt1[1]-dt2[1])**2)**(0.5)

# move that is the closet to dot 
def mv_close_to_dot(dot, moves, min_max='min'):
    moves.sort(key=lambda x: ((x[0]-dot[0])**2+(x[1]-dot[1])**2))
    return moves[0] if min_max == 'min' else moves[-1]
# nešto čudno
def filling_tight(field, figure, moves):
    pass

def glob_var(field):
    global pole
    pole = field
    # debug(f'==={pole}')

def new_move(player:int, old:list, new: list)->set:
    symb = 'O' if player == 1 else 'X'
    rows = len(old)
    colons = len(old[0])
    # for i in range(rows):
    #     debug(f'{new[i]}')
    #     debug(f'{old[i]}')

    moves = {(row, col) for col in range(colons) for row in range(rows) if old[row][col] != new[row][col] != symb}
    debug(f'{moves}')
    return moves

# function that apply strategy
def strat(field, figure, moves, player, field_dim):
    if len(moves) == 0:
        return
    # moves.sort(key=lambda x: (x[0], x[1]))
    # debug(f'{field}')
    try:
        pre_field = pole
    except:
        pre_field = [['.' for _ in range(len(field[0]))] for _ in range(len(field))]
    glob_var(field)
    # debug(f'{field, pre_field}')
    # new_move(field)
    neww_mvs = new_move(player, pre_field, field)
    debug(f'{neww_mvs}')
    # opp_dots = ev_dots(player, field, field_dim, oppponent=True)
    # opp_brdrs = borders(opp_dots)
    # our_dots = ev_dots(player, field, field_dim, oppponent=False)
    # our_brdrs = borders(our_dots)
    # dot_aim = sorted([(i, j) for i in opp_brdrs for j in our_brdrs], key=len_dot)
    # opp_dots.sort(key=lambda x: )
    # dot_aim = sorted([(i, j) for i in opp_brdrs for j in our_brdrs], key=len_dot)

    # debug(f'{dot_aim}')
    if len(neww_mvs) != 0:
        move = mv_close_to_dot(list(neww_mvs)[0], moves)
    else:
        move =  mv_close_to_dot((0, 0), moves)
    return move

""" every possible move """
def ev_move(player, field, figure, f_dim):
    """
    Got:
    ((2, 3), ['***', '...'])
    Return:
    {(x1, y1), (x2, y2),...,(xn, yn)}
    """
    cords = set()
    symb = 'o' if player == 1 else 'x'
    for num_line in range(f_dim[0]):
        if (symb.upper() or symb) in field[num_line]:
            # debug('***')
            opt_line_up = num_line
            break
    opt_line_up = opt_line_up - figure[0][0] if opt_line_up > figure[0][0] else 0

    for row in range(opt_line_up, f_dim[0]-figure[0][0]+1):
        for col in range(f_dim[1]-figure[0][1]+1):
            counter = 0
            flag = True
            for i in range(figure[0][0]):
                for j in range(figure[0][1]):
                    # # debug(f'i={figure}')
                    if figure[1][i][j] == '*':
                        # # debug(f'=={field[row+i][col+j].lower()}, {symb}')
                        if field[row+i][col+j].lower() == symb:
                            counter += 1
                            # # debug('eeeeej')
                        elif field[row+i][col+j].lower() != '.':
                            flag = False
            if counter == 1 and flag:
                dot = row-figure[2][0], col-figure[2][1]
                cords.add(dot)
                # # debug(f'cords{dot}')
    # # debug(f' Evo tebi i set {cords}')
    return cords

""" define where to go """
def step(player: int):
    """
    Got:
    ---
    Return:
    (x, y) cords of the move
    """
    move = None
    fld_dim = parse_field_info() 
    field = parse_field(fld_dim)
    figure = real_fig(parse_figure())
    moves = ev_move(player, field, figure, fld_dim)
    # debug(f'{list(moves)}')
    move = strat(field, figure, list(moves), player, fld_dim)
    return move

""" make a move """
def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        if move == None:
            print('1 1')
        else:
            # debug(f'{type(move), type(move[0])}')
            print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    # debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()

""" pl 1 == 'o' """
