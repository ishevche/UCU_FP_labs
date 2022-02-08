"""chesspuzzle.py"""


def chess_puzzle(bishop, queen):
    """
    Searches all all not attacked places by bishop and queen
    :param bishop: bishop location
    :param queen: queen location
    :return: a set of all possible places
    >>> chess_puzzle('b5', 'g3') == {'b2', 'a1', 'a8', 'b6', 'f8', 'h6', 'c8',\
    'd4', 'd1', 'e4', 'd2', 'b7', 'f5', 'a2', 'c5', 'e6', 'h7', 'e7', 'b4', \
    'h8', 'a5', 'c2', 'f7', 'b1', 'h5','c1', 'a7', 'd8', 'h1', 'f6', 'd5'}
    True
    """
    cols = 'abcdefgh'
    rows = '12345678'
    b_col, b_row = cols.index(bishop[0]), rows.index(bishop[1])
    q_col, q_row = cols.index(queen[0]), rows.index(queen[1])
    ans_set = set()
    for col in cols:
        for row in rows:
            ans_set.add(col + row)
    ans_set = ans_set.difference(get_line_through(b_col, b_row, 1, 1))
    ans_set = ans_set.difference(get_line_through(b_col, b_row, 1, -1))
    ans_set = ans_set.difference(get_line_through(q_col, q_row, 1, 1))
    ans_set = ans_set.difference(get_line_through(q_col, q_row, 1, -1))
    ans_set = ans_set.difference(get_line_through(q_col, q_row, 1, 0))
    ans_set = ans_set.difference(get_line_through(q_col, q_row, 0, 1))
    return ans_set


def get_line_through(col, row, cols_incr, rows_incr):
    """
    Gets all cells in line, that passes through given cell
    :return: set of cells on the line
    """
    return get_line_from(col, row, cols_incr, rows_incr).union(
        get_line_from(col, row, -cols_incr, -rows_incr)
    )


def get_line_from(start_col, start_row, cols_incr, rows_incr):
    """
    Gets all cells in line, that starts at given cell
    :return: set of cells on the line
    """
    cols = 'abcdefgh'
    rows = '12345678'
    ans = set()
    cur_attacked_cell_col = start_col
    cur_attacked_cell_row = start_row
    while 0 <= cur_attacked_cell_col < len(cols) and \
            0 <= cur_attacked_cell_row < len(rows):
        cur_attacked_cell = cols[cur_attacked_cell_col] + \
                            rows[cur_attacked_cell_row]
        ans.add(cur_attacked_cell)
        cur_attacked_cell_col += cols_incr
        cur_attacked_cell_row += rows_incr
    return ans
