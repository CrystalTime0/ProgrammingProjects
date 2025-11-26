from Pieces import *
from constants import *


# noinspection PyRedundantParentheses
class NewBoard:
    def __init__(self, Width, Height, Rows, Cols, Square, Win, game):
        self.Width = Width
        self.Height = Height
        self.Square = Square
        self.Win = Win
        self.Rows = Rows
        self.Cols = Cols
        self.Board = []
        self.game = game
        self.create_board()

    def __len__(self):
        return len(self.Board)

    def create_board(self):
        for row in range(self.Rows):

            self.Board.append([0 for _ in range(self.Cols)])

            for col in range(self.Cols):
                if row == 1:
                    self.Board[row][col] = Pawn(self.Square, Black_pawn, BLACK, "Pawn", row, col, self.game)
                if row == 6:
                    self.Board[row][col] = Pawn(self.Square, White_pawn, WHITE, "Pawn", row, col, self.game)
                if row == 0:
                    if col == 0 or col == 7:
                        self.Board[row][col] = Rook(self.Square, Black_Rook, BLACK, "Rook", row, col, self.game)
                    if col == 1 or col == 6:
                        self.Board[row][col] = Knight(self.Square, Black_Knight, BLACK, "Knight", row, col, self.game)
                    if col == 2 or col == 5:
                        self.Board[row][col] = Bishop(self.Square, Black_Bishop, BLACK, "Bishop", row, col, self.game)
                    if col == 3:
                        self.Board[row][col] = King(self.Square, Black_King, BLACK, "King", row, col, self.game)
                    if col == 4:
                        self.Board[row][col] = Queen(self.Square, Black_Queen, BLACK, "Queen", row, col, self.game)
                if row == 7:
                    if col == 0 or col == 7:
                        self.Board[row][col] = Rook(self.Square, White_Rook, WHITE, "Rook", row, col, self.game)
                    if col == 1 or col == 6:
                        self.Board[row][col] = Knight(self.Square, White_Knight, WHITE, "Knight", row, col, self.game)
                    if col == 2 or col == 5:
                        self.Board[row][col] = Bishop(self.Square, White_Bishop, WHITE, "Bishop", row, col, self.game)
                    if col == 3:
                        self.Board[row][col] = King(self.Square, White_King, WHITE, "King", row, col, self.game)
                    if col == 4:
                        self.Board[row][col] = Queen(self.Square, White_Queen, WHITE, "Queen", row, col, self.game)

    def get_piece(self, row, col):
        return self.Board[row][col]

    def move(self, piece, row, col):
        self.Board[piece.row][piece.col], self.Board[row][col] = self.Board[row][col], self.Board[piece.row][piece.col]
        piece.piece_move(row, col)

        if piece.type == "Pawn":
            if piece.first_move:
                piece.first_move = False

    def draw_board(self):
        self.Win.fill(BEIGE)

        for row in range(Rows):
            for col in range(row % 2, Cols, 2):
                pygame.draw.rect(self.Win, GREEN, (Square * (row), Square * (col), Square, Square))

    @staticmethod
    def draw_piece(piece, Win):
        Win.blit(piece.image, (piece.x, piece.y))

    def draw_pieces(self):
        for row in range(self.Rows):
            for col in range(self.Cols):
                if self.Board[row][col] != 0:
                    self.draw_piece(self.Board[row][col], self.Win)

