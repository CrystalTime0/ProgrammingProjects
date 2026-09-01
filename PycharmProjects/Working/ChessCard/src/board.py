import copy
from Pieces import *
from constants import *


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
        self.Board = [[0 for _ in range(self.Cols)] for _ in range(self.Rows)]

        for col in range(self.Cols):
            self.Board[1][col] = Pawn(self.Square, Black_pawn, BLACK, "Pawn", 1, col, self.game)
            self.Board[6][col] = Pawn(self.Square, White_pawn, WHITE, "Pawn", 6, col, self.game)

        # Pièces noires
        self.Board[0][0] = Rook(self.Square, Black_Rook, BLACK, "Rook", 0, 0, self.game)
        self.Board[0][7] = Rook(self.Square, Black_Rook, BLACK, "Rook", 0, 7, self.game)
        self.Board[0][1] = Knight(self.Square, Black_Knight, BLACK, "Knight", 0, 1, self.game)
        self.Board[0][6] = Knight(self.Square, Black_Knight, BLACK, "Knight", 0, 6, self.game)
        self.Board[0][2] = Bishop(self.Square, Black_Bishop, BLACK, "Bishop", 0, 2, self.game)
        self.Board[0][5] = Bishop(self.Square, Black_Bishop, BLACK, "Bishop", 0, 5, self.game)
        self.Board[0][3] = Queen(self.Square, Black_Queen, BLACK, "Queen", 0, 3, self.game)
        self.Board[0][4] = King(self.Square, Black_King, BLACK, "King", 0, 4, self.game)

        # Pièces blanches
        self.Board[7][0] = Rook(self.Square, White_Rook, WHITE, "Rook", 7, 0, self.game)
        self.Board[7][7] = Rook(self.Square, White_Rook, WHITE, "Rook", 7, 7, self.game)
        self.Board[7][1] = Knight(self.Square, White_Knight, WHITE, "Knight", 7, 1, self.game)
        self.Board[7][6] = Knight(self.Square, White_Knight, WHITE, "Knight", 7, 6, self.game)
        self.Board[7][2] = Bishop(self.Square, White_Bishop, WHITE, "Bishop", 7, 2, self.game)
        self.Board[7][5] = Bishop(self.Square, White_Bishop, WHITE, "Bishop", 7, 5, self.game)
        self.Board[7][3] = Queen(self.Square, White_Queen, WHITE, "Queen", 7, 3, self.game)
        self.Board[7][4] = King(self.Square, White_King, WHITE, "King", 7, 4, self.game)

    def get_piece(self, row, col):
        return self.Board[row][col]

    def move(self, piece, row, col):
        self.Board[piece.row][piece.col] = 0
        self.Board[row][col] = piece
        piece.piece_move(row, col)

        if piece.type in ("Pawn", "Rook", "King") and getattr(piece, "first_move", False):
            piece.first_move = False

    def draw_board(self):
        for row in range(self.Rows):
            for col in range(self.Cols):
                color = BEIGE if (row + col) % 2 == 0 else GREEN
                pygame.draw.rect(self.Win, color, (BOARD_OFFSET[0] + col * self.Square, BOARD_OFFSET[1] + row * self.Square, self.Square, self.Square))

    def draw_piece(self, piece, Win):
        Win.blit(piece.image, (BOARD_OFFSET[0] + piece.x, BOARD_OFFSET[1] + piece.y))

    def draw_pieces(self):
        for row in range(self.Rows):
            for col in range(self.Cols):
                piece = self.Board[row][col]
                if piece != 0:
                    self.draw_piece(piece, self.Win)

    def get_fen(self):
        fen = []

        # 1. Placement des pièces
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

        # 2. Trait
        fen.append("w" if self.game.turn == WHITE else "b")

        # 3. Roques
        castling = ""
        # Blanc
        king_w = self.Board[7][4]
        if king_w != 0 and king_w.type == "King" and getattr(king_w, "first_move", False):
            rook_k = self.Board[7][7]
            rook_q = self.Board[7][0]
            if rook_k != 0 and rook_k.type == "Rook" and getattr(rook_k, "first_move", False):
                castling += "K"
            if rook_q != 0 and rook_q.type == "Rook" and getattr(rook_q, "first_move", False):
                castling += "Q"

        # Noir
        king_b = self.Board[0][4]
        if king_b != 0 and king_b.type == "King" and getattr(king_b, "first_move", False):
            rook_k = self.Board[0][7]
            rook_q = self.Board[0][0]
            if rook_k != 0 and rook_k.type == "Rook" and getattr(rook_k, "first_move", False):
                castling += "k"
            if rook_q != 0 and rook_q.type == "Rook" and getattr(rook_q, "first_move", False):
                castling += "q"

        fen.append(castling if castling else "-")

        # 4. En passant
        en_passant = "-"
        if self.game.total_turn > 1:
            last_move = self.game.past_moves_usable.get(self.game.total_turn - 1)
            if last_move:
                (sr, sc), (er, ec) = last_move
                piece = self.Board[er][ec]
                if piece != 0 and piece.type == "Pawn" and abs(sr - er) == 2:
                    ep_row = (sr + er) // 2
                    en_passant = col_name[ec] + str(8 - ep_row)

        fen.append(en_passant)

        # 5. Demi-coups (règle des 50 coups)
        fen.append(str(self.game.nb_moves_from_last_capture))

        # 6. Numéro du coup complet
        fen.append(str(self.game.current_turn))

        return " ".join(fen)

    def __deepcopy__(self, memo):
        cls = self.__class__
        copy_board = cls.__new__(cls)
        memo[id(self)] = copy_board

        copy_board.Board = [[copy.deepcopy(p, memo) if p != 0 else 0 for p in row] for row in self.Board]
        copy_board.Rows = self.Rows
        copy_board.Cols = self.Cols
        copy_board.Square = self.Square
        copy_board.Win = self.Win
        copy_board.game = None

        return copy_board