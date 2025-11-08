import requests
import os

# Correspondance code → nom anglais
pieces = {
    "wp": "white_pawn",
    "wn": "white_knight",
    "wb": "white_bishop",
    "wr": "white_rook",
    "wq": "white_queen",
    "wk": "white_king",
    "bp": "black_pawn",
    "bn": "black_knight",
    "bb": "black_bishop",
    "br": "black_rook",
    "bq": "black_queen",
    "bk": "black_king"
}

base_url = "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/"

for code, name in pieces.items():
    url = f"{base_url}{code}.png"
    response = requests.get(url)
    if response.status_code == 200:
        path = f"{code}.png"  # Enregistre directement dans le répertoire courant
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"Téléchargé et enregistré : {path}")
    else:
        print(f"Erreur téléchargement : {url}")
