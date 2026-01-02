import requests
import os

print("Downloading Pieces png")
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
path = f"{os.path.dirname(os.path.abspath(__file__))}"
files_to_download: list[str] = []

for key in pieces.keys():
    tmp_path = f"{path}/{key}.png"
    if not os.path.exists(tmp_path):
        files_to_download.append(key)
    else:
        print("Already exist :", tmp_path[-34:])

for code in files_to_download:
    url = f"{base_url}{code}.png"
    response = requests.get(url)
    if response.status_code == 200:
        # Enregistre directement dans le répertoire courant
        code_path = f"{path}/{code}.png"
        with open(code_path, "wb") as f:
            f.write(response.content)
        print(f"Téléchargé et enregistré : {path}")
    else:
        print(f"Erreur téléchargement : {url}")
else:
    print("Download complete\n")
