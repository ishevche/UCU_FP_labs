#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
My bot, version 8.4 'Lesser he thinks, better he works'
"""
import timeit


from logging import DEBUG, debug, getLogger

getLogger().setLevel(DEBUG)

symbols = [["o", "O"], ["x", "X"]]


def main():
    """
    Main function
    """
    def parse_info_about_player():
        """
        This function parses the info about the player

        It can look like this:

        $$$ exec p2 : [./player1.py]
        """
        i = input()
        return 0 if "p1 :" in i else 1

    def play():
        """
        Function with game cycle
        """

        move_num = 0
        ofield = []

        def placed_symbols():
            """
            Searches placed symbols
            """
            for i in range(len(field)):
                for j in range(len(field[i])):
                    if field[i][j] in gs:
                        all_g_points.append((i, j))
                    if field[i][j] in bs:
                        all_b_points.append((i, j))

        def parse_field_info():
            """
            Parses the info about the field.

            Returns height and width of the field

            """
            l = input()
            h, w = int(l.split()[1]), int(l.split()[2][:-1])
            return h, w

        def parse_field():
            """
            Parses the field.

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
            field = [0] * height
            for i in range(-1, height):
                inp = input()
                if i != -1:
                    field[i] = inp[-width:]
            return field

        def parse_figure():
            """
            Parses the figure.

            The function parses the height and the width of the figure.
            Returns it for further usage.

            The input may look like this:

            Piece 2 2:
            **
            ..
            """
            piece = []
            inp = input()
            height, width = int(inp.split()[1]), int(inp.split()[2][:-1])
            for _ in range(height):
                inp = input()
                piece.append(inp)
            return piece

        def move_decision():
            """
            Function which determines the next move of the bot
            """
            def appropriate_moves():
                """
                Finds moves which can be made with given piece
                """
                def imaginary_board_conflicts(pos):
                    """
                    Determines, whether the move is correct
                    """
                    count = 0
                    for row in range(len(n_piece)):
                        for col in range(len(n_piece[row])):
                            if field[pos[0] + row][pos[1] + col] in gs and piece[row][col] != ".":
                                count += 1
                            elif (field[pos[0] + row][pos[1] + col] in bs and piece[row][col] != ".") or (
                                    field[pos[0] + row][pos[1] + col] in gs and count > 1 and piece[row][col] != "."):
                                return False
                    if count == 1:
                        return True
                    return False

                def cropping_piece():
                    """
                    Crops the piece, throwing away points on the right and bottom
                    """
                    new_piece = []
                    for row in range(len(piece)):
                        new_piece.append([])
                        for sym in range(len(piece[row])):
                            new_piece[row].append(piece[row][sym])
                    check = True
                    while check:
                        for i in new_piece[-1]:
                            if i != ".":
                                check = False
                        if check:
                            new_piece.pop()
                    check = True
                    while check:
                        for i in range(len(new_piece)):
                            if new_piece[i][-1] != ".":
                                check = False
                        if check:
                            for i in range(len(new_piece)):
                                new_piece[i].pop()
                    return new_piece

                moves = []
                n_piece = cropping_piece()
                for row_count in range(len(field)):
                    for pos_num in range(len(field[row_count])):
                        # here i can add some initial test to exclude some definitely bad positions
                        # why row_count + len(piece) <= len(field), not row_count + len(piece) <= len(field) -1?
                        if (row_count + len(n_piece) <= len(field)) \
                                and (pos_num + len(n_piece[0]) <= len(field[0])):
                            if imaginary_board_conflicts((row_count, pos_num)):
                                moves.append((row_count, pos_num))
                return moves

            def imaginary_board(move, mode=None):
                """
                Returns the list of newly placed symbols if the given move will be performed
                """
                i_board = []
                for i in range(len(field)):
                    i_board.append([])
                    for j in range(len(field[i])):
                        i_board[i].append(field[i][j])
                if mode:
                    new_stars_pos = []
                for row in range(len(piece)):
                    for col in range(len(piece[row])):
                        if move[0] + row <= len(field) and move[1] + col <= len(field[0]):
                            if mode and piece[row][col] == "*" and \
                                    field[move[0] + row][move[1] + col] not in gs:
                                new_stars_pos.append((move[0] + row, move[1] + col))
                            if not mode:
                                i_board[move[0] + row][move[1] + col] = piece[row][col]
                if mode:
                    return new_stars_pos
                else:
                    return i_board

            def updating_score(moves):
                """
                Calculates score for each move
                """
                for move in moves:
                    positions = imaginary_board(move, 1)
                    for pos in positions:
                        if field[pos[0]][pos[1]] == ".":
                            moves_price[move] += field_tiles_prices[pos[0]][pos[1]]

            def bubble_ops():
                """
                Finds 'bubbles'(places, surrounded only with friendly symbols) and makes the value
                of bubbled positions be equal to 0.
                """
                additional_field = []
                bubbles = {}
                tile_bubble = {}
                bubble_isolation = {}
                count = 0

                for i in range(len(field)):
                    additional_field.append([])
                    for j in range(len(field[i])):
                        additional_field[i].append(field[i][j])

                for row in range(len(field)):
                    for column in range(len(field[0])):
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if (not 0 <= row + i < len(field) or
                                    not 0 <= column + j < len(field[0])
                                    or additional_field[row + i][column + j]
                                    in gs) and additional_field[row][column] == ".":
                                    additional_field[row][column] = "$"
                                elif 0 <= row + i < len(field) \
                                        and 0 <= column + j < len(field[0]) \
                                        and additional_field[row + i][column + j] in bs \
                                        and (
                                        additional_field[row][column] == "."
                                        or additional_field[row][column] == "$"):
                                    additional_field[row][column] = "B"

                for row in range(len(field)):
                    for column in range(len(field[0])):
                        if additional_field[row][column] in ".$B":
                            count += 1
                            tile_bubble[(row, column)] = count
                            bubbles[count] = {(row, column)}
                            bubble_isolation[count] = True
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if 0 <= row + i < len(field) and 0 <= column + j < len(field[0]) \
                                            and additional_field[row + i][column + j] in "*&D" \
                                            and tile_bubble[(row, column)] != tile_bubble[(row + i, column + j)]:

                                        temp_num = tile_bubble[(row, column)]

                                        for tile in bubbles[tile_bubble[(row, column)]]:
                                            tile_bubble[tile] = tile_bubble[(row + i, column + j)]
                                        bubbles[tile_bubble[(row + i, column + j)]] = \
                                            bubbles[tile_bubble[(row + i, column + j)]].union(bubbles[temp_num])
                                        bubble_isolation[tile_bubble[(row + i, column + j)]] = \
                                            bubble_isolation[temp_num] and bubble_isolation[
                                                tile_bubble[(row + i, column + j)]]
                                        del bubbles[temp_num]
                                        del bubble_isolation[temp_num]
                                    elif 0 <= row + i < len(field) and 0 <= column + j < len(field[0]) and \
                                            additional_field[row + i][column + j] in "DB":
                                        bubble_isolation[tile_bubble[(row, column)]] = False

                            if additional_field[row][column] == ".":
                                additional_field[row][column] = "*"
                            if additional_field[row][column] == "$":
                                additional_field[row][column] = "&"
                            if additional_field[row][column] == "B":
                                additional_field[row][column] = "D"
                for bubble in bubble_isolation:
                    if bubble_isolation[bubble] == True:
                        for bubble_tpl in bubbles[bubble]:
                            field_tiles_prices[bubble_tpl[0]][bubble_tpl[1]] = -10**5

            def priority_near_enemy(mode="enemy is far"):
                """
                Raises priority of tiles near the enemy
                """
                additional_field = []
                check = True
                priority_level = {}

                for i in range(len(field)):
                    additional_field.append([])
                    for j in range(len(field[i])):
                        additional_field[i].append(field[i][j])
                count = 1
                while check:
                    to_change = []

                    for row in range(len(additional_field)):
                        for column in range(len(additional_field[0])):
                            if additional_field[row][column] == ".":
                                for i in range(-1,2):
                                    for j in range(-1,2):
                                        if 0 <= row+i < len(field) and 0 <= column+j < len(field[0]):
                                            if additional_field[row+i][column+j] in [*bs, "*"]:
                                                to_change.append((row,column))

                    for row in range(len(additional_field)):
                        for column in range(len(additional_field[0])):
                            if additional_field[row][column] == "*":
                                additional_field[row][column] = "-"

                    for point in to_change:
                        additional_field[point[0]][point[1]] = "*"
                        priority_level[point] = count

                    count += 1
                    check = False
                    if to_change:
                        check = True
                for point in priority_level:
                    if mode == "close fight":
                        field_tiles_prices[point[0]][point[1]] += (1/(abs(priority_level[point]-min(3, width*0.1))+1)**3)*10
                    else:
                        field_tiles_prices[point[0]][point[1]] += (1 / (priority_level[point]) ** 3) * 10

            def check_whether_enemy_is_far(dis):
                """
                Checks if the enemy is closer than 'dis'(in terms of cells)
                """
                for row in range(len(field)):
                    for column in range(len(field[0])):
                        if field[row][column] in gs:
                            for i in range(-dis,dis+1):
                                for j in range(-dis,dis+1):
                                    if 0 <= row + i < len(field) and 0 <= column + j < len(field[0]):
                                        if field[row+i][column+j] in bs:
                                            return False
                return True

            def diagonal_rat():
                """
                Raises the priority of cells which allow to go through the enemy's built line
                """
                for row in range(len(field)):
                    for column in range(len(field[0])):
                        if 0 <= row + 1 < len(field) and 0 <= column + 1 < len(field[0]):
                            if field[row][column] in bs and field[row + 1][column + 1] in bs and\
                                    field[row + 1][column] == "." and field[row][column + 1] == ".":
                                field_tiles_prices[row + 1][column] += 100
                                field_tiles_prices[row][column + 1] += 100
                            elif field[row][column+1] in bs and field[row + 1][column] in bs and\
                                    field[row][column] == "." and field[row + 1][column + 1] == ".":
                                field_tiles_prices[row][column] += 100
                                field_tiles_prices[row + 1][column + 1] += 100

            def stack_debuff(k):
                """
                Debuffs the value of tiles with many friendly adjacent tiles
                """
                for i in range(len(field)):
                    for j in range(len(field[0])):
                        for m in range(1,3):
                            for n in range(1,3):
                                if 0<=i+m<len(field) and 0<=j+n<len(field[0]):
                                    if field[i+m][j+n] in gs:
                                        field_tiles_prices[i][j] -= k

            def edge_tiles(k):
                """
                Finds tiles which are on the edge and are adjacent to enemy. Then raises their priority.
                """
                edge_positions_to_buff = []
                for row in range(0,max(2, height*0.05)):
                    for column in range(0, len(field[0])):
                        for i in range(-1,2):
                            for j in range(-1,2):
                                if 0 <= row + i < len(field) and 0 <= column + j < len(field[0]) and field[row + i][column + j] in bs:
                                    edge_positions_to_buff.append((row,column))
                for row in range(len(field)-max(2, height*0.05),len(field)):
                    for column in range(0, len(field[0])):
                        for i in range(-1,2):
                            for j in range(-1,2):
                                if 0 <= row + i < len(field) and 0 <= column + j < len(field[0]) and field[row + i][column + j] in bs:
                                    edge_positions_to_buff.append((row,column))
                for column in range(0,max(2, width*0.05)):
                    for row in range(0, len(field)):
                        for i in range(-1,2):
                            for j in range(-1,2):
                                if 0 <= row + i < len(field) and 0 <= column + j < len(field[0]) and field[row + i][column + j] in bs:
                                    edge_positions_to_buff.append((row,column))
                for column in range(len(field[0])-max(2, width*0.05),len(field[0])):
                    for row in range(0, len(field)):
                        for i in range(-1,2):
                            for j in range(-1,2):
                                if 0 <= row + i < len(field) and 0 <= column + j < len(field[0]) and field[row + i][column + j] in bs:
                                    edge_positions_to_buff.append((row,column))
                for pos in edge_positions_to_buff:
                    field_tiles_prices[pos[0]][pos[1]] += k

            field_tiles_prices = []
            for i in range(len(field)):
                lst = []
                for j in range(len(field[0])):
                    lst.append(0)
                field_tiles_prices.append(lst)
            move = None

            moves = appropriate_moves()
            moves_price = {i: 0 for i in moves}

            if check_whether_enemy_is_far(min(6, width*0,3)):
                priority_near_enemy()
            elif check_whether_enemy_is_far(min(2, width*0,1)):
                priority_near_enemy()
                stack_debuff(3)
            else:
                priority_near_enemy(mode="close fight")
                edge_tiles(5)
            diagonal_rat()
            bubble_ops()

            updating_score(moves)

            for key in moves_price:
                if moves_price[key] == max(moves_price.values()):
                    move = key
                    break
            if move:
                return move
            else:
                return (0, 0)

        while True:
            height, width = parse_field_info()
            field = parse_field()
            piece = parse_figure()
            all_g_points = []
            all_b_points = []

            placed_symbols()

            start = timeit.default_timer()
            move = move_decision()
            ofield = field
            stop = timeit.default_timer()
            execution_time = stop - start
            # debug(execution_time)
            print(*move)
            move_num += 1

    def determine_player():
        """
        Determines player's symbols
        """
        if player == 1:
            good_s = symbols[1]
            bad_s = symbols[0]
        else:
            good_s = symbols[0]
            bad_s = symbols[1]
        return good_s, bad_s

    player = parse_info_about_player()
    gs, bs = determine_player()

    try:
        play()
    except EOFError as error:
        debug(error)
        debug("Cannot get input. Seems that we've lost ):!!!!!!!1")


if __name__ == "__main__":
    main()
