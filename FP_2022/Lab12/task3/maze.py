"""Implemention of the Maze ADT using a 2-D array."""
from arrays import Array2D
from arraystack import ArrayStack


class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        parents_map: dict = {}
        dfs_stack = ArrayStack()
        dfs_stack.push(self._start_cell.coords())
        exit_found = False
        while not dfs_stack.isEmpty():
            cur_cell = dfs_stack.pop()
            self._mark_tried(*cur_cell)
            if self._exit_found(*cur_cell):
                exit_found = True
                break
            row, col = cur_cell
            moves = [(row, col - 1), (row + 1, col),
                     (row, col + 1), (row - 1, col)]
            for move in moves:
                if self._valid_move(*move):
                    dfs_stack.push(move)
                    parents_map[move] = cur_cell
        if exit_found:
            path_cell = self._exit_cell.coords()
            while path_cell != self._start_cell.coords():
                self._mark_path(*path_cell)
                path_cell = parents_map[path_cell]
            self._mark_path(*path_cell)
        return exit_found

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if (self._maze_cells[row, col] == self.TRIED_TOKEN or
                        self._maze_cells[row, col] == self.PATH_TOKEN):
                    self._maze_cells[row, col] = None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        ans = ''
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                value = self._maze_cells[row, col]
                if value is None:
                    ans += '_ '
                else:
                    ans += f'{value} '
            ans += '\n'
        return ans[:-1]

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return (0 <= row < self.num_rows() and
                0 <= col < self.num_cols() and
                self._maze_cells[row, col] is None)

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN

    @classmethod
    def build_maze(cls, path):
        """
        Returns a maze built from the file located at path
        """
        with open(path, 'r') as maze_input:
            rows, cols = map(int, maze_input.readline().split())
            maze = cls(rows, cols)
            start_row, start_col = map(int, maze_input.readline().split())
            maze.set_start(start_row, start_col)
            exit_row, exit_col = map(int, maze_input.readline().split())
            maze.set_exit(exit_row, exit_col)
            for row in range(rows):
                row_str = maze_input.readline()
                for col, row_cell in enumerate(row_str):
                    if row_cell == '*':
                        maze.set_wall(row, col)
            return maze


class _CellPosition(object):
    """Private storage class for holding a cell position."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def coords(self):
        """
        Returns self coordinates
        """
        return self.row, self.col
