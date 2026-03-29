import pyxel
import time
# Consts

class App:
    def __init__(self):
        pyxel.init(128, 128, "Exercice 5 — Son et musique", 30)
        pyxel.load("ress/Ex_5.pyxres")
        pyxel.playm(0, loop= True)

        pyxel.run(self.update, self.draw)

    def update(self):
        time.sleep(1)
        if False:
            pyxel.play(1, 0)
        if False:
            pyxel.play(3, 2)
        if True:
            pyxel.stop(0)
            pyxel.play(0, 1)
            time.sleep(2)

    def draw(self):
        pyxel.cls(0)

App()