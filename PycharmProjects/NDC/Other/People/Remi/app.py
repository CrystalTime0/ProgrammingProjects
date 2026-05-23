# importation des modules nécessaires
import pyxel
import time

#########VARIABLES GLOBALE
#ici on définit toutes les variables globales
#coo raquettes
r1_x = 12
r1_x_old = 12 #x frame avant
r1_y = 108
r1_y_old = 108 #y frame avant
r2_x = 240
r2_x_old = 240 #x frame avant
r2_y = 108
r2_y_old = 108 #y frame avant
#coo balle
b_x = 20
b_y = 116
dx = 4
dy = 4
#scores
score1 = 0
score2 = 0
#gagne
gagne1 = False
gagne2 = False
#restart si gagne
restart = False
#si le jeu est demarre
jeu_demarre = False
#si le son de debut a deja ete joue
son_debut_joue = False

################### On placera les fonctions annexes ci-dessous
def reset():
    global r1_x, r1_y, r2_x, r2_y, b_x, b_y, dx, dy, score1, score2, gagne1, gagne2, restart, jeu_demarre, son_debut_joue
    #coo raquettes
    r1_x = 12
    r1_y = 108
    r2_x = 240
    r2_y = 108
    #coo balle
    b_x = 20
    b_y = 116
    dx = 4
    dy = 4
    #scores
    score1 = 0
    score2 = 0
    #gagne
    gagne1 = False
    gagne2 = False
    #restart si gagne
    restart = False
    #si le jeu est demarre
    jeu_demarre = False
    #si le son de debut a deja ete joue
    son_debut_joue = False

def rebondir(x, y):
    '''
    ici on détecte les rebonds
    '''
    if (y < 16 or y > 240) and x > 0 and x < 256: #cas d'un rebond vertical
        return "vertical"
    elif (x >= r1_x and x <= r1_x+11): #cas d'un rebond horizontal à gauche
        if y > (r1_y) and y < (r1_y+32):
            return "horizontal"
    elif (x >= r2_x-2 and x <= r2_x+9): #cas d'un rebond horizontal à droite
        if y > (r2_y) and y < (r2_y+32):
            return "horizontal"
    elif x < 0 or x > 256:
        return "out"
    else:
        return ""

def son_rebond(horizontal):
    '''
    ici on joue du son aux rebonds
    '''
    if horizontal:
        pyxel.sounds[0].set("d1d2", "t", "74", "ff", 5) #son pour un rebond horizontal
        pyxel.play(0, 0)
    else:
        pyxel.sounds[0].set("g1g2", "t", "74", "ff", 5) #son pour un rebond vertical
        pyxel.play(0, 0)

def son_demarrage():
    '''
    ici on joue un son à l'affichage du menu de demarrage
    '''
    pyxel.sounds[0].set("d1 r e2 r e4", "t", "74", "ff", 7)
    pyxel.play(0, 0)

def son_debut():
    '''
    ici on joue un son de debut de partie
    '''
    pyxel.sounds[0].set("d1 r d2 r e3 r e2 r e1", "t", "74", "ff", 7)
    pyxel.play(0, 0)

