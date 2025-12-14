from constants import *


class Piece:
    def __init__(self, Square, image, color, type, row, col, game):
        self.Square = Square
        self.image = image
        self.color = color
        self.row = row
        self.col = col
        self.type = type
        self.x = 0
        self.y = 0
        self.available_moves = []
        self.game = game
        self.calc_pos()

    def piece_move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    # Transforme row, col en x, y
    def calc_pos(self):
        self.x = self.col * self.Square
        self.y = self.row * self.Square

    def clear_available_moves(self):
        if len(self.available_moves) > 0:
            self.available_moves = []


class Pawn(Piece):
    def __init__(self, Square, image, color, type, row, col, game):
        super().__init__(Square, image, color, type, row, col, game)
        self.first_move = True

    # noinspection PyUnusedLocal
    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()

        row, col = self.row, self.col

        if self.color == WHITE:
            # go in front
            if row - 1 >= 0:
                if Board.Board[row - 1][col] == 0:
                    self.available_moves.append((row - 1, col))
                    if self.first_move and Board.Board[row - 2][col] == 0:
                        self.available_moves.append((row - 2, col))
            # capture
            if col - 1 >= 0:
                if Board.Board[row - 1][col - 1] != 0:
                    if Board.Board[row - 1][col - 1].color != self.color:
                        self.available_moves.append((row - 1, col - 1))
            if col + 1 < len(Board):
                if Board.Board[row - 1][col + 1] != 0:
                    if Board.Board[row - 1][col + 1].color != self.color:
                        self.available_moves.append((row - 1, col + 1))

            # EN PASSANT (WHITE)
            if self.game.total_turn > 0:
                if self.game.total_turn - 1 in self.game.past_moves_usable:
                    last_move = self.game.past_moves_usable[self.game.total_turn - 1]
                    (sr, sc), (er, ec) = last_move

                    # Le dernier coup est un pion noir qui a avancé de 2 cases
                    if abs(sr - er) == 2:
                        last_piece = Board.Board[er][ec]
                        if last_piece != 0 and last_piece.type == "Pawn" and last_piece.color == BLACK:
                            # Le pion noir doit être **adjacent horizontalement** à notre pion blanc
                            if er == self.row and abs(ec - self.col) == 1:
                                # Ajouter la case derrière le pion noir
                                self.available_moves.append((self.row - 1, ec))

        if self.color == BLACK:
            # go in front
            if row + 1 < len(Board):
                if Board.Board[row + 1][col] == 0:
                    self.available_moves.append((row + 1, col))
                    if self.first_move and Board.Board[row + 2][col] == 0:
                        self.available_moves.append((row + 2, col))
            # capture
            if col - 1 >= 0:
                if Board.Board[row + 1][col - 1] != 0:
                    if Board.Board[row + 1][col - 1].color != self.color:
                        self.available_moves.append((row + 1, col - 1))
            if col + 1 < len(Board):
                if Board.Board[row + 1][col + 1] != 0:
                    if Board.Board[row + 1][col + 1].color != self.color:
                        self.available_moves.append((row + 1, col + 1))

            # EN PASSANT (BLACK)
            if self.game.total_turn > 0:
                last_move = self.game.past_moves_usable.get(self.game.total_turn - 1)
                if last_move:
                    (sr, sc), (er, ec) = last_move
                    last_piece = Board.Board[er][ec]
                    if (last_piece != 0 and last_piece.type == "Pawn" and last_piece.color == WHITE
                            and abs(er - sr) == 2 and er == self.row and abs(ec - col) == 1):
                        # case derrière le pion blanc
                        self.available_moves.append((row + 1, ec))

    def get_attack_squares(self, Board):
        row, col = self.row, self.col
        attack_squares = []

        if self.color == WHITE:
            if col - 1 >= 0:
                if Board.Board[row - 1][col - 1] != 0:
                    if Board.Board[row - 1][col - 1].color != self.color:
                        attack_squares.append((row - 1, col - 1))
            if col + 1 < len(Board):
                if Board.Board[row - 1][col + 1] != 0:
                    if Board.Board[row - 1][col + 1].color != self.color:
                        attack_squares.append((row - 1, col + 1))
        if self.color == BLACK:
            if col - 1 >= 0:
                if Board.Board[row + 1][col - 1] != 0:
                    if Board.Board[row + 1][col - 1].color != self.color:
                        attack_squares.append((row + 1, col - 1))
            if col + 1 < len(Board):
                if Board.Board[row + 1][col + 1] != 0:
                    if Board.Board[row + 1][col + 1].color != self.color:
                        attack_squares.append((row + 1, col + 1))

        return attack_squares


