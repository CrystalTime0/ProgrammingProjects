from constants import *


class Piece:
    def __init__(self, Square, image, color, piece_type, row, col, game):
        self.Square = Square
        self.image = image
        self.color = color
        self.row = row
        self.col = col
        self.type = piece_type
        self.x = 0
        self.y = 0
        self.available_moves = []
        self.game = game
        self.calc_pos()

    def piece_move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def calc_pos(self):
        self.x = self.col * self.Square
        self.y = self.row * self.Square

    def clear_available_moves(self):
        self.available_moves.clear()

    def __deepcopy__(self, memo):
        cls = self.__class__
        copy_obj = cls.__new__(cls)
        memo[id(self)] = copy_obj

        copy_obj.Square = self.Square
        copy_obj.image = self.image
        copy_obj.color = self.color
        copy_obj.row = self.row
        copy_obj.col = self.col
        copy_obj.type = self.type
        copy_obj.x = self.x
        copy_obj.y = self.y
        copy_obj.available_moves = self.available_moves.copy()
        copy_obj.first_move = getattr(self, "first_move", False)
        copy_obj.game = None

        return copy_obj


class Pawn(Piece):
    def __init__(self, Square, image, color, piece_type, row, col, game):
        super().__init__(Square, image, color, piece_type, row, col, game)
        self.first_move = True

    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()
        row, col = self.row, self.col

        if self.color == WHITE:
            # Avancement simple et double
            if row - 1 >= 0 and Board.Board[row - 1][col] == 0:
                self.available_moves.append((row - 1, col))
                if self.first_move and row - 2 >= 0 and Board.Board[row - 2][col] == 0:
                    self.available_moves.append((row - 2, col))

            # Captures standard
            for dc in (-1, 1):
                if 0 <= col + dc < Board.Cols and row - 1 >= 0:
                    target = Board.Board[row - 1][col + dc]
                    if target != 0 and target.color != self.color:
                        self.available_moves.append((row - 1, col + dc))

            # En Passant
            if self.game.total_turn > 1:
                last_move = self.game.past_moves_usable.get(self.game.total_turn - 1)
                if last_move:
                    (sr, sc), (er, ec) = last_move
                    last_piece = Board.Board[er][ec]
                    if (last_piece != 0 and last_piece.type == "Pawn" and last_piece.color == BLACK
                            and abs(er - sr) == 2 and er == self.row and abs(ec - col) == 1):
                        self.available_moves.append((row - 1, ec))

        elif self.color == BLACK:
            # Avancement simple et double
            if row + 1 < Board.Rows and Board.Board[row + 1][col] == 0:
                self.available_moves.append((row + 1, col))
                if self.first_move and row + 2 < Board.Rows and Board.Board[row + 2][col] == 0:
                    self.available_moves.append((row + 2, col))

            # Captures standard
            for dc in (-1, 1):
                if 0 <= col + dc < Board.Cols and row + 1 < Board.Rows:
                    target = Board.Board[row + 1][col + dc]
                    if target != 0 and target.color != self.color:
                        self.available_moves.append((row + 1, col + dc))

            # En Passant
            if self.game.total_turn > 1:
                last_move = self.game.past_moves_usable.get(self.game.total_turn - 1)
                if last_move:
                    (sr, sc), (er, ec) = last_move
                    last_piece = Board.Board[er][ec]
                    if (last_piece != 0 and last_piece.type == "Pawn" and last_piece.color == WHITE
                            and abs(er - sr) == 2 and er == self.row and abs(ec - col) == 1):
                        self.available_moves.append((row + 1, ec))

        return self.available_moves

    def get_attack_squares(self, Board):
        attack_squares = []
        row, col = self.row, self.col
        dr = -1 if self.color == WHITE else 1
        for dc in (-1, 1):
            nr, nc = row + dr, col + dc
            if 0 <= nr < Board.Rows and 0 <= nc < Board.Cols:
                attack_squares.append((nr, nc))
        return attack_squares


class Rook(Piece):
    def __init__(self, Square, image, color, piece_type, row, col, game):
        super().__init__(Square, image, color, piece_type, row, col, game)
        self.first_move = True

    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < Board.Rows and 0 <= c < Board.Cols:
                target = Board.Board[r][c]
                if target == 0:
                    self.available_moves.append((r, c))
                else:
                    if target.color != self.color:
                        self.available_moves.append((r, c))
                    break
                r += dr
                c += dc

        return self.available_moves


class Knight(Piece):
    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()
        moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in moves:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < Board.Rows and 0 <= c < Board.Cols:
                target = Board.Board[r][c]
                if target == 0 or target.color != self.color:
                    self.available_moves.append((r, c))

        return self.available_moves


class Bishop(Piece):
    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < Board.Rows and 0 <= c < Board.Cols:
                target = Board.Board[r][c]
                if target == 0:
                    self.available_moves.append((r, c))
                else:
                    if target.color != self.color:
                        self.available_moves.append((r, c))
                    break
                r += dr
                c += dc

        return self.available_moves


class Queen(Piece):
    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < Board.Rows and 0 <= c < Board.Cols:
                target = Board.Board[r][c]
                if target == 0:
                    self.available_moves.append((r, c))
                else:
                    if target.color != self.color:
                        self.available_moves.append((r, c))
                    break
                r += dr
                c += dc

        return self.available_moves


class King(Piece):
    def __init__(self, Square, image, color, piece_type, row, col, game):
        super().__init__(Square, image, color, piece_type, row, col, game)
        self.first_move = True

    def can_castle_kingside(self, Board):
        row, col = self.row, self.col
        if col + 3 >= Board.Cols:
            return False
        if Board.Board[row][col + 1] != 0 or Board.Board[row][col + 2] != 0:
            return False
        rook = Board.Board[row][col + 3]
        if rook == 0 or rook.type != "Rook" or not rook.first_move:
            return False
        if self.game.is_square_attacked(row, col, self.color) or \
           self.game.is_square_attacked(row, col + 1, self.color) or \
           self.game.is_square_attacked(row, col + 2, self.color):
            return False
        return True

    def can_castle_queenside(self, Board):
        row, col = self.row, self.col
        if col - 4 < 0:
            return False
        if Board.Board[row][col - 1] != 0 or Board.Board[row][col - 2] != 0 or Board.Board[row][col - 3] != 0:
            return False
        rook = Board.Board[row][col - 4]
        if rook == 0 or rook.type != "Rook" or not rook.first_move:
            return False
        if self.game.is_square_attacked(row, col, self.color) or \
           self.game.is_square_attacked(row, col - 1, self.color) or \
           self.game.is_square_attacked(row, col - 2, self.color):
            return False
        return True

    def get_available_moves(self, Board, ignore_checks=False):
        self.clear_available_moves()
        row, col = self.row, self.col

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < Board.Rows and 0 <= c < Board.Cols:
                target = Board.Board[r][c]
                if target == 0 or target.color != self.color:
                    self.available_moves.append((r, c))

        if self.first_move and not ignore_checks:
            if self.can_castle_kingside(Board):
                self.available_moves.append((row, col + 2))
            if self.can_castle_queenside(Board):
                self.available_moves.append((row, col - 2))

        return self.available_moves

    def get_attack_squares(self, Board):
        attack_squares = []
        row, col = self.row, self.col
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < Board.Rows and 0 <= c < Board.Cols:
                attack_squares.append((r, c))
        return attack_squares