import pygame
from constants import *
from utils import make_heat_to_rgb

class Solver:
    def __init__(self, win, labyrinthe):
        self.win = win
        self.labyrinthe = labyrinthe
        self.solution = None
        self.font = pygame.font.Font(None, SQUARE)

    def solve_with_division(self):
        possibles_ways = [[(0, 0)]]

        while possibles_ways:
            new_ways = []

            for way in possibles_ways:
                next_cells = list(self.labyrinthe[way[-1]])

                next_cells = [c for c in next_cells if c not in way]

                if not next_cells:
                    continue

                for cell in next_cells:
                    if cell == (ROWS - 1, COLS - 1):
                        return way + [cell]

                for cell in next_cells:
                    new_ways.append(way + [cell])

            possibles_ways = new_ways

        return None

    def solve_with_heat_map(self):
        heat_map = {}
        last_cells = [(ROWS - 1, COLS - 1)]
        new_cells = []
        heat = 0
        while len(heat_map) != ROWS * COLS:
            for cell in last_cells:
                heat_map[cell] = heat
            for cell in last_cells:
                for next_cell in self.labyrinthe[cell]:
                    if next_cell in heat_map:
                        continue
                    new_cells.append(next_cell)
            last_cells = list(new_cells)
            new_cells = []
            heat += 1
        heat_to_rgb = make_heat_to_rgb(list(heat_map.values()))
        for cell, heat in heat_map.items():
            color = heat_to_rgb(heat)
            pygame.draw.rect(self.win, color, (cell[0] * SQUARE, cell[1] * SQUARE, SQUARE, SQUARE))
            # self.win.blit(self.font.render(str(heat), False, WHITE), (cell[0] * SQUARE, cell[1] * SQUARE))

        solution = [(0, 0)]
        heat = heat_map[solution[0]]
        while heat != 0:
            solution.append(min(self.labyrinthe[solution[-1]], key=lambda cell_: heat_map[cell_]))
            heat -= 1
        assert solution[-1] == (ROWS - 1, COLS - 1)
        return solution

    def draw_solution(self):
        for cell in self.solution:
            pygame.draw.rect(self.win, GREEN, (cell[0] * SQUARE + SQUARE//4, cell[1] * SQUARE + SQUARE//4, SQUARE//2, SQUARE//2))

    def solve(self, mode):
        match mode:
            case "division":
                self.solution = self.solve_with_division()
            case "heat_map":
                self.solution = self.solve_with_heat_map()