import pygame
from Pieces import *
from board import NewBoard
from constants import *


class Game:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Win = Win
        self.Square = Square
        self.turn = WHITE
        self.selected = None
        self.valid_moves = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.current_turn = 1
        self.total_turn = 1
        self.past_moves_code = {}    # {1: ("e4", "e5"), 2: ("Nf3",)}
        self.past_moves_usable = {}  # {1: ((sr, sc), (er, ec))}
        self.nb_moves_from_last_capture = 0
        self.Board = NewBoard(Width, Height, Rows, Cols, Square, Win, self)

    def update_window(self):
        self.Board.draw_board()
        self.Board.draw_pieces()
        self.draw_available_moves()
        pygame.display.update()

    def reset(self):
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
        self.Board = NewBoard(Width, Height, Rows, Cols, self.Square, self.Win, self)

    @staticmethod
    def get_positions_on_board(x: int, y: int) -> tuple[int, int]:
        row = y // Square
        col = x // Square
        return row, col

    def check_game(self):
        if self.checkmate(self.Board):
            winner = "Black" if self.turn == WHITE else "White"
            print(f"Checkmate! {winner} wins.")
            return True
        return False

    def enemies_moves(self, color, Board):
        moves = []
        for r in range(Board.Rows):
            for c in range(Board.Cols):
                piece = Board.Board[r][c]
                if piece != 0 and piece.color != color:
                    if piece.type in ("King", "Pawn"):
                        moves.extend(piece.get_attack_squares(Board))
                    else:
                        moves.extend(piece.get_available_moves(Board, ignore_checks=True))
        return moves

    def is_square_attacked(self, row, col, color):
        return (row, col) in self.enemies_moves(color, self.Board)

    def get_king_pos(self, Board, color=None):
        target_color = color if color else self.turn
        for r in range(Board.Rows):
            for c in range(Board.Cols):
                piece = Board.Board[r][c]
                if piece != 0 and piece.type == "King" and piece.color == target_color:
                    return r, c
        raise ValueError("King not found on board")

    def create_piece(self, piece_type, color, row, col):
        mapping = {
            "Queen": (Queen, White_Queen if color == WHITE else Black_Queen),
            "Rook": (Rook, White_Rook if color == WHITE else Black_Rook),
            "Bishop": (Bishop, White_Bishop if color == WHITE else Black_Bishop),
            "Knight": (Knight, White_Knight if color == WHITE else Black_Knight),
        }
        cls, img = mapping[piece_type]
        return cls(self.Square, img, color, piece_type, row, col, self)

    def promote_pawn(self, pawn):
        popup_x = Height // 2 - 2 * self.Square
        popup_y = (Width - self.Square) // 2

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
                rect = pygame.Rect(BOARD_OFFSET[0] + popup_x + i * self.Square, BOARD_OFFSET[1] + popup_y, self.Square, self.Square)
                pygame.draw.rect(self.Win, GREY, rect)
                self.Win.blit(img, (rect.x, rect.y))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for i in range(4):
                        rect = pygame.Rect(BOARD_OFFSET[0] + popup_x + i * self.Square, BOARD_OFFSET[1] + popup_y, self.Square, self.Square)
                        if rect.collidepoint(mx, my):
                            return self.create_piece(options[i], pawn.color, pawn.row, pawn.col)

    def simulate_move(self, piece, row, col):
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

    def checkmate(self, Board):
        for r in range(Board.Rows):
            for c in range(Board.Cols):
                piece = Board.Board[r][c]
                if piece != 0 and piece.color == self.turn:
                    moves = piece.get_available_moves(Board)
                    for move in moves:
                        if self.simulate_move(piece, move[0], move[1]):
                            return False
        return True

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
            self.current_turn += 1
        self.total_turn += 1

    def handle_click(self, location):
        if (BOARD_OFFSET[0] <= location[0] <= BOARD_OFFSET[0] + Width and
            BOARD_OFFSET[1] <= location[1] <= BOARD_OFFSET[1] + Height
        ):
            row, col = self.get_positions_on_board(location[0] - BOARD_OFFSET[0], location[1] - BOARD_OFFSET[1])
            self.select(row, col)

    def select(self, row, col):
        if self.selected:
            moved = self._move(row, col)
            if moved:
                return

        piece = self.Board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            raw_moves = piece.get_available_moves(self.Board)
            self.valid_moves = [m for m in raw_moves if self.simulate_move(piece, m[0], m[1])]
        else:
            self.selected = None
            self.valid_moves = []

    def get_move_code(self, piece, start_pos, end_pos, captured_piece, is_ep=False, promoted_to=None):
        sr, sc = start_pos
        er, ec = end_pos

        if piece.type == "King" and abs(ec - sc) == 2:
            return "O-O" if ec > sc else "O-O-O"

        code = piece_code[piece.type]
        dest = f"{col_name[ec]}{8 - er}"

        if piece.type == "Pawn":
            if captured_piece != 0 or is_ep:
                code = f"{col_name[sc]}x{dest}"
            else:
                code = dest
        else:
            if captured_piece != 0:
                code += f"x{dest}"
            else:
                code += dest

        if promoted_to:
            code += f"={piece_code[promoted_to.type]}"

        return code

    def _move(self, row, col):
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
                self.Board.move(rook, r_row, col - 1)
            else:
                rook = self.Board.get_piece(r_row, 0)
                self.Board.move(rook, r_row, col + 1)

        if target != 0 and target.color != self.selected.color:
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

    def remove(self, piece, row, col):
        if piece != 0:
            self.Board.Board[row][col] = 0
            if piece.color == WHITE:
                self.White_pieces_left -= 1
            else:
                self.Black_pieces_left -= 1

    def draw_available_moves(self):
        if not self.selected or not self.valid_moves:
            return

        for row, col in self.valid_moves:
            center = (BOARD_OFFSET[0] + col * self.Square + self.Square // 2, BOARD_OFFSET[1] + row * self.Square + self.Square // 2)
            target = self.Board.get_piece(row, col)

            # Détection de la prise en passant
            is_en_passant = (
                self.selected.type == "Pawn"
                and target == 0
                and col != self.selected.col
            )

            # Si la case contient une pièce ennemie ou s'il s'agit d'un En Passant -> Anneau creux
            if target != 0 or is_en_passant:
                radius = self.Square // 2 - 4
                line_width = max(5, self.Square // 14)
                pygame.draw.circle(self.Win, GREY, center, radius, line_width)
            else:
                # Déplacement simple -> Rond plein au centre
                radius = self.Square // 6
                pygame.draw.circle(self.Win, GREY, center, radius)

    def get_board(self):
        return self.Board