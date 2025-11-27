import pygame
from constants import *

class Game:
    def __init__(self, width, height, rows, cols, square, win):
        self.grid = [[1 for _ in range(10)] for _ in range(10)]
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.square = square
        self.win = win
        self.selected: tuple = ()
        self.font = pygame.font.Font(None, 120)

    def draw_grid(self):
        self.win.fill(WHITE)
        if self.selected:
            pygame.draw.rect(self.win, BLUE, (self.square * (self.selected[0]), self.square * (self.selected[1]), self.square, self.square))
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != 0:
                    self.win.blit(self.font.render(str(self.grid[row][col]),1, BLACK), (row * self.square, col * self.square))
        for row in range(self.rows):
            pygame.draw.line(self.win, BLACK, (row * SQUARE,0),(row * SQUARE, HEIGHT))
        for col in range(self.cols):
            pygame.draw.line(self.win, BLACK, (0, col * SQUARE),(WIDTH, col * SQUARE))

    def change_number(self, number):
        if self.selected:
            row, col = self.selected[0], self.selected[1]
            self.grid[row][col] = number

    def update_window(self):
        self.draw_grid()
        pygame.display.update()


    def select(self, row, col):
        self.selected = col, row
        #TO-DO couleur bleu sur la case sélectionné