###################Calculs indispensable au jeu
def calculer():
    '''
    ici on effectue tous les calculs nécessaires au jeu
    '''
    global r1_x, r1_y, r2_x, r2_y, b_x, b_y, dx, dy, score1, score2, gagne1, gagne2, restart, jeu_demarre, son_debut_joue, r1_y_old, r2_y_old, r1_x_old, r2_x_old
    if jeu_demarre:
        #son au debut du jeu
        if son_debut_joue == False:
            son_debut()
            son_debut_joue = True
        #restart si gagne affiche
        if restart:
            pyxel.stop() #arrete le son
            time.sleep(5) #attend 5s
            reset() #redemarre tout
        #gagne
        if score1 == 10 and restart == False: #cas du joueur 1 qui gagne
            gagne1 = True
            restart = True
        elif score2 == 10 and restart == False: #cas du joueur 2 qui gagne
            gagne2 = True
            restart = True
        #deplacer raquette gauche
        if pyxel.btn(pyxel.KEY_Z) and r1_y > 8: #monter
            if r1_y - 5 < 8: #evite que la raquette monte trop haut
                r1_y = 8
            else:
                r1_y -= 5
        if pyxel.btn(pyxel.KEY_S) and r1_y < 216: #descendre
            if r1_y + 5 > 216: #evite que la raquette descende trop bas
                r1_y = 216
            else:
                r1_y += 5
        if pyxel.btn(pyxel.KEY_Q) and r1_x > 12: #aller à gauche
            r1_x -= 5
        if pyxel.btn(pyxel.KEY_D) and r1_x < 110: #aller à droite
            r1_x += 5
        #deplacer raquette droite
        if pyxel.btn(pyxel.KEY_UP) and r2_y > 8: #monter
            if r2_y - 5 < 8: #evite que la raquette monte trop haut
                r2_y = 8
            else:
                r2_y -= 5
        if pyxel.btn(pyxel.KEY_DOWN) and r2_y < 216: #descendre
            if r2_y + 5 > 216: #evite que la raquette descende trop bas
                r2_y = 216
            else:
                r2_y += 5
        if pyxel.btn(pyxel.KEY_LEFT) and r2_x > 142: #aller a gauche
            r2_x -= 5
        if pyxel.btn(pyxel.KEY_RIGHT) and r2_x < 240: #aller a droite
            r2_x += 5
        #deplacement balle
        if gagne1 == False and gagne2 == False: #bouge uniquement si personne n'a gagne
            b_x += dx
            b_y += dy
        #rebond balle
        if rebondir(b_x, b_y) == "vertical": #cas de la balle qui touche une bordure
            son_rebond(False) #son rebond vertical
            dy *= -1
        elif rebondir(b_x, b_y) == "horizontal": #cas de la balle qui touche une raquette
            #supprime les effets x
            if dx > 0:
                dx = 5
            else:
                dx = -5
            if b_x > 0 and b_x < 128 and dx < 0: #pour assurer le bon comportement de la balle
                son_rebond(True) #son rebond horizontal
                b_x = r1_x + 6
                dx *= -1
                #effets
                if r1_y_old != r1_y: #cas du mouvement vertical
                    if r1_y_old > r1_y: #cas de la raquette qui monte
                        if dy > 0: #cas de la balle qui descend
                            dy -= 3
                        else: #cas de la balle qui monte
                            dy -= 3
                    else: #cas de la raquette qui descend
                        if dy > 0: #cas de la balle qui descend
                            dy += 3
                        else: #cas de la balle qui monte
                            dy += 3
                if r1_x_old != r1_x: #cas du mouvement horizontal
                    if r1_x_old < r1_x: #cas de la raquette qui va a droite
                        dx += 3
            elif b_x > 128 and b_x < 256 and dx > 0: #pour assurer le bon comportement de la balle
                son_rebond(True) #son rebond horizontal
                b_x = r2_x - 2
                dx *= -1
                #effets
                if r2_y_old != r2_y: #cas du mouvement vertical
                    if r2_y_old > r2_y: #cas de la raquette qui monte
                        if dy > 0: #cas de la balle qui descend
                            dy -= 3
                        else: #cas de la balle qui monte
                            dy -= 3
                    else: #cas de la raquette qui descend
                        if dy > 0: #cas de la balle qui descend
                            dy += 3
                        else: #cas de la balle qui monte
                            dy += 3
                if r2_x_old != r2_x: #cas du mouvement horizontal
                    if r2_x_old > r2_x: #cas de la raquette qui va a gauche
                        dx -= 3
        elif rebondir(b_x, b_y) == "out" and restart == False and score1 < 10 and score2 < 10: #cas de la balle qui sort
            #place les raquettes aux positions initiales
            r1_x = 12
            r1_y = 108
            r2_x = 240
            r2_y = 108
            if b_x > 128: #cas de la balle a droite
                #place la balle au centre le la raquette gauche
                b_x = r1_x + 5
                b_y = r1_y + 16
                #ajuste les valeurs du deplacement de la balle
                dx = 4
                dy = 4
                score1 += 1 #augmente le score du joueur 1
                pyxel.stop() #arrete le son
                time.sleep(1) #pause d'une seconde
            else: #cas de la balle a gauche
                #place la balle au centre le la raquette droite
                b_x = r2_x - 5
                b_y = r2_y + 16
                #ajuste les valeurs du deplacement de la balle
                dx = -4
                dy = 4
                score2 += 1 #augmente le score du joueur 2
                pyxel.stop() #arrete le son
                time.sleep(1) #pause d'une seconde
        #sauvegarde la position comme ancienne position
        r1_y_old = r1_y
        r2_y_old = r2_y
        r1_x_old = r1_x
        r2_x_old = r2_x
    else:
        #demarrer le jeu
        if pyxel.btn(pyxel.KEY_SPACE):
            jeu_demarre = True

