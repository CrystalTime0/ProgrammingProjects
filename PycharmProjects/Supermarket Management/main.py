from sqlite3 import *
from BD_data_access import *
from random import *

start_fund = 500
current_fund = start_fund

while True:
    user_choice = input("""
    1-manage employee
    2-manage products
    3-manage fund
    
    """)

    if user_choice == "1":
        pass

    elif user_choice == "2":
        pass

    elif user_choice == "3":
        pass

    else:
        print("Please enter a valid choice")

    print("______________________________________________________")