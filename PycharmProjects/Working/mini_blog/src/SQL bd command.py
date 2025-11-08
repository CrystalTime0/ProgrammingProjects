import sqlite3

conn = sqlite3.connect('data/mdp.db')
cursor = conn.cursor()

# Création d'une table
cursor.execute("""
    DROP TABLE user;

""")
conn.commit()