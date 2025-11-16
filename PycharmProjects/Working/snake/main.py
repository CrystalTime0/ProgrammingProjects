import pygame

from constants import *
from game import Game

pygame.init()
clock = pygame.time.Clock()

Win = pygame.display.set_mode((Width, Height))


def main() -> None:
    run = True
    game_over = False
    game = Game(Width, Height, Rows, Cols, Square, Win)

    while run:
        clock.tick(FPS)

        game.update_window()
        if game.check_game():
            game_over = True

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    game.command((0, 1))
                if event.key == pygame.K_DOWN:
                    game.command((0, -1))
                if event.key == pygame.K_RIGHT:
                    game.command((1, 0))
                if event.key == pygame.K_DOWN:
                    game.command((-1, 0))


if __name__ == "__main__":
    main()
