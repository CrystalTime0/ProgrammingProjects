import sqlite3

conn = sqlite3.connect('data/casino.db')
cursor = conn.cursor()


# -------------------- Initialize BD --------------------
def initialize_BD():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            min_bet INTEGER NOT NULL,
            max_bet INTEGER NOT NULL)""")

    cursor.execute("""    
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL ,
            bet_amount INTEGER NOT NULL,
            result TEXT NOT NULL,
            payout INTEGER,
            balance INTEGER,
            date TEXT NOT NULL)""")

    cursor.execute("""    
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL ,
                bet_amount INTEGER NOT NULL,
                balance INTEGER
                )""")

    conn.commit()


initialize_BD()


# -------------------- GET DATA --------------------
def readtable(table):
    cursor.execute(f"""SELECT * FROM {table}""")
    resultats = cursor.fetchall()
    return resultats


def readcell(line, column, table):
    cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (line,))
    conn.commit()
    bd_line = cursor.fetchone()

    if bd_line:
        return bd_line[column]
    else:
        print("cell not found")


def readline(line, table):
    cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (line,))
    conn.commit()
    bd_line = cursor.fetchone()

    if bd_line:
        return bd_line
    else:
        print("line not found")


def readcolumn(column, table):
    cursor.execute(f"""SELECT {column} FROM {table}""")
    resultats = [line[0] for line in cursor.fetchall()]
    return resultats


def get_id_with_name(name, table):
    cursor.execute(f"""SELECT id FROM {table} WHERE name = ?""", (name,))
    conn.commit()
    id_found = cursor.fetchone()
    return id_found[0]


# -------------------- UPDATE DATA --------------------
def updatecell(line, column_title, table, data):
    cursor.execute(f"""UPDATE {table} SET {column_title} = ? WHERE id = ?""", (data, line))
    conn.commit()


def updateline(line, name, password, table):
    cursor.execute(f"""UPDATE {table} SET name = ?, mdp = ? WHERE id = ?""", (name, password, line))
    conn.commit()


# -------------------- ADD DATA --------------------
def addline(name, password, table):
    cursor.execute(f"""INSERT INTO {table} (name,password) VALUES (?, ?)""", (name, password))
    conn.commit()


# -------------------- REMOVE DATA --------------------

def clearline(line, table):
    cursor.execute(f"""DELETE FROM {table} WHERE id = ?""", (line,))
    conn.commit()


def cleardata(table):
    cursor.execute(f"""DELETE FROM {table}""")
    conn.commit()
