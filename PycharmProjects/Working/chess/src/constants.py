import pygame
import os

# Configuration
FPS = 30

# Size
Width, Height = 760, 760
Rows, Cols = 8, 8
Square = Width // Rows

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
Black_Knight = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bn.png")), (Square, Square))
Black_Bishop = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bb.png")), (Square, Square))
Black_King = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bk.png")), (Square, Square))
Black_pawn = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bp.png")), (Square, Square))
Black_Queen = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "bq.png")), (Square, Square))
Black_Rook = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "br.png")), (Square, Square))
# White pieces
White_Knight = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wn.png")), (Square, Square))
White_Bishop = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wb.png")), (Square, Square))
White_King = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wk.png")), (Square, Square))
White_pawn = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wp.png")), (Square, Square))
White_Queen = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wq.png")), (Square, Square))
White_Rook = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, "wr.png")), (Square, Square))

# piece_code
piece_code =  {
    "Pawn": "",
    "Bishop": "B",
    "Rook": "R",
    "King": "K",
    "Queen": "Q",
    "Knight": "C",
    }
col_name = "abcdefgh"