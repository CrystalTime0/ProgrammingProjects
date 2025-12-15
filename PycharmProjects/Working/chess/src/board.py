from Pieces import *
from constants import *

import copy


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
                        self.Board[row][col] = Queen(self.Square, Black_Queen, BLACK, "Queen", row, col, self.game)
                    if col == 4:
                        self.Board[row][col] = King(self.Square, Black_King, BLACK, "King", row, col, self.game)
                if row == 7:
                    if col == 0 or col == 7:
                        self.Board[row][col] = Rook(self.Square, White_Rook, WHITE, "Rook", row, col, self.game)
                    if col == 1 or col == 6:
                        self.Board[row][col] = Knight(self.Square, White_Knight, WHITE, "Knight", row, col, self.game)
                    if col == 2 or col == 5:
                        self.Board[row][col] = Bishop(self.Square, White_Bishop, WHITE, "Bishop", row, col, self.game)
                    if col == 3:
                        self.Board[row][col] = Queen(self.Square, White_Queen, WHITE, "Queen", row, col, self.game)
                    if col == 4:
                        self.Board[row][col] = King(self.Square, White_King, WHITE, "King", row, col, self.game)

    def get_piece(self, row, col):
        return self.Board[row][col]

    def move(self, piece, row, col):
        self.Board[piece.row][piece.col], self.Board[row][col] = self.Board[row][col], self.Board[piece.row][piece.col]
        piece.piece_move(row, col)

        if piece.type == "Pawn" or piece.type == "Rook" or piece.type == "King":
            if piece.first_move:
                piece.first_move = False

    def draw_board(self):
        self.Win.fill(GREEN)

        for row in range(Rows):
            for col in range(row % 2, Cols, 2):
                pygame.draw.rect(self.Win, BEIGE, (Square * (row), Square * (col), Square, Square))

    @staticmethod
    def draw_piece(piece, Win):
        Win.blit(piece.image, (piece.x, piece.y))

    def draw_pieces(self):
        for row in range(self.Rows):
            for col in range(self.Cols):
                if self.Board[row][col] != 0:
                    self.draw_piece(self.Board[row][col], self.Win)

    def get_fen(self):
        fen = []

        # =========================
        # 1. Placement des pièces
        # =========================
        rows = []

        for row in range(8):
            empty = 0
            row_fen = ""

            for col in range(8):
                piece = self.Board[row][col]

                if piece == 0:
                    empty += 1
                else:
                    if empty > 0:
                        row_fen += str(empty)
                        empty = 0

                    char = PIECE_TO_FEN[piece.type]
                    if piece.color == WHITE:
                        char = char.upper()

                    row_fen += char

            if empty > 0:
                row_fen += str(empty)

            rows.append(row_fen)

        fen.append("/".join(rows))

        # =========================
        # 2. Trait
        # =========================
        fen.append("w" if self.game.turn == WHITE else "b")

        # =========================
        # 3. Roques
        # =========================
        castling = ""

        # Blanc
        king = self.Board[7][4]
        if king != 0 and king.type == "King" and king.first_move:
            rook_k = self.Board[7][7]
            rook_q = self.Board[7][0]
            if rook_k != 0 and rook_k.type == "Rook" and rook_k.first_move:
                castling += "K"
            if rook_q != 0 and rook_q.type == "Rook" and rook_q.first_move:
                castling += "Q"

        # Noir
        king = self.Board[0][4]
        if king != 0 and king.type == "King" and king.first_move:
            rook_k = self.Board[0][7]
            rook_q = self.Board[0][0]
            if rook_k != 0 and rook_k.type == "Rook" and rook_k.first_move:
                castling += "k"
            if rook_q != 0 and rook_q.type == "Rook" and rook_q.first_move:
                castling += "q"

        fen.append(castling if castling else "-")

        # =========================
        # 4. En passant
        # =========================
        en_passant = "-"

        if self.game.past_moves_usable:
            last_move = list(self.game.past_moves_usable.values())[-1]
            (sr, sc), (er, ec) = last_move

            piece = self.Board[er][ec]
            if piece != 0 and piece.type == "Pawn" and abs(sr - er) == 2:
                ep_row = (sr + er) // 2
                ep_col = ec
                en_passant = chr(ord('a') + ep_col) + str(8 - ep_row)

        fen.append(en_passant)

        # =========================
        # 5. Demi-coups (50-move rule)
        # =========================
        fen.append(str(self.game.nb_moves_from_last_capture))

        # =========================
        # 6. Numéro du coup
        # =========================
        fullmove = len(self.game.past_moves_usable) // 2 + 1
        fen.append(str(fullmove))

        return " ".join(fen)

    def __deepcopy__(self, memo):
        cls = self.__class__
        copy_board = cls.__new__(cls)
        memo[id(self)] = copy_board

        # Copier la grille
        copy_board.Board = [[copy.deepcopy(p, memo) if p != 0 else 0 for p in row] for row in self.Board]

        # Copier les autres attributs
        copy_board.Rows = self.Rows
        copy_board.Cols = self.Cols
        copy_board.Square = self.Square
        copy_board.Win = self.Win  # surfaces pygame restent les mêmes

        return copy_board
