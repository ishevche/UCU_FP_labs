"""
lifegrid.py
"""

from arrays import Array2D


class LifeGrid:
    """
    Implements the LifeGrid ADT for use with the Game of Life.
    """
    # Defines constants to represent the cell states.
    DEAD_CELL = 0
    LIVE_CELL = 1

    def __init__(self, num_rows, num_cols):
        """
        Creates the game grid and initializes the cells to dead.
        :param num_rows: the number of rows.
        :param num_cols: the number of columns.
        """
        # Allocates the 2D array for the grid.
        self._grid = Array2D(num_rows, num_cols)
        # Clears the grid and set all cells to dead.
        self.configure(list())

    def num_rows(self):
        """
        Returns the number of rows in the grid.
        :return: the number rows in the grid.
        """
        return self._grid.num_rows()

    def num_cols(self):
        """
        Returns the number of columns in the grid.
        :return:Returns the number of columns in the grid.
        """
        return self._grid.num_cols()

    def configure(self, coord_list):
        """
        Configures the grid to contain the given live cells.

        :param coord_list: coords of alive cells
        """
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if (row, col) in coord_list:
                    self.set_cell(row, col)
                else:
                    self.clear_cell(row, col)

    def is_live_cell(self, row, col):
        """
        Does the indicated cell contain a live organism?

        :param row: row of the cell.
        :param col: column of the cell.
        :return: the result of check.
        """
        return self._grid[row, col] == LifeGrid.LIVE_CELL

    def clear_cell(self, row, col):
        """
        Clears the indicated cell by setting it to dead.
        :param row: row of the cell.
        :param col: column of the cell.
        """
        self._grid[row, col] = LifeGrid.DEAD_CELL

    def set_cell(self, row, col):
        """
        Sets the indicated cell to be alive.
        :param row: row of the cell.
        :param col: column of the cell.
        """
        self._grid[row, col] = LifeGrid.LIVE_CELL

    def num_live_neighbors(self, row, col):
        """
        Returns the number of live neighbors for the given cell.
        :param row: row of the cell.
        :param col: column of the cell.
        :return:
        """
        neighbors = []
        neighbors += [(row - 1, col)]
        neighbors += [(row - 1, col - 1)]
        neighbors += [(row - 1, col + 1)]
        neighbors += [(row, col - 1)]
        neighbors += [(row, col + 1)]
        neighbors += [(row + 1, col)]
        neighbors += [(row + 1, col - 1)]
        neighbors += [(row + 1, col + 1)]

        ans = 0
        for neighbor in neighbors:
            if 0 <= neighbor[0] < self.num_rows() and \
                    0 <= neighbor[1] < self.num_cols() and \
                    self.is_live_cell(*neighbor):
                ans += 1
        return ans

    def __str__(self):
        """
        Returns string representation of LifeGrid
        in form of:
        DDLDD
        DLDLD
        DLDLD
        DDLDD
        DDDDD
        Where D - dead cell, L - live cell
        """
        ans = ''
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if self.is_live_cell(row, col):
                    ans += 'L'
                else:
                    ans += 'D'
            ans += '\n'
        return ans[:-1]
