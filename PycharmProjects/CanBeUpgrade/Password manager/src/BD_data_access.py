import sqlite3

conn = sqlite3.connect('data/mdp.db')
cursor = conn.cursor()


# -------------------- Initialize BD --------------------
def initialize_BD():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mdp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )

    """)
    cursor.execute("""INSERT OR IGNORE INTO mdp (name, password) VALUES(?, ?)""", ("main", ""))
    conn.commit()


initialize_BD()


# -------------------- GET DATA --------------------
def readcell(line, column):
    cursor.execute("SELECT * FROM mdp WHERE id = ?", (line,))
    conn.commit()
    bd_line = cursor.fetchone()

    if bd_line:
        return bd_line[column]
    else:
        print("cell not found")


def readline(line):
    cursor.execute("SELECT * FROM mdp WHERE id = ?", (line,))
    conn.commit()
    bd_line = cursor.fetchone()

    if bd_line:
        return bd_line
    else:
        print("line not found")


def readcolumn(column):
    cursor.execute(f"""SELECT {column} FROM mdp""")
    resultats = [line[0] for line in cursor.fetchall()]
    return resultats


def get_id_with_name(name):
    cursor.execute("""SELECT id FROM mdp WHERE name = ?""", (name,))
    conn.commit()
    id_found = cursor.fetchone()
    return id_found[0]


# -------------------- UPDATE DATA --------------------
def updatecell(line, column_title, data):
    cursor.execute(f"""UPDATE mdp SET {column_title} = ? WHERE id = ?""", (data, line))
    conn.commit()


def updateline(line, name, password):
    cursor.execute("""UPDATE mdp SET name = ?, mdp = ? WHERE id = ?""", (name, password, line))
    conn.commit()


# -------------------- ADD DATA --------------------
def addline(name, password):
    cursor.execute("""INSERT INTO mdp (name,password) VALUES (?, ?)""", (name, password))
    conn.commit()


# -------------------- REMOVE DATA --------------------

def clearline(line):
    cursor.execute("""DELETE FROM mdp WHERE id = ?""", (line,))
    conn.commit()


def cleardata():
    cursor.execute("""DELETE FROM mdp WHERE id > 1""")
    conn.commit()
