import os
import subprocess
import sys
import pygame

downloader = os.path.join("data", "chess_images", "pieces_downloader.py")
if os.path.exists(downloader):
    subprocess.run([sys.executable, downloader], check=False)

from constants import FPS
from game import Game

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((480, 960))


def main() -> None:
    run = True
    game_over = False
    game = Game(win)

    while run:
        clock.tick(FPS)

        game.update_window()
        if not game_over and game.check_game():
            game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if pygame.mouse.get_pressed()[0]:
                    location = pygame.mouse.get_pos()
                    game.handle_click(location)

    pygame.quit()


if __name__ == "__main__":
    main()