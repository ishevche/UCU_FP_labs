"""
board.py
"""


class Board:
    """
    Represents a game board
    """

    def __init__(self):
        self._board = [[' '] * 3,
                       [' '] * 3,
                       [' '] * 3]

    def get_status(self):
        """
        Returns the current state on the board
        """
        possible_lines = ((0, 3, 6),
                          (1, 4, 7),
                          (2, 5, 8),
                          (0, 1, 2),
                          (3, 4, 5),
                          (6, 7, 8),
                          (0, 4, 8),
                          (2, 4, 6))
        for line in possible_lines:
            if (self.get_cell(line[0]) == self.get_cell(line[1]) and
                    self.get_cell(line[1]) == self.get_cell(line[2])):
                if self.get_cell(line[1]) == 'x':
                    return 'x'
                if self.get_cell(line[1]) == '0':
                    return '0'

        for row in self._board:
            if ' ' in row:
                return 'continue'

        return 'draw'

    def get_cell(self, coords_number):
        """
        Returns data in the cell
        """
        return self._board[coords_number // 3][coords_number % 3]

    def set_cell(self, coords_number, turn):
        """
         Sets data in cell
        """
        self.make_move((coords_number // 3, coords_number % 3), turn)

    def make_move(self, position, turn):
        """
        Makes turn at position
        """
        if turn != '0' and turn != 'x':
            raise IndexError('Only 0 or x turn allowed')
        if self.get_cell(position[0] * 3 + position[1]) != ' ':
            raise IndexError('The cell i occupied')
        self._board[position[0]][position[1]] = turn

    def build_tree(self, turn):
        """
        Builds a possible turns tree, returns indexes for both possibilities
        """
        status = self.get_status()
        if status == 'x':
            return -1, 0
        if status == '0':
            return 1, 0
        if status == 'draw':
            return 0, 0
        possible_turns = []
        for move in range(9):
            if self.get_cell(move) == ' ':
                possible_turns += [move]
        possible_turns = possible_turns[:2]
        ans = []
        if len(possible_turns) == 1:
            ans = [0]
        for cur_turn in possible_turns:
            self.set_cell(cur_turn, turn)
            ans += [sum(self.build_tree({'0': 'x', 'x': '0'}[turn]))]
            self._board[cur_turn // 3][cur_turn % 3] = ' '
        return tuple(ans)

    def make_computer_move(self):
        """
        Makes the best computer move
        """
        first_variant, second_variant = self.build_tree('0')
        variant_idx = 0
        if first_variant < second_variant:
            variant_idx = 1
        position = -1
        for i in range(9):
            if self.get_cell(i) == ' ':
                if variant_idx == 0:
                    position = i
                    break
                else:
                    variant_idx -= 1
        self.set_cell(position, '0')

    def __str__(self):
        ans = ''
        for row in self._board:
            ans += f'{row}\n'
        return ans[:-1]
