import datetime
from typing import Any, Optional

from constants import *
from Pieces import Bishop, Knight, Piece, Queen, Rook
from board import NewBoard


class Game:
    def __init__(self, win: pygame.Surface):
        self.win = win
        self.turn = WHITE
        self.selected: Optional[Piece] = None
        self.valid_moves: list[tuple[int, int]] = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.current_turn = 1
        self.total_turn = 1
        self.past_moves_code: dict[int, tuple[str, ...]] = {}
        self.past_moves_usable: dict[int, tuple[tuple[int, int], tuple[int, int]]] = {}
        self.nb_moves_from_last_capture = 0
        self.Board = NewBoard(win, self)

    def update_window(self) -> None:
        self.Board.draw_board()
        self.Board.draw_pieces()
        self.draw_available_moves()
        pygame.display.update()

    def reset(self) -> None:
        self.turn = WHITE
        self.selected = None
        self.valid_moves = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.current_turn = 1
        self.total_turn = 1
        self.past_moves_code.clear()
        self.past_moves_usable.clear()
        self.nb_moves_from_last_capture = 0
        self.Board = NewBoard(self.win, self)

    @staticmethod
    def get_positions_on_board(x: int, y: int) -> tuple[int, int]:
        row = y // SQUARE
        col = x // SQUARE
        return row, col

    def check_game(self) -> bool:
        if self.checkmate(self.Board):
            winner = "Black" if self.turn == WHITE else "White"
            print(f"Checkmate! {winner} wins.")
            return True
        return False

    @staticmethod
    def enemies_moves(color: tuple[int, int, int], board: NewBoard) -> list[tuple[int, int]]:
        moves = []
        for r in range(ROWS):
            for c in range(COLS):
                piece = board.Board[r][c]
                if isinstance(piece, Piece) and piece.color != color:
                    if piece.type in ("King", "Pawn"):
                        moves.extend(piece.get_attack_squares(board))
                    else:
                        moves.extend(piece.get_available_moves(board))
        return moves

    def is_square_attacked(self, row: int, col: int, color: tuple[int, int, int]) -> bool:
        return (row, col) in self.enemies_moves(color, self.Board)

    def get_king_pos(self, board: NewBoard, color: Optional[tuple[int, int, int]] = None) -> tuple[int, int]:
        target_color = color if color else self.turn
        for r in range(ROWS):
            for c in range(COLS):
                piece = board.Board[r][c]
                if isinstance(piece, Piece) and piece.type == "King" and piece.color == target_color:
                    return r, c
        raise ValueError("King not found on board")

    def create_piece(self, piece_type: str, color: tuple[int, int, int], row: int, col: int) -> Piece:
        mapping = {
            "Queen": (Queen, White_Queen if color == WHITE else Black_Queen),
            "Rook": (Rook, White_Rook if color == WHITE else Black_Rook),
            "Bishop": (Bishop, White_Bishop if color == WHITE else Black_Bishop),
            "Knight": (Knight, White_Knight if color == WHITE else Black_Knight),
        }
        cls, img = mapping[piece_type]
        return cls(img, color, piece_type, row, col, self)

    def promote_pawn(self, pawn: Piece) -> Piece:
        popup_x = HEIGHT // 2 - 2 * SQUARE
        popup_y = (WIDTH - SQUARE) // 2

        options = ["Queen", "Rook", "Bishop", "Knight"]
        option_images = (
            [White_Queen, White_Rook, White_Bishop, White_Knight]
            if pawn.color == WHITE
            else [Black_Queen, Black_Rook, Black_Bishop, Black_Knight]
        )

        while True:
            self.Board.draw_board()
            self.Board.draw_pieces()

            for i, img in enumerate(option_images):
                rect = pygame.Rect(
                    BOARD_OFFSET[0] + popup_x + i * SQUARE,
                    BOARD_OFFSET[1] + popup_y,
                    SQUARE,
                    SQUARE,
                )
                pygame.draw.rect(self.win, GREY, rect)
                self.win.blit(img, (rect.x, rect.y))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for i in range(4):
                        rect = pygame.Rect(
                            BOARD_OFFSET[0] + popup_x + i * SQUARE,
                            BOARD_OFFSET[1] + popup_y,
                            SQUARE,
                            SQUARE,
                        )
                        if rect.collidepoint(mx, my):
                            return self.create_piece(options[i], pawn.color, pawn.row, pawn.col)

    def simulate_move(self, piece: Piece, row: int, col: int) -> bool:
        orig_row, orig_col = piece.row, piece.col
        captured = self.Board.Board[row][col]

        self.Board.Board[orig_row][orig_col] = 0
        self.Board.Board[row][col] = piece
        piece.row, piece.col = row, col

        ep_captured = None
        if piece.type == "Pawn" and captured == 0 and col != orig_col:
            ep_row = orig_row
            ep_captured = self.Board.Board[ep_row][col]
            self.Board.Board[ep_row][col] = 0

        king_pos = self.get_king_pos(self.Board, piece.color)
        in_check = self.is_square_attacked(king_pos[0], king_pos[1], piece.color)

        self.Board.Board[orig_row][orig_col] = piece
        self.Board.Board[row][col] = captured
        piece.row, piece.col = orig_row, orig_col

        if ep_captured:
            self.Board.Board[orig_row][col] = ep_captured

        return not in_check

    def checkmate(self, board: NewBoard) -> bool:
        for r in range(ROWS):
            for c in range(COLS):
                piece = board.Board[r][c]
                if isinstance(piece, Piece) and piece.color == self.turn:
                    moves = piece.get_available_moves(board)
                    for move in moves:
                        if self.simulate_move(piece, move[0], move[1]):
                            return False
        return True

    def change_turn(self) -> None:
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
            self.current_turn += 1
        self.total_turn += 1

    def handle_click(self, location: tuple[int, int]) -> None:
        if (
            BOARD_OFFSET[0] <= location[0] <= BOARD_OFFSET[0] + WIDTH
            and BOARD_OFFSET[1] <= location[1] <= BOARD_OFFSET[1] + HEIGHT
        ):
            row, col = self.get_positions_on_board(
                location[0] - BOARD_OFFSET[0], location[1] - BOARD_OFFSET[1]
            )
            self.select(row, col)

    def select(self, row: int, col: int) -> None:
        if self.selected:
            moved = self._move(row, col)
            if moved:
                return

        piece = self.Board.get_piece(row, col)
        if isinstance(piece, Piece) and piece.color == self.turn:
            self.selected = piece
            raw_moves = piece.get_available_moves(self.Board)
            self.valid_moves = [m for m in raw_moves if self.simulate_move(piece, m[0], m[1])]
        else:
            self.selected = None
            self.valid_moves = []

    @staticmethod
    def get_move_code(
        piece: Piece,
        start_pos: tuple[int, int],
        end_pos: tuple[int, int],
        captured_piece: Any,
        is_ep: bool = False,
        promoted_to: Optional[Piece] = None,
    ) -> str:
        sr, sc = start_pos
        er, ec = end_pos

        if piece.type == "King" and abs(ec - sc) == 2:
            return "O-O" if ec > sc else "O-O-O"

        code = PIECE_CODE[piece.type]
        dest = f"{COL_NAME[ec]}{8 - er}"

        if piece.type == "Pawn":
            if captured_piece != 0 or is_ep:
                code = f"{COL_NAME[sc]}x{dest}"
            else:
                code = dest
        else:
            if captured_piece != 0:
                code += f"x{dest}"
            else:
                code += dest

        if promoted_to:
            code += f"={PIECE_CODE[promoted_to.type]}"

        return code

    def _move(self, row: int, col: int) -> bool:
        if not self.selected or (row, col) not in self.valid_moves:
            return False

        start_pos = (self.selected.row, self.selected.col)
        end_pos = (row, col)
        target = self.Board.get_piece(row, col)
        is_ep = False
        captured_piece = target

        if self.selected.type == "Pawn" and target == 0 and col != start_pos[1]:
            is_ep = True
            captured_piece = self.Board.get_piece(start_pos[0], col)
            self.remove(captured_piece, start_pos[0], col)

        if self.selected.type == "King" and abs(col - start_pos[1]) == 2:
            r_row = start_pos[0]
            if col > start_pos[1]:
                rook = self.Board.get_piece(r_row, 7)
                if isinstance(rook, Rook):
                    self.Board.move(rook, r_row, col - 1)
            else:
                rook = self.Board.get_piece(r_row, 0)
                if isinstance(rook, Rook):
                    self.Board.move(rook, r_row, col + 1)

        if isinstance(target, Piece) and target.color != self.selected.color:
            self.remove(target, row, col)
            self.nb_moves_from_last_capture = 0
        elif self.selected.type == "Pawn":
            self.nb_moves_from_last_capture = 0
        else:
            self.nb_moves_from_last_capture += 1

        self.Board.move(self.selected, row, col)

        promoted_piece = None
        if self.selected.type == "Pawn" and (row == 0 or row == 7):
            promoted_piece = self.promote_pawn(self.selected)
            self.Board.Board[row][col] = promoted_piece

        code = self.get_move_code(
            self.selected, start_pos, end_pos, captured_piece, is_ep, promoted_piece
        )

        if self.turn == WHITE:
            self.past_moves_code[self.current_turn] = (code,)
        else:
            white_code = self.past_moves_code[self.current_turn][0]
            self.past_moves_code[self.current_turn] = (white_code, code)

        self.past_moves_usable[self.total_turn] = (start_pos, end_pos)

        self.selected = None
        self.valid_moves = []
        self.update_window()
        self.change_turn()

        return True

    def remove(self, piece: Any, row: int, col: int) -> None:
        if isinstance(piece, Piece):
            self.Board.Board[row][col] = 0
            if piece.color == WHITE:
                self.White_pieces_left -= 1
            else:
                self.Black_pieces_left -= 1

    def draw_available_moves(self) -> None:
        if not self.selected or not self.valid_moves:
            return

        grey_alpha = (0, 0, 0, 75)

        for row, col in self.valid_moves:
            target = self.Board.get_piece(row, col)

            is_en_passant = (
                self.selected.type == "Pawn"
                and target == 0
                and col != self.selected.col
            )

            surf = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
            center_rel = (SQUARE // 2, SQUARE // 2)

            if target != 0 or is_en_passant:
                radius = SQUARE // 2 - 4
                line_width = max(5, SQUARE // 14)
                pygame.draw.circle(surf, grey_alpha, center_rel, radius, line_width)
            else:
                radius = SQUARE // 6
                pygame.draw.circle(surf, grey_alpha, center_rel, radius)

            pos_x = BOARD_OFFSET[0] + col * SQUARE
            pos_y = BOARD_OFFSET[1] + row * SQUARE
            self.win.blit(surf, (pos_x, pos_y))

    def get_board(self) -> NewBoard:
        return self.Board

    def get_pgn(self, result: str = "*") -> str:
        """Génère la chaîne de caractères au format PGN standard."""
        today = datetime.date.today().strftime("%Y.%m.%d")

        headers = [
            '[Event "Casual Game"]',
            '[Site "Pygame Chess"]',
            f'[Date "{today}"]',
            '[Round "1"]',
            '[White "White"]',
            '[Black "Black"]',
            f'[Result "{result}"]',
            ""  # Ligne vide obligatoire entre les en-têtes et les coups
        ]

        moves_list = []
        for turn_num in sorted(self.past_moves_code.keys()):
            moves = self.past_moves_code[turn_num]
            if len(moves) == 1:
                moves_list.append(f"{turn_num}. {moves[0]}")
            elif len(moves) == 2:
                moves_list.append(f"{turn_num}. {moves[0]} {moves[1]}")

        moves_str = " ".join(moves_list)
        if moves_str:
            moves_str += f" {result}"
        else:
            moves_str = result

        return "\n".join(headers) + moves_str

    def export_to_pgn(self, filepath: str = "game.pgn", result: str = "*") -> str:
        pgn_content = self.get_pgn(result)
        # Mode "a" pour ajouter à la suite sans écraser
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(pgn_content + "\n\n")
        print(f"Partie ajoutée au PGN : {filepath}")
        return pgn_content