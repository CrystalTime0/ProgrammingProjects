import json
import sqlite3
from datetime import date
from BD_data_access import *
import os
from Crytpter import *

current_user = ""

# -------------------- JSON MANIPULATION --------------------

data_file = "data.json"
all_users_data = {}
all_users_data_lenght = 0
all_users_names = []


def save_user_data(data):

    # Sauvegarder le tout
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        print("\nDonnées d'utilisateurs sauvegardées.")


def load_user_data():
    global all_users_data
    global all_users_data_lenght
    global all_users_names
    if not os.path.exists(data_file):
        print("Fichier de données introuvable.")
        return None

    with open(data_file, "r", encoding="utf-8") as f:
        all_users_data = json.load(f)
        all_users_names = list(all_users_data.keys())


# -------------------- LOGIN --------------------

def login():
    global current_user
    username = input("username ?")
    password = hash_(input("pwd ?"))
    if all_users_data[username]["password"] == password:
        print("authentication passed")
        current_user = username


# -------------------- SETUP --------------------
if __name__ == "__main__":
    load_user_data()
    print(all_users_names)
    initialize_BD(all_users_names)
    login()

    # -------------------- action --------------------

    while True:
        print("___________________________________")
        print(f"you have {all_users_data[current_user]["xp"]} xp")
        user_choice = input("""
    1-Add task
    2-Remove task
    3-Display tasks

    $ """)

        if user_choice == "1":
            task_name = input("name ?")
            task_description = input("description ?")
            expected_time_to_finish_task = input("time ?")
            experience_task = input("xp ?")
            actual_date = date.today()
            addline(task_name, expected_time_to_finish_task, experience_task, actual_date, task_description,
                    current_user)

        elif user_choice == "2":
            clearline(get_id_with_name(input("what task do you want to delete ? (name)"), current_user), current_user)

        elif user_choice == "3":
            cursor.execute(f'SELECT * FROM {current_user}')
            column = [description[0] for description in cursor.description]
            column = column[1:]

            # Construire la requête SELECT avec seulement les colonnes souhaitées
            request = f"SELECT {', '.join(column)} FROM {current_user}"
            cursor.execute(request)
            lines = cursor.fetchall()

            # Afficher les résultats
            print(" | ".join(column))
            invalid_passwords = []
            for line in lines:
                print(" | ".join(map(str, line)))

        save_user_data(all_users_data)