###################Affichage des objets du jeu
def afficher():
    '''
    ici on dessine tous les objets du jeu
    '''
    pyxel.cls(0) #peint le fond en noir pour vider l'écran
    #terrain
    for i in range(10):
        pyxel.rect(126, i*24+14, 4, 12, 10)
    if jeu_demarre: #cas du jeu en cours
        #systeme d'engrenages
        #raquette 1
        #vertical
        pyxel.dither(0.5)
        if r1_y%2 == 0:
            pyxel.blt(5, r1_y+8, 0, 0, 0, 16, 16)
            pyxel.blt(105, r1_y+8, 0, 0, 0, 16, 16)
        else:
            pyxel.blt(5, r1_y+8, 0, 16, 0, 16, 16)
            pyxel.blt(105, r1_y+8, 0, 16, 0, 16, 16)
        pyxel.dither(1)
        #corde
        pyxel.dither(0.1)
        for i1 in range(2): 
            y1 = r1_y+16-i1
            for i2 in range(6):
                if i2%2 == 0:
                    pyxel.rect(13+i2*16+i1, y1, 16, 1, 4)
                else:
                    pyxel.rect(13+i2*16+i1, y1, 16, 1, 9)
                    pyxel.rect(15+i2*16+i1, y1, 12, 1, 4)
        pyxel.dither(1)
        #horizontal
        pyxel.dither(0.5)
        if r1_x%2 == 0:
            pyxel.blt(r1_x-6, 13, 0, 0, 0, 16, 16)
            pyxel.blt(r1_x-6, 227, 0, 0, 0, 16, 16)
        else:
            pyxel.blt(r1_x-6, 13, 0, 16, 0, 16, 16)
            pyxel.blt(r1_x-6, 227, 0, 16, 0, 16, 16)
        pyxel.dither(1)
        #corde
        pyxel.dither(0.1)
        for i1 in range(2): 
            x1 = r1_x+2-i1
            for i2 in range(13):
                if i2%2 == 0:
                    pyxel.rect(x1, 21+i2*16+i1, 1, 16, 4)
                else:
                    pyxel.rect(x1, 21+i2*16+i1, 1, 16, 9)
                    pyxel.rect(x1, 23+i2*16+i1, 1, 12, 4)
        pyxel.dither(1)
        #raquette 2
        #vertical
        pyxel.dither(0.5)
        if r2_y%2 == 0:
            pyxel.blt(235, r2_y+8, 0, 0, 0, 16, 16)
            pyxel.blt(135, r2_y+8, 0, 0, 0, 16, 16)
        else:
            pyxel.blt(235, r2_y+8, 0, 16, 0, 16, 16)
            pyxel.blt(135, r2_y+8, 0, 16, 0, 16, 16)
        pyxel.dither(1)
        #corde
        pyxel.dither(0.1)
        for i1 in range(2): 
            y1 = r2_y+16-i1
            for i2 in range(6):
                if i2%2 == 0:
                    pyxel.rect(143+i2*16+i1, y1, 16, 1, 4)
                else:
                    pyxel.rect(143+i2*16+i1, y1, 16, 1, 9)
                    pyxel.rect(145+i2*16+i1, y1, 12, 1, 4)
        pyxel.dither(1)
        #horizontal
        pyxel.dither(0.5)
        if r2_x%2 == 0:
            pyxel.blt(r2_x-6, 13, 0, 0, 0, 16, 16)
            pyxel.blt(r2_x-6, 227, 0, 0, 0, 16, 16)
        else:
            pyxel.blt(r2_x-6, 13, 0, 16, 0, 16, 16)
            pyxel.blt(r2_x-6, 227, 0, 16, 0, 16, 16)
        pyxel.dither(1)
        #corde
        pyxel.dither(0.1)
        for i1 in range(2): 
            x1 = r2_x+2-i1
            for i2 in range(13):
                if i2%2 == 0:
                    pyxel.rect(x1, 21+i2*16+i1, 1, 16, 4)
                else:
                    pyxel.rect(x1, 21+i2*16+i1, 1, 16, 9)
                    pyxel.rect(x1, 23+i2*16+i1, 1, 12, 4)
        pyxel.dither(1)
        #rectangle bas avec style banniere de chantier
        for i1 in range(8):
            y1 = 255 - i1
            for i2 in range(17):
                if i2%2 == 0:
                    pyxel.rect(-16+i2*16+i1, y1, 16, 1, 7)
                else:
                    pyxel.rect(-16+i2*16+i1, y1, 16, 1, 9)
                    pyxel.rect(-14+i2*16+i1, y1, 12, 1, 10)
        #rectangle haut avec style banniere de chantier
        for i1 in range(8):
            y1 = 8 - i1 - 1
            for i2 in range(17):
                if i2%2 == 0:
                    pyxel.rect(-16+i2*16+i1, y1, 16, 1, 7)
                else:
                    pyxel.rect(-16+i2*16+i1, y1, 16, 1, 9)
                    pyxel.rect(-14+i2*16+i1, y1, 12, 1, 10)
        #raquettes
        pyxel.rect(r1_x, r1_y, 4, 32, 7)
        pyxel.rect(r2_x, r2_y, 4, 32, 7)
        #balle
        pyxel.circ(b_x, b_y, 4, 7)
        #scores
        pyxel.text(118, 16, str(score1), 7)
        pyxel.text(135, 16, str(score2), 7)
        #texte resulats 
        if gagne1 == True:
            pyxel.text(40, 90, "GAGNE,", 7)
            pyxel.text(40, 100, "BRAVO", 7)
            pyxel.text(168, 90, "PERDU,", 7)
            pyxel.text(168, 100, "QUELLE INDIGNITE", 7)
        elif gagne2 == True:
            pyxel.text(40, 90, "PERDU,", 7)
            pyxel.text(40, 100, "QUELLE INDIGNITE", 7)
            pyxel.text(168, 90, "GAGNE,", 7)
            pyxel.text(168, 100, "BRAVO", 7)
    else: #cas du menu de demarrage
        #indication sur le jeu
        pyxel.text(70, 55, "THE BEST PONG EVER, for sure.", 7)
        #indications deplacement player1
        pyxel.text(40, 100, "deplacement :", 7)
        pyxel.text(40, 120, "vertical : Z & S", 7)
        pyxel.text(40, 130, "horizontal : Q & D", 7)
        #indications deplacement player2
        pyxel.text(168, 100, "deplacement :", 7)
        pyxel.text(168, 120, "vertical : ^ & v", 7)
        pyxel.text(168, 130, "horizontal : < & >", 7)
        #indication demarrer partie
        pyxel.text(50, 195, "appuyez sur ESPACE pour demarrer le jeu", 7)
    
##############lancement du programme
pyxel.init(256, 256)
time.sleep(0.1) #pour etre sur que le programme demarre bien avant le son
pyxel.load("ressources.pyxres")

son_demarrage() #son au demarrage du programme
pyxel.run(calculer, afficher)