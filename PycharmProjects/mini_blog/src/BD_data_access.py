import sqlite3


conn = sqlite3.connect('data/data.db')
cursor = conn.cursor()


class BDaccess:
    def __init__(self, table: str, descriptors: list, descriptors_and_properties: str):
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table} ({descriptors_and_properties})""")
        # cursor.execute("""INSERT OR IGNORE INTO mdp (name, password) VALUES(?, ?)""", ("main", ""))
        conn.commit()

        self.table = table
        self.descriptors = descriptors

    # -------------------- GET DATA --------------------
    def readcell(self, id_, column):
        cursor.execute(f"SELECT * FROM {self.table} WHERE id = ?", (id_,))
        conn.commit()
        bd_line = cursor.fetchone()

        if bd_line:
            return bd_line[column]
        else:
            print("cell not found")
            return None

    def readline(self, line):
        cursor.execute(f"SELECT * FROM {self.table} WHERE id = ?", (line,))
        conn.commit()
        bd_line = cursor.fetchone()

        if bd_line:
            return bd_line
        else:
            print("line not found")
            return None

    def readcolumn(self, column):
        cursor.execute(f"""SELECT {column} FROM {self.table}""")
        resultats = [line[0] for line in cursor.fetchall()]
        return resultats

    def get_with_(self,val_to_get,  descriptor, value):
        try:
            cursor.execute(f"""SELECT {val_to_get} FROM {self.table} WHERE {descriptor} = {value}""")
        except sqlite3.OperationalError:
            return None

        conn.commit()
        id_found = cursor.fetchone()
        return id_found[0]

    # -------------------- UPDATE DATA --------------------
    def updatecell(self, line, column_title, data):
        cursor.execute(f"""UPDATE {self.table} SET {column_title} = ? WHERE id = ?""", (data, line))
        conn.commit()

    # -------------------- ADD DATA --------------------
    def addline(self, values: list, columns: list[str]):
        """
        Ajoute une ligne dans la table self.table.

        :param values: Liste des valeurs à insérer
        :param columns: Liste des noms de colonnes
        """
        if len(values) != len(columns):
            raise ValueError(f"Nombre de valeurs ({len(values)}) != nombre de colonnes ({len(columns)})")

        cols_str = ",".join(columns)
        placeholders = ",".join(["?"] * len(values))

        query = f"INSERT INTO {self.table} ({cols_str}) VALUES ({placeholders})"

        cursor.execute(query, tuple(values))
        conn.commit()

    # -------------------- REMOVE DATA --------------------

    def clearline(self, line):
        cursor.execute(f"""DELETE FROM {self.table} WHERE id = ?""", (line,))
        conn.commit()

    def cleardata(self):
        cursor.execute(f"""DELETE FROM {self.table} WHERE id > 1""")
        conn.commit()
