from constants import *
from game import Game

pygame.init()
clock = pygame.time.Clock()

Win = pygame.display.set_mode((WIDTH, HEIGHT))


def get_positions(x: int, y: int) -> tuple:
    row = y // SQUARE
    col = x // SQUARE

    return row, col


def main() -> None:
    run = True
    game_over = False
    game = Game(WIDTH, HEIGHT, ROWS, COLS, SQUARE, Win)

    while run:
        clock.tick(FPS)

        game.update_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game.simulation_on:
                if pygame.mouse.get_pressed()[0]:
                    location = pygame.mouse.get_pos()
                    row, col = get_positions(location[0], location[1])
                    print(row, col)
                    game.change_cell(row, col)
            if event.type == pygame.KEYDOWN and not game.simulation_on:
                if event.key in (49, 50, 51, 52, 53, 54, 55, 56, 57):
                    game.next_generations(event.key-48)


if __name__ == "__main__":
    main()
