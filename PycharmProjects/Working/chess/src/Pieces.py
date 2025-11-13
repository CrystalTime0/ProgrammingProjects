import pygame
from constants import *


class Piece:
    def __init__(self, Square, image, color, type, row, col):
        self.Square = Square
        self.image = image
        self.color = color
        self.row = row
        self.col = col
        self.type = type
        self.x = 0
        self.y = 0
        self.available_moves = []
        self.calc_pos()

    def piece_move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def calc_pos(self):
        self.x = self.col * self.Square
        self.y = self.row * self.Square

    def clear_available_moves(self):
        if len(self.available_moves) > 0:
            self.available_moves = []


class Pawn(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)
        self.first_move = True

    def get_available_moves(self, Board):
        self.clear_available_moves()

        row, col = self.row, self.col

        if self.color == WHITE:
            if row - 1>= 0:
                if Board.Board[row - 1][col] == 0:
                    self.available_moves.append((row - 1, col))
                    if self.first_move and Board.Board[row - 2][col] == 0:
                        self.available_moves.append((row - 2, col))
            if col - 1 >= 0:
                if Board.Board[row - 1][col - 1] != 0:
                    if Board.Board[row - 1][col - 1].color != self.color:
                        self.available_moves.append((row - 1, col - 1))
                        print(self.available_moves)
            if col + 1 < len(Board):
                if Board.Board[row - 1][col + 1] != 0:
                    if Board.Board[row - 1][col + 1].color != self.color:
                        self.available_moves.append((row - 1, col + 1))

        if self.color == BLACK:
            if row + 1 < len(Board):
                if Board.Board[row + 1][col] == 0:
                    self.available_moves.append((row + 1, col))
                    if self.first_move and Board.Board[row + 2][col] == 0:
                        self.available_moves.append((row + 2, col))
            if col - 1 >= 0:
                if Board.Board[row + 1][col - 1] != 0:
                    if Board.Board[row + 1][col - 1].color != self.color:
                        self.available_moves.append((row + 1, col - 1))
            if col + 1 < len(Board):
                if Board.Board[row + 1][col + 1] != 0:
                    if Board.Board[row + 1][col + 1].color != self.color:
                        self.available_moves.append((row + 1, col + 1))

        # TO-DO : Rajouter En Passant


class Rook(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, Board):
        self.clear_available_moves()

        row, col = self.row, self.col

        # ligne N row+
        for i in range(row-1, -1, -1):
            if Board.Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board.Board[i][col].color != self.color:
                    self.available_moves.append((i, col))
                break

        # ligne S row+
        for i in range(row + 1, len(Board)):
            if Board.Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board.Board[i][col].color != self.color:
                    self.available_moves.append((i, col))
                break

        # ligne O col-
        for i in range(col-1, -1, -1):
            if Board.Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board.Board[row][i].color != self.color:
                    self.available_moves.append((row, i))
                break

        # ligne E col+
        for i in range(col + 1, len(Board)):
            if Board.Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board.Board[row][i].color != self.color:
                    self.available_moves.append((row, i))
                break

class Knight(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, Board):
        self.clear_available_moves()

        row, col = self.row, self.col

        if row - 2 >= 0:
            if col - 1 >= 0:
                if Board.Board[row - 2][col - 1] == 0 or Board.Board[row - 2][col - 1].color != self.color:
                    self.available_moves.append((row-2, col-1))
            if col + 1 < len(Board):
                if Board.Board[row - 2][col + 1] == 0 or Board.Board[row - 2][col + 1].color != self.color:
                    self.available_moves.append((row-2, col+1))
        if row - 1 >= 0:
            if col - 2 >= 0:
                if Board.Board[row - 1][col - 2] == 0 or Board.Board[row - 1][col - 2].color != self.color:
                    self.available_moves.append((row-1, col-2))
            if col + 2 < len(Board):
                if Board.Board[row - 1][col + 2] == 0 or Board.Board[row - 1][col + 2].color != self.color:
                    self.available_moves.append((row-1, col+2))
        if row + 1 < len(Board):
            if col - 2 >= 0:
                if Board.Board[row + 1][col - 2] == 0 or Board.Board[row + 1][col - 2].color != self.color:
                    self.available_moves.append((row+1, col-2))
            if col + 2 < len(Board):
                if Board.Board[row + 1][col + 2] == 0 or Board.Board[row + 1][col + 2].color != self.color:
                    self.available_moves.append((row+1, col+2))
        if row + 2 < len(Board):
            if col - 1 >= 0:
                if Board.Board[row + 2][col - 1] == 0 or Board.Board[row + 2][col - 1].color != self.color:
                    self.available_moves.append((row+2, col-1))
            if col + 1 < len(Board):
                if Board.Board[row + 2][col + 1] == 0 or Board.Board[row + 2][col + 1].color != self.color:
                    self.available_moves.append((row+2, col+1))

class Bishop(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, Board):
        self.clear_available_moves()

        row, col = self.row, self.col

        # diagonale NE row- col+
        row_i = row-1
        col_i = col+1

        while row_i >= 0 and col_i < len(Board):
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i -= 1
                col_i += 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale NO row- col-
        row_i = row - 1
        col_i = col - 1

        while row_i >= 0 and col_i >= 0:
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i -= 1
                col_i -= 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale SE row+ col+
        row_i = row + 1
        col_i = col + 1

        while row_i < len(Board) and col_i < len(Board):
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i += 1
                col_i += 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale S0 row+ col-
        row_i = row + 1
        col_i = col - 1

        while row_i < len(Board) and col_i >= 0:
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i += 1
                col_i -= 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

class Queen(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, Board):
        self.clear_available_moves()

        row, col = self.row, self.col

        # ligne N row+
        for i in range(row-1, -1, -1):
            if Board.Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board.Board[i][col].color != self.color:
                    self.available_moves.append((i, col))
                break

        # ligne S row-
        for i in range(row + 1, len(Board)):
            if Board.Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board.Board[i][col].color != self.color:
                    self.available_moves.append((i, col))
                break

        # ligne O col-
        for i in range(col-1, -1, -1):
            if Board.Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board.Board[row][i].color != self.color:
                    self.available_moves.append((row, i))
                break

        # ligne E col+
        for i in range(col + 1, len(Board)):
            if Board.Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board.Board[row][i].color != self.color:
                    self.available_moves.append((row, i))
                break

        # diagonale NE row- col+
        row_i = row - 1
        col_i = col + 1

        while row_i >= 0 and col_i < len(Board):
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i -= 1
                col_i += 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale NO row- col-
        row_i = row - 1
        col_i = col - 1

        while row_i >= 0 and col_i >= 0:
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i -= 1
                col_i -= 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale SE row+ col+
        row_i = row + 1
        col_i = col + 1

        while row_i < len(Board) and col_i < len(Board):
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i += 1
                col_i += 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale S0 row+ col-
        row_i = row + 1
        col_i = col - 1

        while row_i < len(Board) and col_i >= 0:
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i += 1
                col_i -= 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

class King(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, Board):
        self.clear_available_moves()

        row, col = self.row, self.col

        possible_values = (-1, 0, 1)
        combinations = [(x, y) for x in possible_values for y in possible_values]
        combinations.remove((0,0))

        for row_, col_ in combinations:
            if len(Board) > row+row_ >= 0 and len(Board) > col + col_ >= 0:
                if Board.Board[row+row_][col+col_] == 0 or Board.Board[row+row_][col+col_].color != self.color:
                    self.available_moves.append((row+row_,col+col_))

