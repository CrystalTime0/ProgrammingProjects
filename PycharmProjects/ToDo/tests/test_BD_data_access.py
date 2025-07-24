import os
import shutil
import sqlite3
import pytest
from BD_data_access import *

# Chemin vers ta base de test (modèle)
MODEL_DB_PATH = os.path.abspath("tests/data/to-do.db")
# Chemin de la copie temporaire utilisée pendant le test
TEMP_DB_PATH = os.path.abspath("tests/data/tmp/to-do.db")

@pytest.fixture(autouse=True)
def patch_sqlite(monkeypatch):
    # Crée le dossier temporaire s'il n'existe pas
    os.makedirs(os.path.dirname(TEMP_DB_PATH), exist_ok=True)

    # Copie la base de test dans un fichier temporaire
    shutil.copyfile(MODEL_DB_PATH, TEMP_DB_PATH)

    # Patch sqlite3.connect pour utiliser la copie temporaire
    def fake_connect(path, *args, **kwargs):
        if path == "data/to-do.db":
            return sqlite3.connect(TEMP_DB_PATH, *args, **kwargs)
        return sqlite3.connect(path, *args, **kwargs)

    monkeypatch.setattr(sqlite3, "connect", fake_connect)

    yield

    # Nettoyage après le test
    if os.path.exists(TEMP_DB_PATH):
        os.remove(TEMP_DB_PATH)

def test_read_cell():
    generated = readcell("1","1","test_table")
    assert 1 == 1