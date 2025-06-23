from Password_Generator import generate_mdp
from Folder_Manip import read_folder
from Crytpter import hash_
from gui1 import Page1
all_Password = read_folder()

file = open("C:\\Users\\Raphaël\\PycharmProjects\\Password Manager\\config.txt", "r")
if file.readlines()[0] == "0\n":
    print(file.readlines())
    lignes = []
    for i in file.readlines():
        lignes.append(file.readlines()[i])
        print(lignes)

    print(lignes)
    lignes[0] = 1
    lignes[1] = hash_(input("Hi, PLease set up your main Password\n"))
    file.close()
    file = open("C:\\Users\\Raphaël\\PycharmProjects\\Password Manager\\config.txt", "w")
    file.writelines(lignes)
    file.close()

file = open("C:\\Users\\Raphaël\\PycharmProjects\\Password Manager\\config.txt", "r")
print(file.readlines())




while True:
    file = open("C:\\Users\\Raphaël\\PycharmProjects\\Password Manager\\config.txt", "r+")
    user_mdp = input("Main Password ?\n")
    if hash_(user_mdp) == file.readlines()[1]:
        Master_key = user_mdp
        break
    else:
        print("Incorrect Password")

file.close()
while True:
    user_choice = input("What do you want to do ?\n\n1-Generate a Password\n2-Add a Password\n3-Delete a "
                        "Password\n4-Search a Password\n")

    if user_choice == "1":
        while True:
            mdp_generated = generate_mdp()
            print(mdp_generated)
            add_password_ = input("Do you want to add this Password to your list ? (y/n/new)\n")
            if add_password_ == "y":
                new_mdp_key = input("What name ?\n")

                """
                all_Password[new_mdp_key] = mdp_generated
                """

                fichier = open("C:\\Users\\Raphaël\\PycharmProjects\\Password Manager\\mdp.txt", "a")
                fichier.write(f"{new_mdp_key}\n")
                fichier.write(f"{mdp_generated}\n")
                fichier.close()
                all_Password = read_folder()
                break

            elif add_password_ == "n":
                break

            elif add_password_ != "y" and add_password_ != "n" and add_password_ != "new":
                print("PLease enter a valid answer.")

    if user_choice == "2":
        new_mdp_key = input("What name ?\n")
        new_mdp = input("Write the Password\n")
        fichier = open("C:\\Users\\Raphaël\\PycharmProjects\\Password Manager\\mdp.txt", "a")
        fichier.write(f"{new_mdp_key}\n")
        fichier.write(f"{new_mdp}\n")
        fichier.close()
        all_Password = read_folder()

    if user_choice == "3":

        for keys in all_Password:
            print(keys)
        while True:
            mdp_key_to_delete = input("What Password do you want to delete ?\n")
            if mdp_key_to_delete in read_folder():
                user_delete_choice = input(
                    f"Do you really want to delete this Password ? (y/n)\n {mdp_key_to_delete}   :  "
                    f" {all_Password[mdp_key_to_delete]}\n")
                while True:
                    if user_delete_choice == "y":
                        print("Your Password was deleted")

                        list_keys = []
                        for key in read_folder().keys():
                            list_keys.append(key)
                        del_mdp_3 = list_keys.index(mdp_key_to_delete) * 2

                        with open("C:\\Users\\Raphaël\\PycharmProjects\\Password Manager\\mdp.txt", "r+") as fp:
                            lines = fp.readlines()
                            fp.seek(0)
                            fp.truncate()
                            for number, line in enumerate(lines):
                                if number not in [del_mdp_3, del_mdp_3 + 1]:
                                    fp.write(line)

                        all_Password = read_folder()

                        break

                    elif user_delete_choice == "n":
                        break

                    elif user_delete_choice != "y" and user_delete_choice != "n":
                        print("PLease enter a valid answer.")

                break

            else:
                print("PLease enter a valid answer.")

    if user_choice == "4":
        for keys in all_Password:
            print(keys)
        while True:
            User_search = input("What Password are you looking for ?\n")
            if User_search in all_Password:
                print(f"Your Password is {User_search}   :   {all_Password[User_search]}")
                break
            else:
                print("PLease enter a valid answer.")

    elif user_choice != "1" and user_choice != "2" and user_choice != "3" and user_choice != "4":
        print("PLease enter a valid answer.")
