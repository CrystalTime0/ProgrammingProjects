from random import randint

def get_rank(dices):
    d = sorted(dices)
    if d == [1,2,4]:
        return 1
    if d == [1,1,1]:
        return 2
    if (d.count(1) == 2 and 6 in d) or d == [6,6,6]:
        return 3
    if (d.count(1) == 2 and 5 in d) or d == [5,5,5]:
        return 4
    if (d.count(1) == 2 and 4 in d) or d == [4,4,4]:
        return 5
    if (d.count(1) == 2 and 3 in d) or d == [3,3,3]:
        return 6
    if (d.count(1) == 2 and 2 in d) or d == [2,2,2]:
        return 7
    if d[0]+1 == d[1] and d[1]+1 == d[2]:
        return 8
    if d == [1,2,2]:
        return 9
    return 10

def compare(d1, d2):
    r1 = get_rank(d1)
    r2 = get_rank(d2)
    if r1 < r2:
        return 1
    elif r2 < r1:
        return 2
    else:
        # même rang, on compare dés décroissants
        sd1 = sorted(d1, reverse=True)
        sd2 = sorted(d2, reverse=True)
        if sd1 > sd2:
            return 1
        elif sd2 > sd1:
            return 2
        else:
            return 0  # égalité

def lancer_des():
    return [randint(1,6) for _ in range(3)]

def tour_de_jeu(joueur, forced_throws=None):
    nb_lancers = 1
    des = lancer_des()
    print(f"{joueur['nom']} lance : {des}")

    while nb_lancers < 3 and (forced_throws is None or nb_lancers < forced_throws):
        rep = input(f"{joueur['nom']}, relancer ? (y/n) : ").lower()
        if rep != 'y':
            break
        dés_a_relancer = input("Quels dés relancer ? (ex: 13 pour 1er et 3ème) : ")
        for c in dés_a_relancer:
            if c in '123':
                des[int(c)-1] = randint(1,6)
        print(f"{joueur['nom']} relance : {des}")
        nb_lancers += 1

    return des, nb_lancers

def jetons_par_rang(rank):
    barème = {
        1: 10,
        2: 7,
        3: 6,
        4: 5,
        5: 4,
        6: 3,
        7: 2,
        8: 2,
        9: 2,
        10:1
    }
    return barème.get(rank,1)

def main():
    pot = 21
    joueurs = []
    for i in range(2):
        nom = input(f"Nom du joueur {i+1} : ")
        joueurs.append({'nom': nom, 'jetons': 0})

    print("\nDétermination du joueur qui commence :")
    lancers = []
    for j in joueurs:
        d = lancer_des()
        print(f"{j['nom']} lance : {d}")
        lancers.append((j, d))

    # comparer
    r = compare(lancers[0][1], lancers[1][1])
    if r == 1:
        premier = lancers[0][0]
    elif r == 2:
        premier = lancers[1][0]
    else:
        print("Égalité, on relance.")
        return main()  # relance la fonction

    print(f"{premier['nom']} commence.\n")

    phase_decharge = False

    while True:
        print(f"\nPot : {pot}")
        print(f"Jetons : {joueurs[0]['nom']}={joueurs[0]['jetons']}, {joueurs[1]['nom']}={joueurs[1]['jetons']}")
        print(f"C'est au tour de {premier['nom']}.")

        des_premier, nb_lancers = tour_de_jeu(premier)

        # autre joueur
        autre = joueurs[1] if joueurs[0] == premier else joueurs[0]
        print(f"\n{autre['nom']} doit faire {nb_lancers} lancers.")
        des_autre, _ = tour_de_jeu(autre, forced_throws=nb_lancers)

        gagnant_num = compare(des_premier, des_autre)

        if gagnant_num == 0:
            print("Égalité, pas de changement.")
            continue
        gagnant = premier if gagnant_num == 1 else autre
        perdant = autre if gagnant_num == 1 else premier

        print(f"Gagnant du tour : {gagnant['nom']}")

        rang_gagnant = get_rank(des_premier if gagnant == premier else des_autre)
        nb_jetons = jetons_par_rang(rang_gagnant)

        if not phase_decharge:
            # phase charge
            jetons_pris = min(nb_jetons, pot)
            perdant['jetons'] += jetons_pris
            pot -= jetons_pris
            print(f"{perdant['nom']} prend {jetons_pris} jeton(s) du pot.")
            if pot == 0:
                print("\nLe pot est vide. On passe à la phase de décharge.")
                phase_decharge = True
        else:
            # phase décharge
            jetons_retires = min(nb_jetons, gagnant['jetons'])
            gagnant['jetons'] -= jetons_retires
            print(f"{gagnant['nom']} défausse {jetons_retires} jeton(s).")

        # le prochain tour commence
if __name__ == "__main__":
    main()