import pygame.display

from board import NewBoard
from constants import *


class Game:
    def __init__(self, width, height, rows, cols, square, win):
        self.Win = win
        self.Board = NewBoard(width, height, rows, cols, square, win)
        self.Square = square
        self.selected = None
        self.turn = WHITE
        self.valid_moves = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16

    # Afficher les élements
    def update_window(self):
        # TO-DO : all draw
        pygame.display.update()

    # Recréer un nouveau plateau
    def reset(self):
        pass

    # Vérifier les état ex: nombre de pieces restantes ou checkmate
    def check_game(self):
        pass

    # Renvoie une liste de tuple contenant toutes les cases accessible en 1 coup par l'adversaire
    def enemies_moves(self, piece, board) -> list[tuple]:
        pass

    def get_king_pos(self, board):
        pass

    def simulate_move(self, piece, row, col):
        pass

    def possible_moves(self, board):
        pass

    def checkmate(self, board):
        pass

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = BLACK

    def select(self, row, col):
        pass

    def _move(self, row, col):
        pass

    def remove(self, board, piece, row, col):
        if piece != 0:
            board[row][col] = 0
            if piece.color == WHITE:
                self.White_pieces_left -= 1
            else:
                self.Black_pieces_left -= 1
        print("White_pieces_left : ", self.White_pieces_left)
        print("Black_pieces_left : ", self.Black_pieces_left)

    def draw_available_moves(self):
        if len(self.valid_moves) > 0:
            for pos in self.valid_moves:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.Win, GREY,
                                   (col * self.Square + self.Square // 2, row * self.Square + self.Square // 2),
                                   self.Square // 8)

    def get_board(self):
        return self.Board
