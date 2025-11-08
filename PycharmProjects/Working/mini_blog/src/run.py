import sqlite3

from BD_data_access import BDaccess
from datetime import datetime

db_user = BDaccess("user", ["username", "password", "creation time"],
                   """username TEXT NOT NULL UNIQUE,
                                           password TEXT NOT NULL,
                                           creation_time DATETIME NOT NULL
                                           """)

current_user: str = ""

while True:
    try:
        log_in = input('Do you want to log in? (y/n): ').lower().startswith('y')
    except Exception as e:
        raise ValueError(e)
    if log_in:
        print("LOG IN".center(20, "-"))
        login_username = input("username ? : ")
        login_password = input("password ? : ")
        if db_user.get_with_("password", "username", login_username):
            current_user = login_username
            break
        else:
            print("username or password incorrect")

    else:
        print("SIGN UP".center(20, "-"))
        sign_up_username = input("username ? : ")
        sign_up_password = input("password ? : ")
        try:
            db_user.addline([sign_up_username, sign_up_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")], db_user.descriptors)
        except sqlite3.OperationalError as e:
            print("Something get wrong please try again later\n", e)
            continue
        break

print("out of log in")