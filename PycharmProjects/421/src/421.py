#
#    .----------------.  .----------------.  .----------------.
#   | .--------------. || .--------------. || .--------------. |
#   | |   _    _     | || |    _____     | || |     __       | |
#   | |  | |  | |    | || |   / ___ `.   | || |    /  |      | |
#   | |  | |__| |_   | || |  |_/___) |   | || |    `| |      | |
#   | |  |____   _|  | || |   .'____.'   | || |     | |      | |
#   | |      _| |_   | || |  / /____     | || |    _| |_     | |
#   | |     |_____|  | || |  |_______|   | || |   |_____|    | |
#   | |              | || |              | || |              | |
#   | '--------------' || '--------------' || '--------------' |
#    '----------------'  '----------------'  '----------------'
#
# Desc : Jeu de dés 421 - logique, valeur combinaisons, affichage console
# Version : 1.0.0
# Date : 2025-10-13
#
# Signatures :
#   - Raphaël VILLARD        (Développeur principal)      Date: 2025-10-13
#

import random
from collections import Counter


# -------------------------------------------------
# Fonctions utilitaires
# -------------------------------------------------

def lancer_des(nb=3):
    """Lance nb dés et retourne une liste triée décroissante."""
    return sorted([random.randint(1, 6) for _ in range(nb)], reverse=True)


def relancer_des(des, indices):
    """Relance les dés des indices donnés"""
    for i in indices:
        des[int(i) - 1] = random.randint(1, 6)
    return des


# -------------------------------------------------
# Évaluation des combinaisons du 421
# -------------------------------------------------

def evaluer_combinaison(des):
    """
    Retourne (rang, jetons, nom)
    rang = ordre de force de la combinaison
    jetons = nombre de jetons à distribuer
    """
    des = sorted(des, reverse=True)
    counts = Counter(des)
    #  d1, d2, d3 = des

    # Ordre des dés pour comparaison
    val_d = {1: 7, 6: 6, 5: 5, 4: 4, 3: 3, 2: 2}

    # --- Cas spéciaux ---
    if des == [4, 2, 1]:
        return 100, 10, "421"
    if des == [1, 1, 1]:
        return 99, 7, "3 As"
    if des == [2, 2, 1]:
        return 1, 2, "Nénette"

    # --- Doubles As + autre dé ---
    if counts[1] == 2:
        autre = [x for x in des if x != 1][0]
        jetons = autre
        return 90 + autre, jetons, f"2 As + {autre}"

    # --- Trois dés identiques ---
    if len(counts) == 1:
        n = des[0]
        jetons = {6: 6, 5: 5, 4: 4, 3: 3, 2: 2}[n]
        return 80 + n, jetons, f"3 x {n}"

    # --- Suites ---
    if des in ([6, 5, 4], [5, 4, 3], [4, 3, 2]):
        return 40, 2, f"Suite {des}"
    if des == [3, 2, 1]:
        return 30, 1, "3-2-As"

    # --- Autres combinaisons ---
    return 10 + sum(val_d[d] for d in des) / 10, 1, f"Autre {des}"


# -------------------------------------------------
# Jeu d’un tour
# -------------------------------------------------

def jouer_tour(joueur, relances_max=3):
    """Tour d’un joueur avec possibilité de relances."""
    des = lancer_des()
    print(f"\n🎲 {joueur} lance : {des}")

    for relance in range(relances_max - 1):
        choix = input(f"{joueur}, relancer des dés ? (o/n) ").lower()
        if choix == 'o':
            indices = input("Quels dés (1,2,3) ? ex: 1 3 : ")
            try:
                des = relancer_des(des, indices)
                print(f"Nouveau tirage : {des}")
            except ValueError:
                print("Entrée invalide.")
        else:
            break

    rang, jetons, nom = evaluer_combinaison(des)
    print(f"→ {joueur} obtient {nom}  : {jetons} jetons, rang {rang}")
    return rang, jetons, nom, des


