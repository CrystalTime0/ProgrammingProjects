import random

option = ["pierre", "feuille", "ciseaux"]
score_ordi = 0
score_player = 0

while 3 != score_ordi and 3 != score_player:

    ordi_choice = random.choice(option)

    Player_choice = input("Choisissez parmi : pierre, feuille et ciseaux\n")

    if Player_choice == ordi_choice:
        print("Match nul")
        print(f"Ordi avait choisit {ordi_choice}")

    elif Player_choice == "pierre" and ordi_choice == "ciseaux":
        print("Player Win")
        score_player += 1
        print(f"Ordi avait choisit {ordi_choice}")

    elif Player_choice == "ciseaux" and ordi_choice == "feuille":
        print("Player Win")
        score_player += 1
        print(f"Ordi avait choisit {ordi_choice}")

    elif Player_choice == "feuille" and ordi_choice == "pierre":
        print("Player Win")
        score_player += 1
        print(f"Ordi avait choisit {ordi_choice}")

    else:
        print("Ordi Win")
        score_ordi += 1
        print(f"Ordi avait choisit {ordi_choice}")

    print(f"{score_player} : {score_ordi}")


if score_ordi == 3:
    print(f"The Game Is Over \n Ordi Win\n\n  {score_player} : {score_ordi}")

elif score_player == 3:
    print(f"The Game Is Over \n Player Win\n\n  {score_player} : {score_ordi}")
