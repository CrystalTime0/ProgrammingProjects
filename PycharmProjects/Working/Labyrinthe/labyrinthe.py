import pygame
import random
from constants import *

class Labyrinthe:
    def __init__(self, win):
        self.win = win
        self.labyrinthe: dict = {}
        self.generate_labyrinthe()

    def generate_labyrinthe(self):
        def is_differents_id(labyrinthe):
            first_cell_id = labyrinthe[(0, 0)][0]
            for coordinate in labyrinthe.keys():
                if labyrinthe[coordinate][0] != first_cell_id:
                    return True
            return False

        tmp_labyrinthe = {(x, y): [x * ROWS + y, []] for x in range(ROWS) for y in range(COLS)} #[id, ways]
        while is_differents_id(tmp_labyrinthe):
            tmp_cell = random.choice(list(tmp_labyrinthe.keys()))
            direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            next_cell = (tmp_cell[0] + direction[0], tmp_cell[1] + direction[1])
            if next_cell in tmp_labyrinthe:
                if tmp_labyrinthe[tmp_cell][0] != tmp_labyrinthe[next_cell][0]:
                    old_id = tmp_labyrinthe[next_cell][0]
                    new_id = tmp_labyrinthe[tmp_cell][0]
                    for cell in tmp_labyrinthe:
                        if tmp_labyrinthe[cell][0] == old_id:
                            tmp_labyrinthe[cell][0] = new_id
                    tmp_labyrinthe[tmp_cell][1].append(next_cell)
                    tmp_labyrinthe[next_cell][1].append(tmp_cell)

        for cell in tmp_labyrinthe.keys():
            tmp_labyrinthe[cell] = tmp_labyrinthe[cell][1]
        self.labyrinthe = tmp_labyrinthe

    def draw_labyrinthe_walls(self, color):
        # Collecter tous les passages existants
        possible_ways = set()
        for cell, ways in self.labyrinthe.items():
            for way in ways:
                # Stocker en tuple ordonné pour éviter les doublons (A,B) == (B,A)
                possible_ways.add((min(cell, way), max(cell, way)))

        # Parcourir toutes les cellules et vérifier les voisins
        for (a, b) in self.labyrinthe.keys():
            for (c, d) in [(a + 1, b), (a, b + 1)]:  # voisin droite et voisin bas
                if (c, d) in self.labyrinthe:
                    edge = (min((a, b), (c, d)), max((a, b), (c, d)))
                    if edge not in possible_ways:  # pas de passage = c'est un mur
                        wall_pos = ()
                        if b == d:  # même ligne → mur vertical
                            x = max(a, c)
                            wall_pos = (x, b), (x, b + 1)
                        elif a == c:  # même colonne → mur horizontal
                            y = max(b, d)
                            wall_pos = (a, y), (a + 1, y)

                        p1 = (wall_pos[0][0] * SQUARE, wall_pos[0][1] * SQUARE)
                        p2 = (wall_pos[1][0] * SQUARE, wall_pos[1][1] * SQUARE)
                        pygame.draw.line(self.win, color, p1, p2)