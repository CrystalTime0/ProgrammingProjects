import random
import string

punctuation = "!#$%&*+-./:;=?@_!#$%&+-/:;=?@"
digits = string.digits
letters = string.ascii_letters

def generate_mdp():
    characters = []
    characters += letters

    while True:
        length_mdp = input("how many characters ?")
        if not length_mdp.isdigit():
            print("Please enter a valid number")
        elif length_mdp.isdigit():
            length_mdp = int(length_mdp)
            break

    while True:
        digits_ = input("digits ? (y/n)")
        if digits_ != "y" and digits_ != "n":
            print("PLease enter a valid answer.")
        elif digits_ == "y":
            characters += digits
            break
        elif digits_ == "n":
            break

    while True:
        punctuation_ = input("punctuation ? (y/n)")
        if punctuation_ != "y" and punctuation_ != "n":
            print("PLease enter a valid answer.")
        elif punctuation_ == "y":
            characters += punctuation
            break
        elif punctuation_ == "n":
            break

    # Selection mdp

    mdp_generated = []
    last_choice = ""
    for _ in range(length_mdp):
        choice = random.choice(characters)
        if choice != last_choice:
            mdp_generated += choice
            last_choice = choice

    mdp_string = ""
    for element in mdp_generated:
        mdp_string += element

    return mdp_string
