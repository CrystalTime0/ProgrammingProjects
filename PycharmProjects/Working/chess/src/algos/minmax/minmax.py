from algos.minmax.constants import PIECES_VALUES, WHITE, BLACK
import copy


class MinMax:

    @staticmethod
    def possible_moves(board, turn):
        moves_list = []
        grid = board.Board

        for r in range(len(grid)):
            for c in range(len(grid[r])):
                piece = grid[r][c]
                if piece != 0 and piece.color == turn:
                    piece.get_available_moves(board)
                    for move in piece.available_moves:
                        moves_list.append(((r, c), move))
        return moves_list

    def evaluate(self, board):
        value = 0
        grid = board.Board

        for r in range(len(grid)):
            for c in range(len(grid[r])):
                piece = grid[r][c]
                if piece != 0:
                    if piece.color == WHITE:
                        value += PIECES_VALUES[piece.type]
                    else:
                        value -= PIECES_VALUES[piece.type]

        value *= 10
        value -= len(self.possible_moves(board, BLACK))
        value += len(self.possible_moves(board, WHITE))
        return value

    def minimax(self, board, depth, maximizing, original_game):
        if depth == 0:
            return self.evaluate(board)

        turn = WHITE if maximizing else BLACK
        moves = self.possible_moves(board, turn)

        if not moves:
            return self.evaluate(board)

        if maximizing:
            best = float('-inf')
            for start, end in moves:
                tmp = copy.deepcopy(board)
                # Réassigner game pour toutes les pièces
                for row in tmp.Board:
                    for piece in row:
                        if piece != 0:
                            piece.game = original_game
                grid = tmp.Board

                grid[end[0]][end[1]] = grid[start[0]][start[1]]
                grid[start[0]][start[1]] = 0

                best = max(best, self.minimax(tmp, depth - 1, False, original_game))
            return best
        else:
            best = float('inf')
            for start, end in moves:
                tmp = copy.deepcopy(board)
                # Réassigner game pour toutes les pièces
                for row in tmp.Board:
                    for piece in row:
                        if piece != 0:
                            piece.game = original_game

                grid = tmp.Board

                grid[end[0]][end[1]] = grid[start[0]][start[1]]
                grid[start[0]][start[1]] = 0

                best = min(best, self.minimax(tmp, depth - 1, True, original_game))
            return best

    def next_move(self, board, depth, original_game):
        best_move = None
        best_value = float('inf')  # IA joue BLACK → minimise

        moves = self.possible_moves(board, BLACK)
        if not moves:
            return None

        for start, end in moves:
            tmp = copy.deepcopy(board)

            # Réassigner game pour toutes les pièces copiées
            for row in tmp.Board:
                for piece in row:
                    if piece != 0:
                        piece.game = original_game  # référence vers le Game réel

            # Simuler le coup
            grid = tmp.Board
            grid[end[0]][end[1]] = grid[start[0]][start[1]]
            grid[start[0]][start[1]] = 0

            # Appeler minimax sur le plateau simulé
            value = self.minimax(tmp, depth - 1, True, original_game)

            if value < best_value:
                best_value = value
                best_move = (start, end)

        return best_move
