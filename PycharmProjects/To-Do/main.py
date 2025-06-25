import json
import sqlite3
import BD_data_access

data_user = {"1": 30}


def save_data():
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data_user, f, indent=4, ensure_ascii=False)
        print("data saved")


def load_data():
    global data_user
    with open("data.json", "r", encoding="utf-8") as f:
        data_user = json.load(f)

