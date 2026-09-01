import os
import pygame

# Configuration
FPS = 30

# Size
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE = WIDTH // ROWS
BOARD_OFFSET = (0, 240)

# Colors
BG = (47, 79, 79)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BEIGE = (238, 238, 210)
GREEN = (118, 150, 86)
GREY = (75, 72, 71)

# Images
IMG_PATH = "data/chess_images"

# Black pieces
Black_Knight = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bn.png")), (SQUARE, SQUARE))
Black_Bishop = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bb.png")), (SQUARE, SQUARE))
Black_King = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bk.png")), (SQUARE, SQUARE))
Black_pawn = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bp.png")), (SQUARE, SQUARE))
Black_Queen = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bq.png")), (SQUARE, SQUARE))
Black_Rook = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "br.png")), (SQUARE, SQUARE))

# White pieces
White_Knight = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wn.png")), (SQUARE, SQUARE))
White_Bishop = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wb.png")), (SQUARE, SQUARE))
White_King = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wk.png")), (SQUARE, SQUARE))
White_pawn = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wp.png")), (SQUARE, SQUARE))
White_Queen = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wq.png")), (SQUARE, SQUARE))
White_Rook = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wr.png")), (SQUARE, SQUARE))

# Notation standard internationale
PIECE_CODE = {
    "Pawn": "",
    "Knight": "N",
    "Bishop": "B",
    "Rook": "R",
    "Queen": "Q",
    "King": "K",
}

PIECE_TO_FEN = {
    "King": "k",
    "Queen": "q",
    "Rook": "r",
    "Bishop": "b",
    "Knight": "n",
    "Pawn": "p",
}

COL_NAME = "abcdefgh"