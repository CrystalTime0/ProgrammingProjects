from stockfish import Stockfish


class StockfishEngine:
    def __init__(self, game, contempt=0, skill_level=20, ignore_skill: str = "false", elo=1350):
        self.parameters = {
    "Debug Log File": "",
    "Contempt": contempt,
    "Min Split Depth": 0,
    "Threads": 1,
    "Ponder": False,  # ← Boolean au lieu de "false"
    "Hash": 16,
    "MultiPV": 1,
    "Skill Level": skill_level,
    "Move Overhead": 10,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": False,  # ← Boolean au lieu de "false"
    "UCI_LimitStrength": True if elo else False,  # ← Boolean
    "UCI_Elo": elo if elo else 1350,
    }

        self.stockfish = Stockfish(
            path="/usr/bin/stockfish",
            parameters=self.parameters
        )
        self.game = game

        self.stockfish.set_fen_position(game.Board.get_fen())

    def next_move(self):
        self.stockfish.set_fen_position(self.game.Board.get_fen())
        move = self.stockfish.get_best_move()
        start_pos = ((8 - int(move[1])), ord(move[0]) - ord("a"))
        end_pos = (8 - int(move[3]), ord(move[2]) - ord('a'))
        return start_pos, end_pos
