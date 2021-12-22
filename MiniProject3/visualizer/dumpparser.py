"""
Module for parsing game dump file
"""
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
Field = list[list[int]]
State = tuple[Field, bool, bool]
History = tuple[list[State], str, str]


def parse(dump: str) -> History:
    lines = dump.split('\n')
    line_idx = 0
    player1_name = player2_name = 'NO_NAME'
    player1_alive = player2_alive = True
    history = []
    while line_idx < len(lines):
        line = lines[line_idx]
        if line.startswith('$$$ exec'):
            name = line[line.index('[') + 1:line.index(']')].split('/')[-1]
            if 'p1 :' in line:
                player1_name = name
            else:
                player2_name = name
        elif line.startswith('Plateau'):
            height = line[8:-1].split(' ')[0]
            line_idx += 1
            field = []
            for _ in range(int(height)):
                line_idx += 1
                line = lines[line_idx]
                row = []
                for char in line.split(' ')[1]:
                    row.append({'X': PLAYER2, 'O': PLAYER1, '.': EMPTY}[char.upper()])
                field.append(row)
            history.append((field, player1_alive, player2_alive))
        elif "Player with" in line:
            if line.split(' ')[2][0] == '1':
                player1_alive = False
            else:
                player2_alive = False
        line_idx += 1
    return history, player1_name, player2_name
