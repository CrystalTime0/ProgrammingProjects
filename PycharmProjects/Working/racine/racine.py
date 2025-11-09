def racine(n: str, rang: int):
    racine_calculee = ""  # valeur de la racine calculée

    # Si la longueur est impaire, on ajoute un zéro devant
    if len(n) % 2 == 1:
        n = "0" + n

    # On regroupe les chiffres par deux
    groupes = [n[i * 2:i * 2 + 2] for i in range(len(n) // 2)]

    # On complète avec des "00" pour obtenir la précision voulue
    while len(groupes) < rang:
        groupes.append("00")

    print("Groupes :", groupes)

    # Trouver le plus grand carré inférieur ou égal au premier groupe
    carre_max = 0
    while (carre_max + 1) ** 2 <= int(groupes[0]):
        carre_max += 1

    racine_calculee += str(carre_max)
    reste = int(groupes[0]) - carre_max ** 2

    # Étape suivante : itération pour chaque rang
    for i in range(1, rang):
        # On descend le groupe suivant
        nombre = int(str(reste) + groupes[i])

        # On cherche le plus grand chiffre x tel que (20*racine + x)*x <= nombre
        prefixe = int(racine_calculee) * 20
        x = 0
        while (prefixe + (x + 1)) * (x + 1) <= nombre:
            x += 1

        # On met à jour la racine et le reste
        racine_calculee += str(x)
        reste = nombre - (prefixe + x) * x

    print("Racine approchée :", racine_calculee)
    return racine_calculee


# Exemple :
racine("117", 3)