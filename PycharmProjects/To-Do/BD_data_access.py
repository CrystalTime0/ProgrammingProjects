import sqlite3

conn = sqlite3.connect('to-do.db')
cursor = conn.cursor()


# -------------------- Initialize BD --------------------
def initialize_BD():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS to_do_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            time INTEGER NOT NULL,
            xp INTEGER NOT NULL,
            creation_date TEXT NOT NULL,
            description TEXT
            )  
        """)

    conn.commit()


initialize_BD()


# -------------------- GET DATA --------------------
def readcell(line, column):
    cursor.execute("SELECT * FROM to_do_list WHERE id = ?", (line,))
    conn.commit()
    bd_line = cursor.fetchone()

    if bd_line:
        return bd_line[column]
    else:
        print("cell not found")


def readline(line):
    cursor.execute("SELECT * FROM to_do_list WHERE id = ?", (line,))
    conn.commit()
    bd_line = cursor.fetchone()

    if bd_line:
        return bd_line
    else:
        print("line not found")


def readcolumn(column):
    cursor.execute(f"""SELECT {column} FROM to_do_list""")
    resultats = [line[0] for line in cursor.fetchall()]
    return resultats


def get_id_with_name(name):
    cursor.execute("""SELECT id FROM to_do_list WHERE name = ?""", (name,))
    conn.commit()
    id_found = cursor.fetchone()
    return id_found[0]


# -------------------- UPDATE DATA --------------------
def updatecell(line, column_title, data):
    cursor.execute(f"""UPDATE to_do_list SET {column_title} = ? WHERE id = ?""", (data, line))
    conn.commit()


def updateline(line, name, password):
    cursor.execute("""UPDATE to_do_list SET name = ?, mdp = ? WHERE id = ?""", (name, password, line))
    conn.commit()


# -------------------- ADD DATA --------------------
def addline(name, time, xp, creation_date, description):
    cursor.execute("""INSERT INTO to_do_list (name, time, xp, creation_date, description) 
                            VALUES (?, ?, ?, ?, ?)""", (name, time, xp, creation_date, description))
    conn.commit()


# -------------------- REMOVE DATA --------------------

def clearline(line):
    cursor.execute("""DELETE FROM to_do_list WHERE id = ?""", (line,))
    conn.commit()


def cleardata():
    cursor.execute("""DELETE FROM to_do_list""")
    conn.commit()