# -------------------------------------------------
# Manche de jeu
# -------------------------------------------------
def manche(joueurs, pot, phase="charge"):
    """Joue une manche avec gestion des égalités pour le meilleur et le pire."""
    print(f"\n=== Manche de {phase.upper()} ===")
    resultats = {}

    # Chaque joueur joue son tour
    for j in joueurs:
        resultats[j] = jouer_tour(j)  # rang, jetons, nom, des ex : {'raph' : (92,2, '2 As + 2', [1, 2, 1])}

    # Classement par rang (du meilleur au pire)
    classement = sorted(resultats.items(), key=lambda x: x[1][0], reverse=True)  # x = [(joueur, (rang, jetons, nom, des)),(joueur, data)]
    meilleurs_rang = classement[0][1][0]
    pires_rang = classement[-1][1][0]

    # Vérifier égalité du meilleur et du pire
    nb_meilleurs = sum(1 for j in classement if j[1][0] == meilleurs_rang)
    nb_pires = sum(1 for j in classement if j[1][0] == pires_rang)

    if nb_meilleurs > 1 or nb_pires > 1:
        print("⚠️ Égalité détectée entre le meilleur ou le pire ! Le tour est annulé.")
        # On retourne le pot inchangé et None pour indiquer aucun jeton distribué
        if phase == "charge":
            return pot, None, 0
        else:
            return pot, None, None, 0

    # Sinon, distribuer les jetons normalement
    meilleur = classement[0]
    pire = classement[-1]
    print(f"\n⭐ Meilleur : {meilleur[0]} avec {meilleur[1][2]}")
    print(f"💀 Pire : {pire[0]} avec {pire[1][2]}\n")
    if pire[1][3] == [2, 2, 1]:
        jetons_a_donner = 2
    else:
        jetons_a_donner = meilleur[1][1]

    if phase == "charge":
        jetons_effectifs = min(jetons_a_donner, pot)
        pot -= jetons_effectifs
        print(f"{pire[0]} reçoit {jetons_effectifs} jetons du pot.")
        return pot, pire[0], jetons_effectifs
    else:  # décharge
        print(f"{pire[0]} reçoit {jetons_a_donner} jetons de {meilleur[0]}.")
        return pot, pire[0], meilleur[0], jetons_a_donner

# -------------------------------------------------
# Jeu complet
# -------------------------------------------------

def jouer_421():
    print("=== Jeu du 421 ===")
    nb_joueurs = int(input("Nombre de joueurs : "))
    joueurs = [input(f"Nom du joueur {i + 1} : ") for i in range(nb_joueurs)]
    jetons = {j: 0 for j in joueurs}
    pot = 21


    # --- Manche de CHARGE ---
    while pot > 0:
        pot, perdant, nb = manche(joueurs, pot, "charge")
        if perdant is None:  # égalité => tour annulé
            continue
        jetons[perdant] += nb
        print(f"Pot restant : {pot}, jetons : {jetons}")

    print("\n=== Fin de la CHARGE ===")
    print("Début de la DÉCHARGE !")

    # --- Manche de DÉCHARGE ---
    while True:
        pot, perdant, gagnant, nb = manche(joueurs, pot, "décharge")
        if perdant is None:  # égalité => tour annulé
            continue

        jetons_a_transferer = min(nb, jetons[gagnant])
        jetons[gagnant] -= jetons_a_transferer
        jetons[perdant] += jetons_a_transferer
        if jetons[gagnant] < 0:  # évite les cas de total de jetons négatifs
            jetons[gagnant] = 0
        print(f"Jetons : {jetons}")

        for j, n in jetons.items():
            if n == 0:
                print(f"\n🏆 {j} a gagné la partie !")
                return


# -------------------------------------------------
# Lancer le jeu
# -------------------------------------------------
if __name__ == "__main__":
    jouer_421()