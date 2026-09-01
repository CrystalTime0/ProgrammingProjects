from typing import TYPE_CHECKING, Any, Optional
import pygame

from constants import (
    BLACK,
    COLS,
    ROWS,
    SQUARE,
    WHITE,
)

if TYPE_CHECKING:
    from game import Game


class Piece:
    def __init__(
        self,
        image: pygame.Surface,
        color: tuple[int, int, int],
        piece_type: str,
        row: int,
        col: int,
        game: Optional["Game"],
    ):
        self.image = image
        self.color = color
        self.row = row
        self.col = col
        self.type = piece_type
        self.x = 0
        self.y = 0
        self.available_moves: list[tuple[int, int]] = []
        self.game = game
        self.calc_pos()

    def piece_move(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.calc_pos()

    def calc_pos(self) -> None:
        self.x = self.col * SQUARE
        self.y = self.row * SQUARE

    def clear_available_moves(self) -> None:
        self.available_moves.clear()

    def get_available_moves(self, _board: Any, _ignore_checks: bool = False) -> list[tuple[int, int]]:
        return []

    def get_attack_squares(self, _board: Any) -> list[tuple[int, int]]:
        return []


class Pawn(Piece):
    def __init__(
        self,
        image: pygame.Surface,
        color: tuple[int, int, int],
        piece_type: str,
        row: int,
        col: int,
        game: Optional["Game"],
    ):
        super().__init__(image, color, piece_type, row, col, game)
        self.first_move = True

    def get_available_moves(self, board: Any, _ignore_checks: bool = False) -> list[tuple[int, int]]:
        self.clear_available_moves()
        row, col = self.row, self.col

        if self.color == WHITE:
            if row - 1 >= 0 and board.Board[row - 1][col] == 0:
                self.available_moves.append((row - 1, col))
                if self.first_move and row - 2 >= 0 and board.Board[row - 2][col] == 0:
                    self.available_moves.append((row - 2, col))

            for dc in (-1, 1):
                if 0 <= col + dc < COLS and row - 1 >= 0:
                    target = board.Board[row - 1][col + dc]
                    if isinstance(target, Piece) and target.color != self.color:
                        self.available_moves.append((row - 1, col + dc))

            if self.game and self.game.total_turn > 1:
                last_move = self.game.past_moves_usable.get(self.game.total_turn - 1)
                if last_move:
                    (sr, sc), (er, ec) = last_move
                    last_piece = board.Board[er][ec]
                    if (
                        isinstance(last_piece, Pawn)
                        and last_piece.color == BLACK
                        and abs(er - sr) == 2
                        and er == self.row
                        and abs(ec - col) == 1
                    ):
                        self.available_moves.append((row - 1, ec))

        elif self.color == BLACK:
            if row + 1 < ROWS and board.Board[row + 1][col] == 0:
                self.available_moves.append((row + 1, col))
                if self.first_move and row + 2 < ROWS and board.Board[row + 2][col] == 0:
                    self.available_moves.append((row + 2, col))

            for dc in (-1, 1):
                if 0 <= col + dc < COLS and row + 1 < ROWS:
                    target = board.Board[row + 1][col + dc]
                    if isinstance(target, Piece) and target.color != self.color:
                        self.available_moves.append((row + 1, col + dc))

            if self.game and self.game.total_turn > 1:
                last_move = self.game.past_moves_usable.get(self.game.total_turn - 1)
                if last_move:
                    (sr, sc), (er, ec) = last_move
                    last_piece = board.Board[er][ec]
                    if (
                        isinstance(last_piece, Pawn)
                        and last_piece.color == WHITE
                        and abs(er - sr) == 2
                        and er == self.row
                        and abs(ec - col) == 1
                    ):
                        self.available_moves.append((row + 1, ec))

        return self.available_moves

    def get_attack_squares(self, _board: Any) -> list[tuple[int, int]]:
        attack_squares = []
        row, col = self.row, self.col
        dr = -1 if self.color == WHITE else 1
        for dc in (-1, 1):
            nr, nc = row + dr, col + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                attack_squares.append((nr, nc))
        return attack_squares


class Rook(Piece):
    def __init__(
        self,
        image: pygame.Surface,
        color: tuple[int, int, int],
        piece_type: str,
        row: int,
        col: int,
        game: Optional["Game"],
    ):
        super().__init__(image, color, piece_type, row, col, game)
        self.first_move = True

    def get_available_moves(self, board: Any, _ignore_checks: bool = False) -> list[tuple[int, int]]:
        self.clear_available_moves()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < ROWS and 0 <= c < COLS:
                target = board.Board[r][c]
                if target == 0:
                    self.available_moves.append((r, c))
                else:
                    if isinstance(target, Piece) and target.color != self.color:
                        self.available_moves.append((r, c))
                    break
                r += dr
                c += dc

        return self.available_moves


class Knight(Piece):
    def get_available_moves(self, board: Any, _ignore_checks: bool = False) -> list[tuple[int, int]]:
        self.clear_available_moves()
        moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in moves:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                target = board.Board[r][c]
                if target == 0 or (isinstance(target, Piece) and target.color != self.color):
                    self.available_moves.append((r, c))

        return self.available_moves


class Bishop(Piece):
    def get_available_moves(self, board: Any, _ignore_checks: bool = False) -> list[tuple[int, int]]:
        self.clear_available_moves()
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < ROWS and 0 <= c < COLS:
                target = board.Board[r][c]
                if target == 0:
                    self.available_moves.append((r, c))
                else:
                    if isinstance(target, Piece) and target.color != self.color:
                        self.available_moves.append((r, c))
                    break
                r += dr
                c += dc

        return self.available_moves


class Queen(Piece):
    def get_available_moves(self, board: Any, _ignore_checks: bool = False) -> list[tuple[int, int]]:
        self.clear_available_moves()
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < ROWS and 0 <= c < COLS:
                target = board.Board[r][c]
                if target == 0:
                    self.available_moves.append((r, c))
                else:
                    if isinstance(target, Piece) and target.color != self.color:
                        self.available_moves.append((r, c))
                    break
                r += dr
                c += dc

        return self.available_moves


class King(Piece):
    def __init__(
        self,
        image: pygame.Surface,
        color: tuple[int, int, int],
        piece_type: str,
        row: int,
        col: int,
        game: Optional["Game"],
    ):
        super().__init__(image, color, piece_type, row, col, game)
        self.first_move = True

    def can_castle_kingside(self, board: Any) -> bool:
        row, col = self.row, self.col
        if col + 3 >= COLS:
            return False
        if board.Board[row][col + 1] != 0 or board.Board[row][col + 2] != 0:
            return False
        rook = board.Board[row][col + 3]
        if not isinstance(rook, Rook) or not rook.first_move:
            return False
        if not self.game:
            return False
        if (
            self.game.is_square_attacked(row, col, self.color)
            or self.game.is_square_attacked(row, col + 1, self.color)
            or self.game.is_square_attacked(row, col + 2, self.color)
        ):
            return False
        return True

    def can_castle_queenside(self, board: Any) -> bool:
        row, col = self.row, self.col
        if col - 4 < 0:
            return False
        if board.Board[row][col - 1] != 0 or board.Board[row][col - 2] != 0 or board.Board[row][col - 3] != 0:
            return False
        rook = board.Board[row][col - 4]
        if not isinstance(rook, Rook) or not rook.first_move:
            return False
        if not self.game:
            return False
        if (
            self.game.is_square_attacked(row, col, self.color)
            or self.game.is_square_attacked(row, col - 1, self.color)
            or self.game.is_square_attacked(row, col - 2, self.color)
        ):
            return False
        return True

    def get_available_moves(self, board: Any, ignore_checks: bool = False) -> list[tuple[int, int]]:
        self.clear_available_moves()
        row, col = self.row, self.col

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                target = board.Board[r][c]
                if target == 0 or (isinstance(target, Piece) and target.color != self.color):
                    self.available_moves.append((r, c))

        if self.first_move and not ignore_checks:
            if self.can_castle_kingside(board):
                self.available_moves.append((row, col + 2))
            if self.can_castle_queenside(board):
                self.available_moves.append((row, col - 2))

        return self.available_moves

    def get_attack_squares(self, _board: Any) -> list[tuple[int, int]]:
        attack_squares = []
        row, col = self.row, self.col
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                attack_squares.append((r, c))
        return attack_squares