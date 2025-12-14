import os
os.system("python data/chess_images/pieces_downloader.py")
from constants import *
from game import Game

pygame.init()
clock = pygame.time.Clock()

Win = pygame.display.set_mode((Width, Height))


def get_positions(x: int, y: int) -> tuple:
    row = y // Square
    col = x // Square

    return row, col

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
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if pygame.mouse.get_pressed()[0]:
                    location = pygame.mouse.get_pos()
                    row, col = get_positions(location[0], location[1])
                    # print(row,col)
                    game.select(row, col)

if __name__ == "__main__":
    main()