from BD_data_access import *
from Crytpter import hash_, crypt, decrypt
from Password_Generator import *

while True:
    if readcell(1, 2) == "":
        updatecell(1, "password", hash_(str(input("Define your main Password\n$ "))))

    else:
        user_try_mdp = str(input("Main Password : \n$ "))

        if hash_(user_try_mdp) == readcell(1, 2):
            break

        if user_try_mdp == "forget":
            updatecell(1, "password", "")
            continue

        else:
            print("Invalid password")

while True:
    print("___________________________________")
    user_choice = input("""
1-Add password
2-Remove password
3-Generate password
4-Show all password
5-Delete all password
6-Change main password
$ """)

    if user_choice == "1":
        new_password_name = str(input("\nWhat name ?\n$ "))
        new_password = str(input("Password:\n$ "))
        addline(new_password_name, crypt(new_password))
        print("password added")

    elif user_choice == "2":
        password_to_delete = input("\n What password do you would like to delete ?\n$ ")
        if password_to_delete in readcolumn("name"):
            clearline(get_id_with_name(password_to_delete))
            print(f"The password {password_to_delete} has been deleted")
        else:
            print("Enter a valid name")

    elif user_choice == "3":
        while True:
            new_generated_mdp = generate_mdp()
            user_choice_generated_password = input(f"The password generated is : {new_generated_mdp}"
                                                   f" (yes/another/cancel)\n$ ")

            if user_choice_generated_password == "yes":
                addline(input("What name ?\n$ "), crypt(new_generated_mdp))
                print("password added")
                break

            elif user_choice_generated_password == "another":
                continue

            elif user_choice_generated_password == "cancel":
                break

            else:
                print("Please enter a valid answer")

    elif user_choice == "4":
        invalid_key_password_count = 0
        cursor.execute(f'SELECT * FROM mdp')
        column = [description[0] for description in cursor.description]
        column = column[1:]

        # Construire la requête SELECT avec seulement les colonnes souhaitées
        request = f"SELECT {', '.join(column)} FROM mdp"
        cursor.execute(request)
        lines = cursor.fetchall()

        # Afficher les résultats
        print(" | ".join(column))
        invalid_passwords = []
        for line in lines[1:]:  # sauf la premiere colonne
            print(f"{line[0]} : {decrypt(line[1])}")
            if decrypt(line[1]) == "Invalid key":
                invalid_key_password_count += 1
                invalid_passwords.append(line[0])

        if invalid_key_password_count > 0:
            print(f"\n{invalid_key_password_count} "
                  f"passwords could not be decrypted because the main password is not the same as during encryption")

            if input("Do you want to delete these password ? (y/n)\n$ ") == "y":
                for name in invalid_passwords:
                    clearline(get_id_with_name(name))

                print("All invalid password have been deleted")

    elif user_choice == "5":
        if hash_(input("\nEnter your main password to continue :\n$ ")) == readcell(1, 2):
            cleardata()
            print("All your password have been deleted")
        else:
            print("Invalid password")
        continue

    elif user_choice == "6":
        encrypt_password = {}
        cursor.execute("""SELECT name, password FROM mdp""")
        all_passwords = cursor.fetchall()
        all_passwords_name = []
        for i in all_passwords[1:]:
            encrypt_password[i[0]] = decrypt(i[1])
            all_passwords_name.append(i[0])
        cleardata()
        updatecell(1, "password", hash_(str(input("new main password\n$ "))))
        for i in range(len(all_passwords[1:])):
            addline(all_passwords_name[i], crypt(encrypt_password[all_passwords_name[i]]))

    else:
        print("Invalid choice")
