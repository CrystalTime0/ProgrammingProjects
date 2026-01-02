import pygame
import sys
import copy
import json

# ======================
# CONFIG
# ======================
CELL_SIZE = 40
MARGIN = 50
STONE_RADIUS = 18
BTN_HEIGHT = 40

BG_COLOR = (199, 167, 120)
LINE_COLOR = (0, 0, 0)
BLACK = (20, 20, 20)
WHITE = (235, 235, 235)
GRAY = (160, 160, 160)

BOARD_SIZES = {1: 9, 2: 13, 3: 19}

# ======================
# OUTILS GO
# ======================
def neighbors(x, y, size):
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            yield nx, ny

def get_group(board, x, y, visited=None):
    if visited is None:
        visited = set()
    color = board[x][y]
    group = {(x, y)}
    visited.add((x, y))
    for nx, ny in neighbors(x, y, len(board)):
        if (nx, ny) not in visited and board[nx][ny] == color:
            group |= get_group(board, nx, ny, visited)
    return group

def has_liberty(board, group):
    for x, y in group:
        for nx, ny in neighbors(x, y, len(board)):
            if board[nx][ny] == 0:
                return True
    return False

def remove_group(board, group):
    for x, y in group:
        board[x][y] = 0

# ======================
# SCORE
# ======================
def calculate_score(board, captures):
    size = len(board)
    visited = set()
    territory = {1: 0, 2: 0}

    for x in range(size):
        for y in range(size):
            if board[x][y] == 0 and (x, y) not in visited:
                region = set()
                borders = set()
                stack = [(x, y)]

                while stack:
                    cx, cy = stack.pop()
                    if (cx, cy) in visited:
                        continue
                    visited.add((cx, cy))
                    region.add((cx, cy))

                    for nx, ny in neighbors(cx, cy, size):
                        if board[nx][ny] == 0:
                            stack.append((nx, ny))
                        else:
                            borders.add(board[nx][ny])

                if len(borders) == 1:
                    territory[borders.pop()] += len(region)

    score_black = territory[1] + captures[1]
    score_white = territory[2] + captures[2]

    return score_black, score_white

# ======================
# JEU
# ======================
class GoGame:
    def __init__(self, size):
        self.size = size
        self.board = [[0]*size for _ in range(size)]
        self.turn = 1
        self.previous_board = None
        self.history = []
        self.captures = {1: 0, 2: 0}
        self.pass_count = 0

    def save_state(self):
        self.history.append((copy.deepcopy(self.board), self.turn,
                             copy.deepcopy(self.captures)))

    def undo(self):
        if self.history:
            self.board, self.turn, self.captures = self.history.pop()

    def play(self, x, y):
        if self.board[x][y] != 0:
            return False

        self.save_state()
        new_board = copy.deepcopy(self.board)
        new_board[x][y] = self.turn
        opponent = 2 if self.turn == 1 else 1
        captured_stones = 0

        for nx, ny in neighbors(x, y, self.size):
            if new_board[nx][ny] == opponent:
                group = get_group(new_board, nx, ny)
                if not has_liberty(new_board, group):
                    captured_stones += len(group)
                    remove_group(new_board, group)

        group = get_group(new_board, x, y)
        if not has_liberty(new_board, group) and captured_stones == 0:
            self.history.pop()
            return False

        if self.previous_board and new_board == self.previous_board:
            self.history.pop()
            return False

        self.previous_board = copy.deepcopy(self.board)
        self.board = new_board
        self.captures[self.turn] += captured_stones
        self.turn = opponent
        self.pass_count = 0
        return True

    def pass_turn(self):
        self.save_state()
        self.turn = 2 if self.turn == 1 else 1
        self.pass_count += 1

    def save_game(self):
        with open("save_go.json", "w") as f:
            json.dump({
                "board": self.board,
                "turn": self.turn,
                "captures": self.captures
            }, f)

    def load_game(self):
        try:
            with open("save_go.json", "r") as f:
                data = json.load(f)
                self.board = data["board"]
                self.turn = data["turn"]
                self.captures = data["captures"]
        except:
            pass

# ======================
# UI
# ======================
def draw_button(screen, rect, text, font):
    pygame.draw.rect(screen, GRAY, rect)
    label = font.render(text, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))

def draw_board(screen, game, font):
    screen.fill(BG_COLOR)
    size = game.size

    for i in range(size):
        pos = MARGIN + i * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR,
                         (MARGIN, pos),
                         (MARGIN + CELL_SIZE*(size-1), pos))
        pygame.draw.line(screen, LINE_COLOR,
                         (pos, MARGIN),
                         (pos, MARGIN + CELL_SIZE*(size-1)))

    for x in range(size):
        for y in range(size):
            if game.board[x][y]:
                color = BLACK if game.board[x][y] == 1 else WHITE
                pygame.draw.circle(
                    screen, color,
                    (MARGIN + x*CELL_SIZE, MARGIN + y*CELL_SIZE),
                    STONE_RADIUS
                )

    sb, sw = calculate_score(game.board, game.captures)
    txt = font.render(f"Noir: {sb}  Blanc: {sw}", True, BLACK)
    screen.blit(txt, (10, 5))

# ======================
# MAIN
# ======================
def choose_size():
    print("1: 9x9  2: 13x13  3: 19x19")
    return BOARD_SIZES.get(int(input("> ")), 9)

def main():
    size = choose_size()
    pygame.init()
    font = pygame.font.SysFont(None, 24)

    screen_w = MARGIN*2 + CELL_SIZE*(size-1)
    screen_h = screen_w + BTN_HEIGHT + 10
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Jeu de Go")

    game = GoGame(size)

    pass_btn = pygame.Rect(10, screen_w+5, 100, BTN_HEIGHT)
    undo_btn = pygame.Rect(120, screen_w+5, 100, BTN_HEIGHT)
    save_btn = pygame.Rect(230, screen_w+5, 100, BTN_HEIGHT)
    load_btn = pygame.Rect(340, screen_w+5, 100, BTN_HEIGHT)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        draw_board(screen, game, font)
        draw_button(screen, pass_btn, "Passer", font)
        draw_button(screen, undo_btn, "Annuler", font)
        draw_button(screen, save_btn, "Sauver", font)
        draw_button(screen, load_btn, "Charger", font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pass_btn.collidepoint(event.pos):
                    game.pass_turn()
                elif undo_btn.collidepoint(event.pos):
                    game.undo()
                elif save_btn.collidepoint(event.pos):
                    game.save_game()
                elif load_btn.collidepoint(event.pos):
                    game.load_game()
                else:
                    mx, my = event.pos
                    x = round((mx - MARGIN) / CELL_SIZE)
                    y = round((my - MARGIN) / CELL_SIZE)
                    if 0 <= x < size and 0 <= y < size:
                        game.play(x, y)

if __name__ == "__main__":
    main()
