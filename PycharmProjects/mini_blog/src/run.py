import sqlite3
from ftplib import print_line

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
    print_line("#" * 40)
    print_line(" COMPTE ADMINISTRATEUR ".center(40,"#"))
    print_line("#" * 40)
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

print("\n","TOPICS".center(20, "-"))
for index, topic in enumerate(topics):
    print(f"{index + 1} - {topic}")