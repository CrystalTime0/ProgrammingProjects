import pyxel
import random


#########VARIABLES GLOBALE
r1_x = 12
r1_y = 108
r2_x = 240
r2_y = 108
b_x = 128
b_y = 128
dx = 4
dy = 4
score1 = 0
score2 = 0
message = ""

# Timer (30 secondes à 30 fps = 900 frames)
timer = 0
TIMER_MAX = 3600
timer_actif = True

# Compte à rebours de début (3 secondes = 90 frames)
countdown = 90
countdown_actif = True

# Traînée de la balle
trail = []

# Clignotement message fin
blink_timer = 0


################### Fonctions annexes

def deplacer_r1():
    global r1_y
    if pyxel.btn(pyxel.KEY_S):
        r1_y = max(4, r1_y - 4)
    if pyxel.btn(pyxel.KEY_X):
        r1_y = min(252 - 36, r1_y + 4)

def deplacer_r2():
    global r2_y
    if pyxel.btn(pyxel.KEY_UP):
        r2_y = max(4, r2_y - 4)
    if pyxel.btn(pyxel.KEY_DOWN):
        r2_y = min(252 - 36, r2_y + 4)

def rebondir():
    global b_x, b_y
    # Bords haut et bas (rayon balle = 4)
    if b_y - 4 <= 4 or b_y + 4 >= 252:
        return 'vertical'
    # Raquette joueur 1 : balle vient de droite, rayon inclus
    if (r1_x + 4 >= b_x - 4 >= r1_x - 4 and
            r1_y - 4 <= b_y <= r1_y + 36 + 4):
        b_x = r1_x + 6
        return 'horizontal'
    # Raquette joueur 2 : balle vient de gauche, rayon inclus
    if (r2_x <= b_x + 4 <= r2_x + 8 and
            r2_y - 4 <= b_y <= r2_y + 36 + 4):
        b_x = r2_x - 2
        return 'horizontal'
    if b_x < 0 or b_x > 256:
        return 'out'
    return ''

def reset_balle(gagnant):
    global b_x, b_y, dx, dy
    trail.clear()
    if gagnant == 1:
        b_x = r2_x - 10
        b_y = r2_y + 18
        dx = -4
    else:
        b_x = r1_x + 10
        b_y = r1_y + 18
        dx = 4
    dy = 4

def dessiner_raquette(x, y, couleur_bord, couleur_centre):
    pyxel.rect(x, y, 4, 36, couleur_bord)
    pyxel.rect(x + 1, y + 2, 2, 32, couleur_centre)
    pyxel.pset(x + 1, y + 1, 7)
    pyxel.pset(x + 2, y + 1, 7)
    pyxel.pset(x + 1, y + 34, 7)
    pyxel.pset(x + 2, y + 34, 7)

def dessiner_balle(x, y):
    pyxel.circ(x, y, 6, 1)
    pyxel.circ(x, y, 4, 7)
    pyxel.pset(x - 1, y - 1, 7)
    pyxel.pset(x, y - 2, 7)

def dessiner_score(s1, s2):
    pyxel.rect(74, 6, 20, 9, 1)
    pyxel.rect(162, 6, 20, 9, 1)
    pyxel.text(80, 8, str(s1), 7)
    pyxel.text(168, 8, str(s2), 7)
    pyxel.text(126, 8, ":", 13)

###################Calculs indispensable au jeu
def calculer():
    global b_x, b_y, dx, dy, score1, score2, message, blink_timer, timer, timer_actif, countdown, countdown_actif

    deplacer_r1()
    deplacer_r2()

    # Compte à rebours de début
    if countdown_actif:
        countdown -= 1
        if countdown <= 0:
            countdown_actif = False
        return

    blink_timer += 1

    # Mise à jour du timer
    if timer_actif and score1 < 10 and score2 < 10:
        timer += 1
        if timer >= TIMER_MAX:
            timer_actif = False
            if score1 > score2:
                message = "Joueur 1 gagne !"
            elif score2 > score1:
                message = "Joueur 2 gagne !"
            else:
                message = "Egalite !"

    if score1 >= 10 or score2 >= 10 or not timer_actif:
        if pyxel.btnp(pyxel.KEY_SPACE):
            score1 = 0
            score2 = 0
            message = ""
            timer = 0
            timer_actif = True
            countdown = 90
            countdown_actif = True
            reset_balle(2)
        return

    trail.append((b_x, b_y))
    if len(trail) > 8:
        trail.pop(0)

    resultat = rebondir()

    if resultat == 'vertical':
        dy *= -1
    elif resultat == 'horizontal':
        dx *= -1
    elif resultat == 'out':
        if b_x < 0:
            score2 += 1
            if score2 >= 10:
                message = "Joueur 2 gagne !"
            reset_balle(1)
            return
        else:
            score1 += 1
            if score1 >= 10:
                message = "Joueur 1 gagne !"
            reset_balle(2)
            return

    b_x += dx
    b_y += dy

###################Affichage des objets du jeu
def afficher():
    pyxel.cls(0)

    # --- Bordures ---
    pyxel.rect(0, 0, 256, 4, 7)
    pyxel.rect(0, 252, 256, 4, 7)
    pyxel.line(0, 4, 255, 4, 13)
    pyxel.line(0, 251, 255, 251, 13)

    # --- Ligne centrale pointillée ---
    for i in range(-5, 257, 21):
        pyxel.rect(126, i, 4, 12, 13)
        pyxel.rect(127, i + 1, 2, 10, 7)

    # --- Traînée de la balle ---
    for i, (tx, ty) in enumerate(trail):
        alpha = i + 1
        if alpha <= 2:
            col = 1
        elif alpha <= 4:
            col = 5
        elif alpha <= 6:
            col = 6
        else:
            col = 13
        pyxel.circ(tx, ty, 2, col)

    # --- Raquettes ---
    dessiner_raquette(r1_x, r1_y, 6, 7)
    dessiner_raquette(r2_x, r2_y, 8, 7)

    # --- Balle ---
    dessiner_balle(b_x, b_y)

    # --- Scores ---
    dessiner_score(score1, score2)

    # --- Timer ---
    secondes_restantes = max(0, (TIMER_MAX - timer) // 30)
    couleur_timer = 8 if secondes_restantes <= 10 else 7
    pyxel.text(118, 8, str(secondes_restantes) + "s", couleur_timer)

    # --- Compte à rebours de début ---
    if countdown_actif:
        chiffre = (countdown // 30) + 1
        if chiffre > 3:
            chiffre = 3
        if chiffre == 0 or countdown <= 0:
            label = "GO!"
            couleur = 11
        else:
            label = str(chiffre)
            couleur = 10 if chiffre == 1 else (9 if chiffre == 2 else 7)
        # Grand affichage centré
        pyxel.text(120, 110, label, 1)   # ombre
        pyxel.text(119, 109, label, couleur)

    # --- Message fin de match ---
    if message:
        pyxel.rect(20, 100, 216, 50, 1)
        pyxel.rectb(20, 100, 216, 50, 7)
        if blink_timer % 40 < 30:
            if message.startswith("Joueur 1"):
                pyxel.text(60, 115, message, 10)
            else:
                pyxel.text(60, 115, message, 8)
            pyxel.text(55, 130, "ESPACE pour rejouer", 13)

##############lancement du programme
pyxel.init(256, 256)
pyxel.run(calculer, afficher)