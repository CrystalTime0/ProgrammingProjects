import pygame.display

from Pieces import *
from board import NewBoard
from constants import *
from algos.minmax.minmax import MinMax


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
        self.ia = MinMax()

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

    def create_piece(self, type, color, row, col):
        if type == "Queen":
            img = White_Queen if color == WHITE else Black_Queen
            return Queen(self.Square, img, color, "Queen", row, col, self)
        elif type == "Rook":
            img = White_Rook if color == WHITE else Black_Rook
            return Rook(self.Square, img, color, "Rook", row, col, self)
        elif type == "Bishop":
            img = White_Bishop if color == WHITE else Black_Bishop
            return Bishop(self.Square, img, color, "Bishop", row, col, self)
        elif type == "Knight":
            img = White_Knight if color == WHITE else Black_Knight
            return Knight(self.Square, img, color, "Knight", row, col, self)

    def promote_pawn(self, pawn):
        # Dimensions de la popup
        popup_x = Height // 2 - 2 * self.Square
        popup_y = (Width - self.Square) // 2  # au-dessus du pion

        # Options de promotion
        options = ["Queen", "Rook", "Bishop", "Knight"]
        option_images = [White_Queen, White_Rook, White_Bishop, White_Knight] \
            if pawn.color == WHITE else [Black_Queen, Black_Rook, Black_Bishop, Black_Knight]

        selecting = True
        while selecting:
            self.Win.fill(BEIGE)  # ou redraw le plateau
            self.Board.draw_board()
            self.Board.draw_pieces()

            # Dessiner la popup
            for i, img in enumerate(option_images):
                rect = pygame.Rect(popup_x + i * self.Square, popup_y, self.Square, self.Square)
                pygame.draw.rect(self.Win, GREY, rect)
                self.Win.blit(img, (rect.x, rect.y))

            pygame.display.update()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for i in range(4):
                        rect = pygame.Rect(popup_x + i * self.Square, popup_y, self.Square, self.Square)
                        if rect.collidepoint(mx, my):
                            # Remplacer le pion par la pièce choisie
                            new_piece_type = options[i]
                            new_piece = self.create_piece(new_piece_type, pawn.color, pawn.row, pawn.col)
                            return new_piece

    def simulate_move(self, piece, row, col):
        piece_row, piece_col = piece.row, piece.col
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
                    if Board.Board[r][c].color == self.turn:
                        moves = Board.Board[r][c].get_available_moves(Board)
                        if moves:
                            for move in moves:
                                possible_moves.append(move)

        return possible_moves

    def checkmate(self, Board):
        king_row, king_col = self.get_king_pos(Board)
        king = Board.get_piece(king_row, king_col)

        # Récupérer les mouvements légaux du roi
        king.get_available_moves(Board)
        if king.available_moves:
            # Le roi peut encore bouger → pas de mat
            return False

        # Vérifier si une autre pièce peut sauver le roi
        for r in range(len(Board.Board)):
            for c in range(len(Board.Board[r])):
                piece = Board.Board[r][c]
                if piece != 0 and piece.color == king.color and piece.type != "King":
                    piece.get_available_moves(Board)
                    for move in piece.available_moves:
                        # Simuler le coup
                        orig_row, orig_col = piece.row, piece.col
                        captured_piece = Board.Board[move[0]][move[1]]
                        Board.Board[move[0]][move[1]] = piece
                        Board.Board[orig_row][orig_col] = 0
                        piece.row, piece.col = move

                        king_safe = not self.is_square_attacked(king_row, king_col, king.color)

                        # Restaurer
                        Board.Board[orig_row][orig_col] = piece
                        Board.Board[move[0]][move[1]] = captured_piece
                        piece.row, piece.col = orig_row, orig_col

                        if king_safe:
                            return False  # Le roi peut être sauvé

        # Aucun mouvement légal pour le roi ni aucune pièce ne peut sauver → mat
        return True

    def ia_play(self):
        pass

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
            print("BLACK TURN".center(24, "-"))
            ia_move = self.ia.next_move(self.Board, 3, self)
            print("MinMax joue : ", ia_move)
            ia_start_pos, ia_end_pos = ia_move
            self.select(ia_start_pos[0], ia_start_pos[1])
            self.select(ia_end_pos[0], ia_end_pos[1])
        elif self.turn == BLACK:
            self.turn = WHITE
            self.current_turn += 1
            print("WHITE TURN".center(24, "-"))
        self.total_turn += 1

    def select(self, row, col):
        if self.selected:

            move = self._move(row, col)

            if not move:
                self.selected = None
                self.select(row, col)

        piece = self.Board.get_piece(row, col)
        if piece == 0 or piece.color != self.turn:
            self.valid_moves = []
            self.draw_available_moves()
        if piece != 0 and self.turn == piece.color:
            self.selected = piece
            self.draw_available_moves()
            piece.get_available_moves(self.Board)
            self.valid_moves = piece.available_moves
        else:
            self.draw_available_moves()

    def get_move_code(self, start_pos, captured_piece=0):
        code = ""
        piece = self.selected
        code += piece_code[piece.type]
        if captured_piece == 0:
            code += col_name[piece.col] + str(piece.row + 1)
        else:
            code += col_name[start_pos[1]] + str(start_pos[0] + 1)
            code += "x" + col_name[captured_piece.col] + str(captured_piece.row)
        return code

    def _move(self, row, col):
        piece = self.Board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            if piece == 0 or piece.color != self.selected.color:
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

                    if self.selected.type == "Pawn":
                        # --- Gestion En Passant ---
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

                    # ----- Promotion -----
                    if self.Board.Board[row][col].type == "Pawn":
                        if row == 0 or row == 7:
                            self.Board.Board[row][col] = self.promote_pawn(self.selected)

                    # -----histo coups-----
                    #   code
                    code = self.get_move_code(start_pos, piece)
                    if self.turn == WHITE:
                        self.past_moves_code[self.current_turn] = code
                    if self.turn == BLACK:
                        self.past_moves_code[self.current_turn] = (self.past_moves_code[self.current_turn], code)
                    print(self.past_moves_code)
                    #   usable
                    self.past_moves_usable[self.total_turn] = (start_pos, end_pos)
                    self.valid_moves = []
                    self.selected = None
                    self.update_window()
                    self.change_turn()

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