class Rook(Piece):
    def __init__(self, Square, image, color, type, row, col, game):
        super().__init__(Square, image, color, type, row, col, game)
        self.first_move = True  # Pour vérifier le roque

    # noinspection PyUnusedLocal
    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()

        row, col = self.row, self.col

        # ligne N row+
        for i in range(row - 1, -1, -1):
            if Board.Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board.Board[i][col].color != self.color:
                    self.available_moves.append((i, col))
                break

        # ligne S row+
        for i in range(row + 1, len(Board)):
            if Board.Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board.Board[i][col].color != self.color:
                    self.available_moves.append((i, col))
                break

        # ligne O col-
        for i in range(col - 1, -1, -1):
            if Board.Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board.Board[row][i].color != self.color:
                    self.available_moves.append((row, i))
                break

        # ligne E col+
        for i in range(col + 1, len(Board)):
            if Board.Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board.Board[row][i].color != self.color:
                    self.available_moves.append((row, i))
                break


class Knight(Piece):
    def __init__(self, Square, image, color, type, row, col, game):
        super().__init__(Square, image, color, type, row, col, game)

    # noinspection PyUnusedLocal
    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()

        row, col = self.row, self.col

        if row - 2 >= 0:
            if col - 1 >= 0:
                if Board.Board[row - 2][col - 1] == 0 or Board.Board[row - 2][col - 1].color != self.color:
                    self.available_moves.append((row - 2, col - 1))
            if col + 1 < len(Board):
                if Board.Board[row - 2][col + 1] == 0 or Board.Board[row - 2][col + 1].color != self.color:
                    self.available_moves.append((row - 2, col + 1))
        if row - 1 >= 0:
            if col - 2 >= 0:
                if Board.Board[row - 1][col - 2] == 0 or Board.Board[row - 1][col - 2].color != self.color:
                    self.available_moves.append((row - 1, col - 2))
            if col + 2 < len(Board):
                if Board.Board[row - 1][col + 2] == 0 or Board.Board[row - 1][col + 2].color != self.color:
                    self.available_moves.append((row - 1, col + 2))
        if row + 1 < len(Board):
            if col - 2 >= 0:
                if Board.Board[row + 1][col - 2] == 0 or Board.Board[row + 1][col - 2].color != self.color:
                    self.available_moves.append((row + 1, col - 2))
            if col + 2 < len(Board):
                if Board.Board[row + 1][col + 2] == 0 or Board.Board[row + 1][col + 2].color != self.color:
                    self.available_moves.append((row + 1, col + 2))
        if row + 2 < len(Board):
            if col - 1 >= 0:
                if Board.Board[row + 2][col - 1] == 0 or Board.Board[row + 2][col - 1].color != self.color:
                    self.available_moves.append((row + 2, col - 1))
            if col + 1 < len(Board):
                if Board.Board[row + 2][col + 1] == 0 or Board.Board[row + 2][col + 1].color != self.color:
                    self.available_moves.append((row + 2, col + 1))


class Bishop(Piece):
    def __init__(self, Square, image, color, type, row, col, game):
        super().__init__(Square, image, color, type, row, col, game)

    # noinspection PyUnusedLocal
    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()

        row, col = self.row, self.col

        # diagonale NE row- col+
        row_i = row - 1
        col_i = col + 1

        while row_i >= 0 and col_i < len(Board):
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i -= 1
                col_i += 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale NO row- col-
        row_i = row - 1
        col_i = col - 1

        while row_i >= 0 and col_i >= 0:
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i -= 1
                col_i -= 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale SE row+ col+
        row_i = row + 1
        col_i = col + 1

        while row_i < len(Board) and col_i < len(Board):
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i += 1
                col_i += 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale S0 row+ col-
        row_i = row + 1
        col_i = col - 1

        while row_i < len(Board) and col_i >= 0:
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i += 1
                col_i -= 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break


