import pyxel

# On initialise pyxel sans fenêtre juste pour le traitement
pyxel.init(256, 256, display_scale=1)

# 1. On charge ton PNG externe dans la banque 0
pyxel.image(0).load(0, 0, "Main_Door_Final.png")

# 2. On sauvegarde l'état actuel de Pyxel dans le fichier final
pyxel.save("../../Phase_2/ress/Mini-Projet_B.pyxres")

print("Fichier assets.pyxres créé avec succès !")