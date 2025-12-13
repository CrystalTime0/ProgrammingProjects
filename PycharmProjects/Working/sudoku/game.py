import pygame
from constants import *
from sudoku_solver import SudokuVerifier
from sudoku_generator import generate_sudoku

class Game:
    def __init__(self, width, height, rows, cols, square, win):
        self.grid = generate_sudoku() # [[1 for _ in range(10)] for _ in range(10)]
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.square = square
        self.win = win
        self.selected: tuple = ()
        self.font = pygame.font.Font(None, 120)
        self.verifier = SudokuVerifier(self.grid)
        self.invalid_cases = []
        self.get_invalid_cases()

    def draw_grid(self):
        self.win.fill(WHITE)
        if self.selected:
            pygame.draw.rect(self.win, SELECT_BLUE, (self.square * (self.selected[0]), self.square * (self.selected[1]), self.square, self.square))
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != 0:
                    if (row,col) in self.invalid_cases:
                        self.win.blit(self.font.render(str(self.grid[row][col]),1, BLACK), (row * self.square + DIGIT_MARGIN, col * self.square + DIGIT_MARGIN))
                    else:
                        self.win.blit(self.font.render(str(self.grid[row][col]),1, DIGIT_BLUE), (row * self.square + DIGIT_MARGIN, col * self.square + DIGIT_MARGIN))
                else:
                    self.win.blit(self.font.render("",1, BLACK), (row * self.square + DIGIT_MARGIN, col * self.square + DIGIT_MARGIN))
        for row in range(self.rows):
            curr_line_size = LINE_SIZE
            if row%3==0:
               curr_line_size = LINE_SIZE*2
            pygame.draw.line(self.win, BLACK, (row * SQUARE,0),(row * SQUARE, HEIGHT), curr_line_size)
        for col in range(self.cols):
            curr_line_size = LINE_SIZE
            if col%3==0:
               curr_line_size = LINE_SIZE*2 
            pygame.draw.line(self.win, BLACK, (0, col * SQUARE),(WIDTH, col * SQUARE), curr_line_size)
    
    def get_invalid_cases(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] != 0:
                    self.invalid_cases.append((i,j))
                    

    def change_number(self, number):
        if self.selected and self.selected not in self.invalid_cases:
            row, col = self.selected[0], self.selected[1]
            self.grid[row][col] = number
    
    def check(self):
        return self.verifier.verif_grid()

    def update_window(self):
        self.draw_grid()
        pygame.display.update()


    def select(self, row, col):
        if row < self.rows and col < self.cols:
            self.selected = col, row