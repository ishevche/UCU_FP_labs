#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filler Bot
"""
from typing import Optional

EMPTY = 0
PLAYER = 1
OPPONENT = 2
Tile = int
Field = list[list[Tile]]
Point = tuple[int, int]
Move = tuple[int, int]
INF = 10000000


def bfs(heatmap: Field, stack: list[Point]):
    """
    Runs bfs with starting tiles at stack
    """
    height = len(heatmap)
    width = len(heatmap[0])
    level = 1

    while stack:
        new_stack = []
        for py, px in stack:
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x, y = px + dx, py + dy
                if 0 <= x < width and 0 <= y < height and heatmap[y][x] > level:
                    new_stack.append((y, x))
                    heatmap[y][x] = level
        level += 1
        stack, new_stack = new_stack, []


def create_heatmap(board: Field) -> list[list[int]]:
    """
    Creates heatmap based on current state of the board
    """
    height = len(board)
    width = len(board[0])

    def tile_to_int(tile: Tile):
        if tile == OPPONENT:
            return 0
        if tile:
            return -2
        return INF

    heatmap = [[tile_to_int(cell) for cell in row] for row in board]
    stack = [(row, col) for row in range(height) for col in range(width) if heatmap[row][col] == 0]
    stack.extend([(height // 3, width // 3), (height * 2 // 3, width * 2 // 3)])

    bfs(heatmap, stack)
    return heatmap


def iterate_filled_fields(figure: Field):
    """
    Iterates through all filled fields in figure
    """
    for row_idx, row in enumerate(figure):
        for col_idx, tile in enumerate(row):
            if tile:
                yield row_idx, col_idx


def parse_board_dimensions() -> tuple[int, int]:
    """
    Parses board dimensions from stdin
    """
    height, width = input()[8:-1].split(' ')
    return int(height), int(width)


def parse_board(board_dimensions: tuple[int, int], player: int) -> Field:
    """
    Parses board from stdin
    """
    input()
    field = Field()
    for _ in range(board_dimensions[0]):
        row = []
        line = input()
        for char in line.split(' ')[1]:
            row.append({'.': 0,
                        'x': 2 - int(player == 2),
                        'o': 2 - int(player == 1)}[char.lower()])
        field.append(row)
    return field


def cut_figure(figure: Field) -> tuple[tuple[int, int], Field]:
    """
    [[1, 0], [1, 1], [1, 1]]
    """
    def is_empty_row(row: int):
        return (0 <= row < len(figure)) and all(map(lambda x: not x, figure[row]))

    def is_empty_col(col: int):
        rotated = list(list(x) for x in zip(*figure))
        return (0 <= col < len(figure[0])) and all(map(lambda x: not x, rotated[col]))

    offset = 0, 0
    while is_empty_row(offset[0]):
        offset = offset[0] + 1, offset[1]
    while is_empty_col(offset[1]):
        offset = offset[0], offset[1] + 1

    del figure[:offset[0]]
    for idx, _ in enumerate(figure):
        del figure[idx][:offset[1]]

    while is_empty_row(len(figure) - 1):
        figure.pop()
    while is_empty_col(len(figure[0]) - 1):
        for idx, _ in enumerate(figure):
            figure[idx].pop()

    return offset, figure


def parse_figure() -> tuple[tuple[int, int], Field]:
    """
    Parses figure from stdin
    """
    height, _ = input()[6:-1].split(' ')
    figure = Field()
    for _ in range(int(height)):
        figure.append([int(char == '*') for char in input()])
    return cut_figure(figure)


def parse_player() -> int:
    """
    Parse player number from stdin
    """
    return 1 if "p1 :" in input() else 2


def get_score(heatmap: list[list[int]], figure: Field, move: Move):
    """
    Get score of the figure placed on a heatmap
    """
    score = 0
    for row_idx, col_idx in iterate_filled_fields(figure):
        score += heatmap[move[0] + row_idx][move[1] + col_idx]
    return score


def get_tile(board: Field, row: int, col: int) -> Optional[Tile]:
    """
    Get tile from board
    """
    if 0 <= row < len(board) and 0 <= col < len(board[row]):
        return board[row][col]
    return None


def can_place_figure(board: Field, figure: Field, move: Move) -> bool:
    """
    Checks if move is valid
    """
    intersect_count = 0
    for row_idx, col_idx in iterate_filled_fields(figure):
        tile = get_tile(board, move[0] + row_idx, move[1] + col_idx)
        if tile is None or tile == OPPONENT:
            return False
        if tile:
            intersect_count += 1

    return intersect_count == 1


def make_move(board: Field, offset: tuple[int, int], figure: Field) -> Move:
    """
    Makes move
    """
    positions = []
    for row_idx in range(-len(figure), len(board)):
        for col_idx in range(-len(figure[0]), len(board[0])):
            if can_place_figure(board, figure, (row_idx, col_idx)):
                positions.append((row_idx, col_idx))

    heatmap = create_heatmap(board)
    scores = map(lambda move: (get_score(heatmap, figure, move), move), positions)
    best_move = min(scores)[1]
    return (best_move[0] - offset[0], best_move[1] - offset[1])


def main():
    """
    Main bot loop
    """
    player = parse_player()
    try:
        while True:
            board = parse_board(parse_board_dimensions(), player)
            offset, figure = parse_figure()
            print(*make_move(board, offset, figure))
    except Exception:
        print('-1 -1')


if __name__ == "__main__":
    main()
