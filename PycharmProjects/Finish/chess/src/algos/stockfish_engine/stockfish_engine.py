from stockfish import Stockfish


class StockfishEngine:
    def __init__(self, game, contempt=0, skill_level=20, ignore_skill: str = "false", elo=1350):
        self.parameters = {
            # Fichier dans lequel Stockfish peut écrire des logs de debug (laisser vide = pas de log)
            "Debug Log File": "",

            # Biais volontaire dans l’évaluation (valeur positive = Stockfish joue plus agressif,
            # valeur négative = plus conservateur). 0 = neutre.
            "Contempt": contempt,

            # Profondeur minimale à partir de laquelle Stockfish commence à diviser la recherche
            # sur plusieurs threads (0 = automatique).
            "Min Split Depth": 0,

            # Nombre de threads CPU utilisés par le moteur.
            # Plus il y en a, plus le moteur est fort, mais ne doit pas dépasser
            # le nombre de cœurs/logical processors de la machine.
            "Threads": 1,

            # Si "true", Stockfish réfléchit pendant le tour de l’adversaire.
            # Augmente légèrement la force mais consomme plus de CPU.
            "Ponder": "false",

            # Taille de la table de hachage en Mo.
            # Stockfish mémorise les positions déjà analysées.
            # Plus la valeur est grande, meilleure est la performance (dans la limite de la RAM).
            "Hash": 16,

            # Nombre de variantes principales calculées en parallèle.
            # 1 = une seule meilleure ligne, >1 = analyse multi-variantes.
            "MultiPV": 1,

            # Niveau de compétence (0 à 20).
            # 20 = force maximale, valeurs plus basses rendent le moteur plus faible.
            "Skill Level": skill_level,

            # Temps (en millisecondes) réservé pour gérer la latence de l’interface.
            # Utile pour éviter de dépasser le temps en partie rapide.
            "Move Overhead": 10,

            # Temps minimum (en millisecondes) que Stockfish passera à réfléchir,
            # même si la position est simple.
            "Minimum Thinking Time": 20,

            # Facteur de lenteur volontaire.
            # Plus la valeur est élevée, plus Stockfish prendra son temps avant de jouer.
            "Slow Mover": 100,

            # Active les règles du Chess960 (Fischer Random).
            "UCI_Chess960": "false",

            # Si "true", limite la force du moteur via un Elo artificiel.
            "UCI_LimitStrength": ignore_skill,

            # Elo cible utilisé lorsque UCI_LimitStrength est activé.
            # Typiquement entre 800 et ~2850.
            "UCI_Elo": elo
        }

        self.stockfish = Stockfish(
            path=r"C:\Program Files\stockfish\stockfish-windows-x86-64-avx2.exe",
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
