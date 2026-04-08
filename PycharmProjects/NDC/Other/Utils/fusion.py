import pyxel

# On initialise pyxel
pyxel.init(256, 256)
pyxel.load("../../Phase_2/ress/Mini-Projet_B.pyxres")

# 1. On charge le menu dans la banque 0
pyxel.image(0).load(0, 0, "Main_Door_Final.png")

# 2. On charge la pause dans la banque 1
pyxel.image(1).load(0, 0, "Pause_Menu_Final.png")

# 4. On sauvegarde TOUT dans le même fichier
pyxel.save("../../Phase_2/ress/Mini-Projet_B.pyxres")

print("Fusion terminée ! Utilise uniquement Mini-Projet_B.pyxres maintenant.")