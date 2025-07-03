import sqlite3

conn = sqlite3.connect('to-do.db')
cursor = conn.cursor()


# -------------------- Initialize BD --------------------
def initialize_BD(all_username):
    for name in all_username:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                time INTEGER NOT NULL,
                xp INTEGER NOT NULL,
                creation_date TEXT NOT NULL,
                description TEXT
                )  
            """)

    conn.commit()


# -------------------- GET DATA --------------------
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
def updatecell(line, column_title, data, table):
    cursor.execute(f"""UPDATE {table} SET {column_title} = ? WHERE id = ?""", (data, line))
    conn.commit()


def updateline(line, name, password):
    cursor.execute("""UPDATE to_do_list SET name = ?, mdp = ? WHERE id = ?""", (name, password, line))
    conn.commit()


# -------------------- ADD DATA --------------------
def addline(name, time, xp, creation_date, description, table):
    cursor.execute(f"""INSERT INTO {table} (name, time, xp, creation_date, description) 
                            VALUES (?, ?, ?, ?, ?)""", (name, time, xp, creation_date, description))
    conn.commit()


# -------------------- REMOVE DATA --------------------

def clearline(line, table):
    cursor.execute(f"""DELETE FROM {table} WHERE id = ?""", (line,))
    conn.commit()


def cleardata(table):
    cursor.execute(f"""DELETE FROM {table}""")
    conn.commit()
