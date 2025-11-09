import pygame
from Pieces import *
from constants import *


# noinspection PyRedundantParentheses
class NewBoard:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Width = Width
        self.Height = Height
        self.Square = Square
        self.Win = Win
        self.Rows = Rows
        self.Cols = Cols
        self.Board = []
        self.create_board()

    def create_board(self):
        for row in range(self.Rows):

            self.Board.append([0 for _ in range(self.Cols)])

            for col in range(self.Cols):
                pass

    def get_piece(self, row, col):
        return self.Board[row][col]

    def move(self, piece, row, col):
        self.Board[piece.row][piece.col], self.Board[row][col] = self.Board[row][col], self.Board[piece.row][piece.col]
        piece.piece_move(row, col)

        if piece.type == "Pawn":
            if piece.first_move:
                piece.first_move = False

    def draw_board(self):
        self.Win.fill(BEIGE)

        for row in range(Rows):
            for col in range(row % 2, Cols, 2):
                pygame.draw.rect(self.Win, GREEN, (Square * (row), Square * (col), Square, Square))

    @staticmethod
    def draw_piece(piece, Win):
        Win.blit(piece.image, (piece.x, piece.y))

    def draw_pieces(self):
        for row in range(self.Rows):
            for col in range(self.Cols):
                if self.Board[row][col] != 0:
                    self.draw_piece(self.Board[row][col], self.Win)
