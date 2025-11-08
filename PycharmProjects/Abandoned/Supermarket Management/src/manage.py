from BD_data_access import *
import sqlite3
import random

conn = sqlite3.connect('data/supermarket.db')
cursor = conn.cursor()


def open_manage_employees():
    while True:
        user_choice = input("""
        1-hire employee
        2-fire employee
        3-see employee

        """)

        if user_choice == "1":
            employees_possibilities = []
            for i in range(3):
                employees_possibilities.append([i, name, random.randint(10, 30), random.randint(1, 50)/10])


        elif user_choice == "2":
            while True:
                fire_employee_user_choice = input("Quel employee voulez-vous fire ? (id) (cancel)")
                if fire_employee_user_choice == "cancel":
                    break
                if readline(fire_employee_user_choice, "employees"):
                    clearline(fire_employee_user_choice, "employees")
                    break
                else:
                    print("enter valid answer")

        elif user_choice == "3":
            cursor.execute(f'SELECT * FROM employees')
            column = [description[0] for description in cursor.description]
            cursor.close()
            print(" | ".join(column))
            for line in readtable("employees"):
                print(f"{line[0]} | {line[1]} | {line[2]} | {line[3]}")

        else:
            print("Please enter a valid choice")

        print("______________________________________________________")


open_manage_employees()
