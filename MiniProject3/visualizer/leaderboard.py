import argparse
import math
import os
import random
import subprocess
import sys

import numpy.random

import visualizer

filler_path, field_path, bots_path, results_path = '', '', '', ''
progress_draw = 0
progress_x = 0
progress_max = 0


def main():
    global filler_path, field_path, bots_path, results_path, progress_max
    filler_path, field_path, bots_path, results_path = get_args()

    bots = list(filter(lambda x: os.path.isfile(os.path.join(bots_path, x)),
                       os.listdir(bots_path)))
    bots: list = numpy.random.permutation(bots).tolist()

    progress_max = len(bots)
    start_progress('Filtering slow bots')
    filter_bots(bots)
    end_progress()

    n = len(bots)
    print(f'{n} bots left')

    rounds = int(math.log2(len(bots)))
    first_round_amount = len(bots) - 2 ** rounds

    progress_max = first_round_amount * 5
    start_progress('Qualifying rounds')
    results = [play_round(bots, first_round_amount)]
    end_progress()

    for game in results[-1]:
        if game[0][1] > game[1][1]:
            bots.remove(game[1][0])
        else:
            bots.remove(game[0][0])
    if not results[-1]:
        results.clear()

    while len(bots) != 1:
        progress_max = 5 * len(bots) // 2
        start_progress(f'1/{progress_max // 5} final'
                       if progress_max != 5 else 'FINAL')
        results += [play_round(bots, len(bots) // 2)]
        end_progress()
        for game in results[-1]:
            if game[0][1] > game[1][1]:
                bots.remove(game[1][0])
            else:
                bots.remove(game[0][0])
    print_results(results)
    os.system('cat results.txt')


def start_progress(title):
    global progress_x, progress_draw
    sys.stdout.write(title + ": [" + "-" * 40 + "]" + chr(8) * 41)
    sys.stdout.flush()
    progress_x = 0
    progress_draw = 0


def progress():
    global progress_draw
    x = progress_x * 40 // progress_max
    sys.stdout.write("#" * (x - progress_draw))
    sys.stdout.flush()
    progress_draw = x


def end_progress():
    sys.stdout.write("#" * (40 - progress_draw) + "]\n")
    sys.stdout.flush()


def print_results(other):
    with open('results.txt', 'w') as out:
        lines = [''] * (len(other[1]) * 4)
        for circle_num, circle in enumerate(other):
            if circle_num == len(other) - 1: continue
            pow2 = 2 ** (circle_num + 2)
            similar = 2 ** circle_num
            if circle_num == 0:
                coll_arr = circle[:len(other[1])]
            else:
                coll_arr = circle[:len(circle) // 2]
            add_col1(lines, coll_arr, pow2, similar)
            if circle_num == 0:
                for i in range(len(coll_arr) * 4, len(other[1]) * 4):
                    lines[i] += ' ' * 14
        last_game = other[-1][0]
        if last_game[0][1] > last_game[1][1]:
            winner = "╢" + last_game[0][0].replace(".py", "") + "╟"
        else:
            winner = "╢" + last_game[1][0].replace(".py", "") + "╟"
        for i in range(len(other[1]) * 4):
            if len(other[1]) * 2 - 4 <= i <= len(other[1]) * 2 - 1:
                if last_game[0][1] > last_game[1][1]:
                    if len(other[1]) * 2 - 4 == i:
                        lines[i] += ' ' * 14 + '╔' + '═' * (
                                len(winner) - 2) + '╗' + ' ' * 14
                    elif len(other[1]) * 2 - 3 == i:
                        lines[i] += ' ' * 13 + '┏' + winner + '┐' + ' ' * 13
                    elif len(other[1]) * 2 - 2 == i:
                        lines[i] += ' ' * 13 + \
                                    '┃╚' + '═' * (len(winner) - 2) + '╝│' + \
                                    ' ' * 13
                    else:
                        lines[
                            i] += f'{cut(last_game[0][0], 8):8} ({last_game[0][1]}) ' + \
                                  '┛' + ' ' * len(winner) + '└' + \
                                  f'{cut(last_game[1][0], 8):8} ({last_game[1][1]}) '
                else:
                    if len(other[1]) * 2 - 4 == i:
                        lines[i] += ' ' * 14 + '╔' + '═' * (
                                len(winner) - 2) + '╗' + ' ' * 14
                    elif len(other[1]) * 2 - 3 == i:
                        lines[i] += ' ' * 13 + '┌' + winner + '┓' + ' ' * 13
                    elif len(other[1]) * 2 - 2 == i:
                        lines[i] += ' ' * 13 + \
                                    '│╚' + '═' * (len(winner) - 2) + '╝┃' + \
                                    ' ' * 13
                    else:
                        lines[
                            i] += f'{cut(last_game[0][0], 8):8} ({last_game[0][1]}) ' + \
                                  '┘' + ' ' * len(winner) + '┗' + \
                                  f'{cut(last_game[1][0], 8):8} ({last_game[1][1]}) '
            else:
                lines[i] += ' ' * (14 + len(winner) + 14)
        for circle_num, circle in reversed(list(enumerate(other))):
            if len(circle) == 1: continue
            pow2 = 2 ** (circle_num + 2)
            similar = 2 ** circle_num
            if circle_num == 0:
                coll_arr = circle[len(other[1]):]
            else:
                coll_arr = circle[len(circle) // 2:]
            add_col2(lines, coll_arr, pow2, similar)
        out.write('\n'.join(lines[:-1]))


def add_col1(lines, circle, pow2, similar):
    for idx, game in enumerate(circle):
        for i in range(similar - 1):
            lines[idx * pow2 + i] += (" " * 14)
            lines[idx * pow2 + similar * 3 + i] += (" " * 14)
        if game[0][1] > game[1][1]:
            lines[idx * pow2 + similar * 1 - 1] += \
                f'{cut(game[0][0], 8):8} ({game[0][1]}) ┓'
            lines[idx * pow2 + similar * 2 - 1] += \
                f'{" " * 13}┡'
            lines[idx * pow2 + similar * 3 - 1] += \
                f'{cut(game[1][0], 8):8} ({game[1][1]}) ┘'
            lines[idx * pow2 + similar * 4 - 1] += \
                f'{" " * 14}'
            for i in range(similar - 1):
                lines[idx * pow2 + similar * 1 + i] += (" " * 13) + '┃'
                lines[idx * pow2 + similar * 2 + i] += (" " * 13) + '│'
        else:
            lines[idx * pow2 + similar * 1 - 1] += \
                f'{cut(game[0][0], 8):8} ({game[0][1]}) ┐'
            lines[idx * pow2 + similar * 2 - 1] += \
                f'{" " * 13}┢'
            lines[idx * pow2 + similar * 3 - 1] += \
                f'{cut(game[1][0], 8):8} ({game[1][1]}) ┛'
            lines[idx * pow2 + similar * 4 - 1] += \
                f'{" " * 14}'
            for i in range(similar - 1):
                lines[idx * pow2 + similar * 1 + i] += (" " * 13) + '│'
                lines[idx * pow2 + similar * 2 + i] += (" " * 13) + '┃'


def add_col2(lines, circle, pow2, similar):
    for idx, game in enumerate(circle):
        for i in range(similar - 1):
            lines[idx * pow2 + i] += (" " * 14)
            lines[idx * pow2 + similar * 3 + i] += (" " * 14)
        if game[0][1] > game[1][1]:
            lines[idx * pow2 + similar * 1 - 1] += \
                f'┏{cut(game[0][0], 8):8} ({game[0][1]}) '
            lines[idx * pow2 + similar * 2 - 1] += \
                f'┩{" " * 13}'
            lines[idx * pow2 + similar * 3 - 1] += \
                f'└{cut(game[1][0], 8):8} ({game[1][1]}) '
            lines[idx * pow2 + similar * 4 - 1] += \
                f'{" " * 14}'
            for i in range(similar - 1):
                lines[idx * pow2 + similar * 1 + i] += '┃' + (" " * 13)
                lines[idx * pow2 + similar * 2 + i] += '│' + (" " * 13)
        else:
            lines[idx * pow2 + similar * 1 - 1] += \
                f'┌{cut(game[0][0], 8):8} ({game[0][1]}) '
            lines[idx * pow2 + similar * 2 - 1] += \
                f'┪{" " * 13}'
            lines[idx * pow2 + similar * 3 - 1] += \
                f'┗{cut(game[1][0], 8):8} ({game[1][1]}) '
            lines[idx * pow2 + similar * 4 - 1] += \
                f'{" " * 14}'
            for i in range(similar - 1):
                lines[idx * pow2 + similar * 1 + i] += '│' + (" " * 13)
                lines[idx * pow2 + similar * 2 + i] += '┃' + (" " * 13)


def cut(name, num):
    name = name.replace('.py', '')
    if len(name) > num:
        name = name[:num - 2] + '..'
    return name


def filter_bots(bots):
    global progress_x
    for bot in bots.copy():
        bot_path = os.path.join(bots_path, bot)
        try:
            game = subprocess.Popen(
                f"{filler_path} -f {field_path} "
                f"-p1 {bot_path} -p2 {bot_path}",
                shell=True, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            game.wait(timeout=60 * 5)
            progress_x += 1
            progress()
        except Exception as e:
            if "timed out" in str(e):
                bots.remove(bot)
            else:
                print(e)


def play_round(bots, amount):
    global progress_x
    starts = []
    for game_idx in range(amount):
        starts += [play_games(bots[2 * game_idx], bots[2 * game_idx + 1])]
        progress_x += 4
        progress_x -= progress_x % 5
        progress()
    return starts


def play_games(first, second):
    global progress_x
    first_wins = 0
    second_wins = 0
    while first_wins < 3 and second_wins < 3:
        back_order = random.randint(0, 1)
        if back_order:
            winner = play_game(second, first, first_wins + second_wins)
        else:
            winner = play_game(first, second, first_wins + second_wins)
        if winner == first:
            first_wins += 1
            progress_x += 1
        elif winner == second:
            second_wins += 1
            progress_x += 1
        progress()
    return (first, first_wins), (second, second_wins)


def play_game(first, second, game_idx):
    first_name = first.replace('.py', '')
    second_name = second.replace('.py', '')
    first_path = os.path.join(bots_path, first)
    second_path = os.path.join(bots_path, second)
    result_gifs = os.path.join(results_path, 'gifs')
    result_reports = os.path.join(results_path, 'reports')
    game_name = f'{first_name}-{second_name}-{game_idx}'
    report_path = os.path.join(result_reports, f'{game_name}r.txt')
    gif_path = os.path.join(result_gifs, f'{game_name}g.gif')
    ans = None
    try:
        game = subprocess.Popen(
            f"{filler_path} -f {field_path} "
            f"-p1 {first_path} -p2 {second_path} "
            f"> {report_path}",
            shell=True, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        game.wait(timeout=60 * 100000)
        visualizer.generate_gif(report_path, gif_path)
        with open('filler.trace', 'r') as trace:
            lines = list(filter(lambda x: ' won' in x,
                                trace.readlines()))
            if not lines:
                raise ValueError()
            winner = lines[0].replace(' won\n', '')
            if winner == first_path:
                ans = first
            elif winner == second_path:
                ans = second
            else:
                print('ERROR no winner')
    except Exception as e:
        print(e)
    finally:
        os.remove('filler.trace')
        return ans


def get_args():
    """
    Get args specified in the cmd
    :return: Namespace object with all arguments
    """
    parser = argparse.ArgumentParser(
        description='Plays leaderboard'
    )
    parser.add_argument(
        '-bots',
        help='path to bots directory'
    )
    parser.add_argument(
        '-result',
        help='path to result directory'
    )
    parser.add_argument(
        '-filler',
        help='path to filler_vm'
    )
    parser.add_argument(
        '-map',
        help='path to a map'
    )
    args = parser.parse_args()
    return args.filler, args.map, args.bots, args.result


if __name__ == "__main__":
    main()
