import sqlite3

conn = sqlite3.connect('data/to-do.db')
cursor = conn.cursor()

# Création d'une table
cursor.execute("""
    DROP TABLE ;

""")
conn.commit()
