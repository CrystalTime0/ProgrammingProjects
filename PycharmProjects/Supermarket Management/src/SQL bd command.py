import sqlite3

conn = sqlite3.connect('data/supermarket.db')
cursor = conn.cursor()

# Création d'une table
cursor.execute("""
    INSERT INTO employees (name, cost, reputation) VALUES (?, ?, ?)""", ("Raymond", 10, 1))
conn.commit()
