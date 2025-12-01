import time

import pygame.display

from grid import NewGrid
from constants import *


class Game:
    def __init__(self, width, height, rows, cols, square, win):
        self.win = win
        self.grid = NewGrid(width, height, rows, cols, square, win)
        self.Square = square
        self.generation = 0
        self.simulation_on = False

    # Afficher les élements
    def update_window(self):
        self.grid.draw_board()
        self.grid.draw_cells()
        self.grid.draw_lines()
        pygame.display.update()

    def next_generations(self, num: int):
        self.simulation_on = True
        for _ in range(num):
            new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            for row in range(1, ROWS-1):
                for col in range(1, COLS-1):
                    n_cell = []
                    possible_values = (-1, 0, 1)
                    combinations = [(x, y) for x in possible_values for y in possible_values]
                    combinations.remove((0, 0))
                    for i in range(8):
                        n_cell.append(self.grid.grid[row + combinations[i][0]][col + combinations[i][1]])
                    # under population
                    if n_cell.count(1) < 2:
                        new_grid[row][col] = 0
                    if n_cell.count(1) > 3:
                        new_grid[row][col] = 0
                    if n_cell.count(1) == 2:
                        new_grid[row][col] = self.grid.grid[row][col]
                    if n_cell.count(1) == 3:
                        new_grid[row][col] = 1
            time.sleep(0.1)
            self.grid.grid = new_grid
            self.update_window()
        self.simulation_on = False

    def change_cell(self, row, col):
        cell = self.grid.grid[row][col]
        if cell == 1:
            cell = 0
        else:
            cell = 1
        print(row, col)
        self.grid.grid[row][col] = cell

    # Recréer une nouvelle grille
    def reset(self):
        self.grid = NewBoard(WIDTH, HEIGHT, ROWS, COLS, SQUARE, self.Win)
        self.Square = Square
