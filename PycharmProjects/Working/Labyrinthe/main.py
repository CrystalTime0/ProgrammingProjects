import pygame
from constants import *
from labyrinthe import Labyrinthe
from solver import Solver

pygame.init()
clock = pygame.time.Clock()

Win = pygame.display.set_mode((WIDTH, HEIGHT))

def main() -> None:
    run = True
    Win.fill(WHITE)
    labyrinthe = Labyrinthe(Win)
    solver = Solver(Win, labyrinthe.labyrinthe)
    solver.solve("heat_map")
    labyrinthe.draw_labyrinthe_walls(WHITE)
    solver.draw_solution()


    #solver.draw_solution()

    while run:
        clock.tick(FPS)
        pygame.display.flip()
        for event in pygame.event.get():
            pass

if __name__ == '__main__':
    main()