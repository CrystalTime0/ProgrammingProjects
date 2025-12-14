import random


class SudokuGenerator:

    def __init__(self):
        self.grid = []
        self.solved_grid = []

    def findNextCellToFill(self, i, j):
        for x in range(i, 9):
            for y in range(j, 9):
                if self.grid[x][y] == 0:
                    return x, y
        for x in range(0, 9):
            for y in range(0, 9):
                if self.grid[x][y] == 0:
                    return x, y
        return -1, -1

    def isValid(self, i, j, e):
        rowOk = all([e != self.grid[i][x] for x in range(9)])
        if rowOk:
            columnOk = all([e != self.grid[x][j] for x in range(9)])
            if columnOk:
                # finding the top left x,y co-ordinates of the section containing the i,j cell
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)  # floored quotient should be used here.
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if self.grid[x][y] == e:
                            return False
                return True
        return False

    def solveSudoku(self, i=0, j=0):
        i, j = self.findNextCellToFill(i, j)
        if i == -1:
            return True
        for _ in range(9):
            e = random.randint(1, 9)
            if self.isValid(i, j, e):
                self.grid[i][j] = e
                if self.solveSudoku(i, j):
                    return True
                # Undo the current cell for backtracking
                self.grid[i][j] = 0
        return False

    def generate_full_sudoku(self):
        self.grid = [[0] * 9 for _ in range(9)]
        while not self.solveSudoku():
            self.grid = self.generate_sudoku()

    def remove_cells(self, holes=3):
        """
        Enlève un nombre de cases pour créer un vrai Sudoku jouable.
        """
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)

        for i in range(holes):
            r, c = positions[i]
            self.grid[r][c] = 0

    def generate_sudoku(self, holes=50):
        self.generate_full_sudoku()
        self.solved_grid = [row[:] for row in self.grid]
        self.remove_cells(holes)
        return self.grid
