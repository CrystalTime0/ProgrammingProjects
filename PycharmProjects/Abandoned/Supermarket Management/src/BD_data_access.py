import sqlite3

conn = sqlite3.connect('data/supermarket.db')
cursor = conn.cursor()


# -------------------- Initialize BD --------------------
def initialize_BD():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            cost INTEGER NOT NULL,
            reputation FLOAT NOT NULL)""")

    cursor.execute("""    
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price FLOAT NOT NULL,
            cost FLOAT NOT NULL,
            stock INTEGER,
            yesterday_sales INTEGER,
            demand FLOAT NOT NULL)""")

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
