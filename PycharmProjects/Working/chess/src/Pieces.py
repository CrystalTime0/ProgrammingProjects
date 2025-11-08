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