class Queen(Piece):
    def __init__(self, Square, image, color, type, row, col, game):
        super().__init__(Square, image, color, type, row, col, game)

    # noinspection PyUnusedLocal
    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()

        row, col = self.row, self.col

        # ligne N row+
        for i in range(row - 1, -1, -1):
            if Board.Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board.Board[i][col].color != self.color:
                    self.available_moves.append((i, col))
                break

        # ligne S row-
        for i in range(row + 1, len(Board)):
            if Board.Board[i][col] == 0:
                self.available_moves.append((i, col))
            else:
                if Board.Board[i][col].color != self.color:
                    self.available_moves.append((i, col))
                break

        # ligne O col-
        for i in range(col - 1, -1, -1):
            if Board.Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board.Board[row][i].color != self.color:
                    self.available_moves.append((row, i))
                break

        # ligne E col+
        for i in range(col + 1, len(Board)):
            if Board.Board[row][i] == 0:
                self.available_moves.append((row, i))
            else:
                if Board.Board[row][i].color != self.color:
                    self.available_moves.append((row, i))
                break

        # diagonale NE row- col+
        row_i = row - 1
        col_i = col + 1

        while row_i >= 0 and col_i < len(Board):
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i -= 1
                col_i += 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale NO row- col-
        row_i = row - 1
        col_i = col - 1

        while row_i >= 0 and col_i >= 0:
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i -= 1
                col_i -= 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale SE row+ col+
        row_i = row + 1
        col_i = col + 1

        while row_i < len(Board) and col_i < len(Board):
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i += 1
                col_i += 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break

        # diagonale S0 row+ col-
        row_i = row + 1
        col_i = col - 1

        while row_i < len(Board) and col_i >= 0:
            if Board.Board[row_i][col_i] == 0:
                self.available_moves.append((row_i, col_i))

                row_i += 1
                col_i -= 1
            else:
                if Board.Board[row_i][col_i].color != self.color:
                    self.available_moves.append((row_i, col_i))
                break


class King(Piece):
    def __init__(self, Square, image, color, type, row, col, game):
        super().__init__(Square, image, color, type, row, col, game)
        self.first_move = True  # Pour vérifier le roque

    def can_castle_kingside(self, Board):
        row, col = self.row, self.col
        # Vérifier que les cases entre roi et tour sont vides
        if Board.Board[row][col - 1] != 0 or Board.Board[row][col - 2] != 0:
            return False
        # Vérifier que la tour n’a pas bougé
        rook = Board.Board[row][col - 3]
        if rook == 0 or rook.type != "Rook" or not rook.first_move:
            return False
        # Vérifier que le roi ne passe pas par des cases attaquées
        if self.game.is_square_attacked(row, col - 1, self.color) or self.game.is_square_attacked(row, col - 2, self.color):
            return False
        return True

    def can_castle_queenside(self, Board):
        row, col = self.row, self.col
        # Vérifier que les cases entre roi et tour sont vides
        if Board.Board[row][col + 1] != 0 or Board.Board[row][col + 2] != 0 or Board.Board[row][col + 3] != 0:
            return False
        # Vérifier que la tour n’a pas bougé
        rook = Board.Board[row][col + 4]
        if rook == 0 or rook.type != "Rook" or not rook.first_move:
            return False
        # Vérifier que le roi ne passe pas par des cases attaquées
        if self.game.is_square_attacked(row, col + 1, self.color) or self.game.is_square_attacked(row, col + 2, self.color):
            return False
        return True

    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()

        row, col = self.row, self.col

        possible_values = (-1, 0, 1)
        combinations = [(x, y) for x in possible_values for y in possible_values]
        combinations.remove((0, 0))

        for row_, col_ in combinations:
            if len(Board) > row + row_ >= 0 and len(Board) > col + col_ >= 0:
                if Board.Board[row + row_][col + col_] == 0 or Board.Board[row + row_][col + col_].color != self.color:
                    # Simuler le déplacement du roi
                    orig_row, orig_col = self.row, self.col
                    captured_piece = Board.Board[row + row_][col + col_]
                    Board.Board[row + row_][col + col_] = self
                    Board.Board[orig_row][orig_col] = 0
                    self.row, self.col = row + row_, col + col_

                    # Vérifier si le roi est attaqué après le déplacement
                    if ignore_checks or not self.game.is_square_attacked(row + row_, col + col_, self.color):
                        self.available_moves.append((row + row_, col + col_))

                    # Restaurer l'état initial
                    Board.Board[orig_row][orig_col] = self
                    Board.Board[row + row_][col + col_] = captured_piece
                    self.row, self.col = orig_row, orig_col

        if self.first_move and not ignore_checks:
            if not self.game.is_square_attacked(row, col, self.color):
                # ROQUE COURT (vers la gauche)
                if self.can_castle_kingside(Board):
                    self.available_moves.append((row, col - 2))

                # ROQUE LONG (vers la droite)
                if self.can_castle_queenside(Board):
                    self.available_moves.append((row, col + 2))

    def get_attack_squares(self, Board):
        self.clear_available_moves()
        row, col = self.row, self.col
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        attack_squares = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(Board) and 0 <= nc < len(Board):
                target = Board.Board[nr][nc]
                if target == 0 or target.color != self.color:
                    attack_squares.append((nr, nc))
        return attack_squares
