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

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()

        if self.color == WHITE:
            if row - 1>= 0:
                if Board[row - 1][col] == 0:
                    self.available_moves.append((row - 1, col))
                    if self.first_move and Board[row - 2][col] == 0:
                        self.available_moves.append((row - 2, col))

            if Board[row - 1][col - 1].color != self.color:
                self.available_moves.append((row - 1, col - 1))
            if Board[row - 1][col + 1].color != self.color:
                self.available_moves.append((row - 1, col + 1))

        if self.color == BLACK:
            if row + 1 <= len(Board):
                if Board[row + 1][col] == 0:
                    self.available_moves.append((row + 1, col))
                    if self.first_move and Board[row + 2][col] == 0:
                        self.available_moves.append((row + 2, col))

            if Board[row - 1][col - 1].color != self.color:
                self.available_moves.append((row - 1, col - 1))
            if Board[row - 1][col + 1].color != self.color:
                self.available_moves.append((row - 1, col + 1))

        # TO-DO : Rajouter En Passant


class Rook(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()

        for i in range(row, 0, -1):
            if Board[i-1][col] == 0:
                self.available_moves.append((i-1, col))
            else:
                break

        for i in range(row + 1, len(Board)):
            if Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                break

        for i in range(col, 0, -1):
            if Board[row][i-1] == 0:
                self.available_moves.append((row, i-1))
            else:
                break

        for i in range(col + 1, len(Board)):
            if Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                break

class Knight(Piece):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square, image, color, type, row, col)

    def get_available_moves(self, row, col, Board):
        self.clear_available_moves()
        
        if row - 2 >= 0:
            if col - 1 >= 0:
                self.available_moves.append((row-2, col-1))
            if col + 1 <= len(Board):
                self.available_moves.append((row-2, col+1))
        if row - 1 >= 0:
            if col - 2 >= 0:
                self.available_moves.append((row-1, col-2))
            if col + 2 <= len(Board):
                self.available_moves.append((row-1, col+2))
        if row + 1 <= len(Board):
            if col - 2 >= 0:
                self.available_moves.append((row+1, col-1))
            if col + 2 <= len(Board):
                self.available_moves.append((row+1, col+1))
        if row + 2 <= len(Board):
            if col - 1 >= 0:
                self.available_moves.append((row+2, col-2))
            if col + 1 <= len(Board):
                self.available_moves.append((row+2, col+2))


