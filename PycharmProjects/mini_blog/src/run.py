#
#    __   __  ___   __    _  ___          _______  ___      _______  _______
#   |  |_|  ||   | |  |  | ||   |        |  _    ||   |    |       ||       |
#   |       ||   | |   |_| ||   |  ____  | |_|   ||   |    |   _   ||    ___|
#   |       ||   | |       ||   | |____| |       ||   |    |  | |  ||   | __
#   |       ||   | |  _    ||   |        |  _   | |   |___ |  |_|  ||   ||  |
#   | ||_|| ||   | | | |   ||   |        | |_|   ||       ||       ||   |_| |
#   |_|   |_||___| |_|  |__||___|        |_______||_______||_______||_______|
#
# Desc : mini-Blog gestion de topics, MP, message et log-in
# Version : 0.1.0
# Date : 2025-10-14
#
# Signatures :
#   - Raphaël VILLARD        (Développeur principal)      Date: 2025-10-13
#
print("\n    __   __  ___   __    _  ___          _______  ___      _______  _______\n   |  |_|  ||   | |  |  | ||   |        |  _    ||   |    |       ||       |\n   |       ||   | |   |_| ||   |  ____  | |_|   ||   |    |   _   ||    ___|\n   |       ||   | |       ||   | |____| |       ||   |    |  | |  ||   | __\n   |       ||   | |  _    ||   |        |  _   | |   |___ |  |_|  ||   ||  |\n   | ||_|| ||   | | | |   ||   |        | |_|   ||       ||       ||   |_| |\n   |_|   |_||___| |_|  |__||___|        |_______||_______||_______||_______|\n\nDesc : mini-Blog gestion de topics, MP, message et log-in\nVersion : 0.0.0\nDate : 2025-10-14\n\nSignatures :\n  - Raphaël VILLARD        (Développeur principal)      Date: 2025-10-13\n======================================================================================= \n\n")

import sqlite3

from BD_data_access import BDaccess
from datetime import datetime

#----------------------------------------------------------
#### SETUP ####
#----------------------------------------------------------
db_user = BDaccess("user", ["username", "password", "creation_time"],
                   """username TEXT NOT NULL UNIQUE,
                                           password TEXT NOT NULL,
                                           creation_time DATETIME NOT NULL
                                           """)
db_message = BDaccess("message", ["message", "user", "time", "topic"],
                    """message TEXT NOT NULL,
                                            user TEXT NOT NULL,
                                            time DATEIME NOT NULL,
                                            topic TEXT NOT NULL
                                            """)

current_user: str = ""
admin = True
#----------------------------------------------------------
#### LOGIN ####
#----------------------------------------------------------
if not admin:
    while True:
        try:
            log_in = input('Do you want to log in? (y/n): ').lower().startswith('y')
        except Exception as e:
            raise ValueError(e)
        if log_in:
            print("LOG IN".center(20, "-"))
            login_username = input("username ? : ")
            login_password = input("password ? : ")
            if db_user.get_with_("password", "username", login_username) == login_password:
                current_user = login_username
                break
            else:
                print("username or password incorrect")

        else:
            print("SIGN UP".center(20, "-"))
            sign_up_username = input("username ? : ")
            sign_up_password = input("password ? : ")
            try:
                db_user.addline([sign_up_username, sign_up_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            except sqlite3.OperationalError as e:
                print("Something get wrong please try again later\n", e)
                continue
            break
elif admin:
    print("#" * 40)
    print(" COMPTE ADMINISTRATEUR ".center(40,"#"))
    print("#" * 40)
#----------------------------------------------------------
#### False Data ####
#----------------------------------------------------------

db_message.addline(["bonjour", "raph", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "jardinage"])
db_message.addline(["bonjour", "raph", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "test"])
db_message.addline(["hello", "raph", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "jardinage"])

#----------------------------------------------------------
#### MENU ####
#----------------------------------------------------------
topics = list(set(db_message.readcolumn("topic")))

def display_topics_menu():
    print("\n","TOPICS".center(20, "-"))
    next_topics_index = 0
    if topics:
        for index, topic in enumerate(topics):
            print(f"{index + 1} - {topic}")
            next_topics_index = index + 1
    print(f"{next_topics_index} - Create a new topic")

def main():
    display_topics_menu()

if __name__ == "__main__":
    main()