def validate(line: list):
    return sorted(line) == [x for x in range(1, 10)]


class RowsVerifier:
    def __init__(self, grid):
        self.grid = grid

    def verif_rows(self):
        for row in self.grid:
            if not validate(row):
                return False
        return True


class ColsVerifier:
    def __init__(self, grid):
        self.grid = grid

    def verif_cols(self):
        for i in range(9):
            col: list = []
            for j in range(9):
                col.append(self.grid[i][j])
            if not validate(col):
                return False
        return True


class SquareVerifier:
    def __init__(self, grid):
        self.grid = grid

    def verif_squares(self):
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square: list = []
                for k in range(3):
                    for l in range(3):
                        square.append(self.grid[i + k][j + l])
                if not validate(square):
                    return False
        return True


class SudokuVerifier:
    def __init__(self, grid):
        self.grid = grid
        self.rows_verifier = RowsVerifier(grid)
        self.cols_verifier = ColsVerifier(grid)
        self.square_verifier = SquareVerifier(grid)

    def verif_grid(self):
        if self.rows_verifier.verif_rows() and self.cols_verifier.verif_cols() and self.square_verifier.verif_squares():
            return True
        else:
            return False
