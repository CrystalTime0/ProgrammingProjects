from constants import *
import os
import json

# noinspection PyRedundantParentheses
class NewGrid:
    def __init__(self, width, height, rows, cols, square, win):
        self.width = width
        self.height = height
        self.square = square
        self.win = win
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.create_grid()

    def __len__(self):
        return len(self.grid)

    def create_grid(self):
        if os.path.exists(GRID_PATH):
            if os.path.getsize(GRID_PATH) > 0:
                with open(GRID_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    correspondances = [item["grid"] for item in data if item.get("name") == SAVED_GRID_NAME]
                    if correspondances:
                        self.grid = correspondances[0]
                        return

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw_board(self):
        self.win.fill(WHITE)

    def draw_lines(self):
        for row in range(self.rows):
            pygame.draw.line(self.win, BLACK, (row * SQUARE, 0), (row * SQUARE, HEIGHT))
        for col in range(self.cols):
            pygame.draw.line(self.win, BLACK, (0, col * SQUARE), (WIDTH, col * SQUARE))

    def draw_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 0:
                    pygame.draw.rect(self.win, WHITE, (SQUARE * (col), SQUARE * (row), SQUARE, SQUARE))
                if self.grid[row][col] == 1:
                    pygame.draw.rect(self.win, BLACK, (SQUARE * (col), SQUARE * (row), SQUARE, SQUARE))
