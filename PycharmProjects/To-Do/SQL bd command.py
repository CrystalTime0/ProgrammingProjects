import sqlite3

conn = sqlite3.connect('to-do.db')
cursor = conn.cursor()

# Création d'une table
cursor.execute("""
    DROP TABLE mdp;

""")
conn.commit()
