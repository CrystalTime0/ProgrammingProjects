from typing import TYPE_CHECKING, Any, Optional

from constants import *
from Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook

if TYPE_CHECKING:
    from game import Game


class NewBoard:
    def __init__(self, win: pygame.Surface, game: Optional["Game"]):
        self.win = win
        self.game = game
        self.Board: list[list[Any]] = []
        self.create_board()

    def __len__(self) -> int:
        return len(self.Board)

    def create_board(self) -> None:
        self.Board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        for col in range(COLS):
            self.Board[1][col] = Pawn(Black_pawn, BLACK, "Pawn", 1, col, self.game)
            self.Board[6][col] = Pawn(White_pawn, WHITE, "Pawn", 6, col, self.game)

        # Pièces noires
        self.Board[0][0] = Rook(Black_Rook, BLACK, "Rook", 0, 0, self.game)
        self.Board[0][7] = Rook(Black_Rook, BLACK, "Rook", 0, 7, self.game)
        self.Board[0][1] = Knight(Black_Knight, BLACK, "Knight", 0, 1, self.game)
        self.Board[0][6] = Knight(Black_Knight, BLACK, "Knight", 0, 6, self.game)
        self.Board[0][2] = Bishop(Black_Bishop, BLACK, "Bishop", 0, 2, self.game)
        self.Board[0][5] = Bishop(Black_Bishop, BLACK, "Bishop", 0, 5, self.game)
        self.Board[0][3] = Queen(Black_Queen, BLACK, "Queen", 0, 3, self.game)
        self.Board[0][4] = King(Black_King, BLACK, "King", 0, 4, self.game)

        # Pièces blanches
        self.Board[7][0] = Rook(White_Rook, WHITE, "Rook", 7, 0, self.game)
        self.Board[7][7] = Rook(White_Rook, WHITE, "Rook", 7, 7, self.game)
        self.Board[7][1] = Knight(White_Knight, WHITE, "Knight", 7, 1, self.game)
        self.Board[7][6] = Knight(White_Knight, WHITE, "Knight", 7, 6, self.game)
        self.Board[7][2] = Bishop(White_Bishop, WHITE, "Bishop", 7, 2, self.game)
        self.Board[7][5] = Bishop(White_Bishop, WHITE, "Bishop", 7, 5, self.game)
        self.Board[7][3] = Queen(White_Queen, WHITE, "Queen", 7, 3, self.game)
        self.Board[7][4] = King(White_King, WHITE, "King", 7, 4, self.game)

    def get_piece(self, row: int, col: int) -> Any:
        return self.Board[row][col]

    def move(self, piece: Piece, row: int, col: int) -> None:
        self.Board[piece.row][piece.col] = 0
        self.Board[row][col] = piece
        piece.piece_move(row, col)

        if piece.type in ("Pawn", "Rook", "King") and getattr(piece, "first_move", False):
            piece.first_move = False

    def draw_board(self) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                color = BEIGE if (row + col) % 2 == 0 else GREEN
                pygame.draw.rect(
                    self.win,
                    color,
                    (
                        BOARD_OFFSET[0] + col * SQUARE,
                        BOARD_OFFSET[1] + row * SQUARE,
                        SQUARE,
                        SQUARE,
                    ),
                )

    @staticmethod
    def draw_piece(piece: Piece, win: pygame.Surface) -> None:
        win.blit(piece.image, (BOARD_OFFSET[0] + piece.x, BOARD_OFFSET[1] + piece.y))

    def draw_pieces(self) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.Board[row][col]
                if isinstance(piece, Piece):
                    self.draw_piece(piece, self.win)

    def get_fen(self) -> str:
        fen = []

        # 1. Placement des pièces
        rows = []
        for row in range(8):
            empty = 0
            row_fen = ""
            for col in range(8):
                piece = self.Board[row][col]
                if not isinstance(piece, Piece):
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
        fen.append("w" if self.game and self.game.turn == WHITE else "b")

        # 3. Roques
        castling = ""
        king_w = self.Board[7][4]
        if isinstance(king_w, King) and king_w.first_move:
            rook_k = self.Board[7][7]
            rook_q = self.Board[7][0]
            if isinstance(rook_k, Rook) and rook_k.first_move:
                castling += "K"
            if isinstance(rook_q, Rook) and rook_q.first_move:
                castling += "Q"

        king_b = self.Board[0][4]
        if isinstance(king_b, King) and king_b.first_move:
            rook_k = self.Board[0][7]
            rook_q = self.Board[0][0]
            if isinstance(rook_k, Rook) and rook_k.first_move:
                castling += "k"
            if isinstance(rook_q, Rook) and rook_q.first_move:
                castling += "q"

        fen.append(castling if castling else "-")

        # 4. En passant
        en_passant = "-"
        if self.game and self.game.total_turn > 1:
            last_move = self.game.past_moves_usable.get(self.game.total_turn - 1)
            if last_move:
                (sr, sc), (er, ec) = last_move
                piece = self.Board[er][ec]
                if isinstance(piece, Pawn) and abs(sr - er) == 2:
                    ep_row = (sr + er) // 2
                    en_passant = COL_NAME[ec] + str(8 - ep_row)

        fen.append(en_passant)

        # 5. Demi-coups (règle des 50 coups)
        nb_moves = self.game.nb_moves_from_last_capture if self.game else 0
        fen.append(str(nb_moves))

        # 6. Numéro du coup complet
        current_turn = self.game.current_turn if self.game else 1
        fen.append(str(current_turn))

        return " ".join(fen)