import pygame.display

from Pieces import *
from board import NewBoard
from constants import *


class Game:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Win = Win
        self.Board = NewBoard(Width, Height, Rows, Cols, Square, Win, self)
        self.Square = Square
        self.selected: Piece | None = None
        self.turn = WHITE
        self.valid_moves = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.current_turn = 1
        self.total_turn = 1
        self.past_moves_code = {}  # {1:("Ke4", "Nxe5")}
        self.past_moves_usable = {}  # {1:((sr, sc), (er, ec))}

    # Afficher les élements
    def update_window(self):
        self.Board.draw_board()
        self.Board.draw_pieces()
        self.draw_available_moves()
        pygame.display.update()

    # Recréer un nouveau plateau
    def reset(self):
        self.Board = NewBoard(Width, Height, Rows, Cols, Square, self.Win, self)
        self.Square = Square
        self.selected = None

    # Vérifier les état ex: nombre de pieces restantes ou checkmate
    def check_game(self):
        if self.Black_pieces_left == 0:
            print("Whites win")
            return True

        if self.White_pieces_left == 0:
            print("Blacks win")
            return True

        if self.checkmate(self.Board):
            if self.turn == WHITE:
                print("Black Wins")
                return True
            else:
                print("White wins")
                return True
        return False

    # Renvoie une liste de tuple contenant toutes les cases accessibles en 1 coup par l'adversaire
    @staticmethod
    def enemies_moves(color, Board):
        moves = []
        for r in range(len(Board.Board)):
            for c in range(len(Board.Board[r])):
                piece = Board.Board[r][c]
                if piece != 0 and piece.color != color:
                    if piece.type == "King" or piece.type == "Pawn":
                        # On utilise get_attack_squares pour éviter la récursion
                        moves.extend(piece.get_attack_squares(Board))
                    else:
                        piece.get_available_moves(Board, ignore_checks=True)
                        moves.extend(piece.available_moves)
        return moves

    def is_square_attacked(self, row, col, color):
        return (row, col) in self.enemies_moves(color, self.Board)

    def get_king_pos(self, Board):
        for r in range(len(Board)):
            for c in range(len(Board)):
                if Board.Board[r][c] != 0:
                    if Board.Board[r][c].type == "King" and Board.Board[r][c].color == self.turn:
                        return r, c
        raise ValueError("The King is un findable")

    def simulate_move(self, piece, row, col):
        piece_row, piece_col = piece.row, piece.col
        print("piece row, col", piece_row, piece_col)
        print(row, col)
        save_piece = self.Board.Board[row][col]
        if self.Board.Board[row][col] != 0:
            self.Board.Board[row][col] = 0

        self.Board.Board[piece.row][piece.col], self.Board.Board[row][col] = self.Board.Board[row][col], \
            self.Board.Board[piece.row][piece.col]

        king_pos = self.get_king_pos(self.Board)
        if king_pos in self.enemies_moves(piece.color, self.Board):
            piece.row, piece.col = piece_row, piece_col
            self.Board.Board[piece_row][piece_col] = piece
            self.Board.Board[row][col] = save_piece
            return False

        piece.row, piece.col = piece_row, piece_col
        self.Board.Board[piece_row][piece_col] = piece
        self.Board.Board[row][col] = save_piece
        return True

    def possible_moves(self, Board):
        possible_moves = []
        for r in range(len(Board)):
            for c in range(len(Board.Board[r])):
                if Board.Board[r][c] != 0:
                    if Board.Board[r][c].color == self.turn and Board.Board[r][c].type != "King":
                        moves = Board.Board[r][c].get_available_moves(Board)
                        # print(self.Board.Board[r][c].type, moves)
                        if moves:
                            for move in moves:
                                possible_moves.append(move)

        return possible_moves

    def checkmate(self, Board):
        king_pos = self.get_king_pos(Board)
        get_king = Board.get_piece(king_pos[0], king_pos[1])
        get_king.get_available_moves(Board)
        king_available_moves = set(get_king.available_moves)
        enemies_moves_set = set(self.enemies_moves(get_king.color, Board))
        king_moves = king_available_moves - enemies_moves_set
        set1 = king_available_moves.intersection(enemies_moves_set)
        possible_moves_to_def = set1.intersection(self.possible_moves(Board))
        if len(king_moves) == 0 and len(king_available_moves) != 0 and possible_moves_to_def == 0:
            return True

        return False

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        elif self.turn == BLACK:
            self.turn = WHITE
            self.current_turn += 1
        self.total_turn += 1
        print(self.turn)

    def select(self, row, col):
        if self.selected:
            # print("selected")

            move = self._move(row, col)

            if not move:
                # print("in not move")
                self.selected = None
                self.select(row, col)

        piece = self.Board.get_piece(row, col)
        if piece == 0 or piece.color != self.turn:
            self.valid_moves = []
            self.draw_available_moves()
        if piece != 0 and self.turn == piece.color:
            self.selected = piece
            self.draw_available_moves()
            # print(piece)
            piece.get_available_moves(self.Board)
            self.valid_moves = piece.available_moves
            print("self valid_moves", self.valid_moves)
            print("new valid_moves", self.valid_moves)
        else:
            self.draw_available_moves()

    def get_move_code(self, captured_piece=None):
        code = ""
        piece = self.selected
        code += piece_code[piece.type]
        code += col_name[piece.col] + str(piece.row)
        if captured_piece:
            code += "x" + col_name[captured_piece.col] + str(captured_piece.row)
        return code

    def _move(self, row, col):
        piece = self.Board.get_piece(row, col)
        print("self selected", self.selected.type)
        if self.selected and (row, col) in self.valid_moves:
            if piece == 0 or piece.color != self.selected.color:
                print(self.simulate_move(self.selected, row, col))
                if self.simulate_move(self.selected, row, col):
                    start_pos = (self.selected.row, self.selected.col)
                    end_pos = (row, col)

                    # --- Gestion Roque ---
                    # Si le roi se déplace de 2 cases → roque
                    if self.selected.type == "King" and abs(col - self.selected.col) == 2:
                        row = self.selected.row
                        # Roque court
                        if col < self.selected.col:
                            rook = self.Board.Board[row][self.selected.col - 3]
                            self.Board.move(rook, row, col + 1)
                            rook.first_move = False
                        # Roque long
                        else:
                            rook = self.Board.Board[row][self.selected.col + 4]
                            self.Board.move(rook, row, col - 1)
                            rook.first_move = False

                        # Marquer le roi comme ayant bougé
                        self.selected.first_move = False

                    # --- Gestion En Passant ---
                    if self.selected.type == "Pawn":
                        # Si le pion se déplace en diagonale vers une case vide => En Passant
                        if piece == 0 and col != self.selected.col:
                            # Pion capturé juste derrière
                            captured_row = self.selected.row
                            captured_col = col
                            captured_piece = self.Board.get_piece(captured_row, captured_col)
                            if captured_piece != 0 and captured_piece.type == "Pawn":
                                self.remove(captured_piece, captured_row, captured_col)
                    self.remove(piece, row, col)
                    self.Board.move(self.selected, row, col)

                    # -----histo coups-----
                    #   code
                    code = self.get_move_code(piece)
                    if self.turn == WHITE:
                        self.past_moves_code[self.current_turn] = code
                    if self.turn == BLACK:
                        self.past_moves_code[self.current_turn] = (self.past_moves_code[self.current_turn], code)
                    print(self.past_moves_code)
                    #   usable
                    self.past_moves_usable[self.total_turn] = (start_pos, end_pos)

                    self.change_turn()
                    print("turn", self.turn)
                    self.valid_moves = []
                    self.selected = None

                    return True
                return False

        return False

    def remove(self, piece, row, col):
        if piece != 0:
            self.Board.Board[row][col] = 0
            if piece.color == WHITE:
                self.White_pieces_left -= 1
            else:
                self.Black_pieces_left -= 1
        print("White_pieces_left : ", self.White_pieces_left)
        print("Black_pieces_left : ", self.Black_pieces_left)

    def draw_available_moves(self):
        if len(self.valid_moves) > 0:
            for pos in self.valid_moves:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.Win, GREY,
                                   (col * self.Square + self.Square // 2, row * self.Square + self.Square // 2),
                                   self.Square // 8)

    def get_board(self):
        return self.Board
