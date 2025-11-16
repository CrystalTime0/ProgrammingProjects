import pygame.display

from board import NewBoard
from constants import *


class Game:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Width = Width
        self.Height = Height
        self.Rows = Rows
        self.Cols = Cols
        self.Square = Square
        self.Win = Win
        self.Board = NewBoard(Width, Height, Rows, Cols, Square, Win)
