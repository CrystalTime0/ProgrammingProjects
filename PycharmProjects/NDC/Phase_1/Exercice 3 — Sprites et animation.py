import pyxel
# Consts
ANIMATION_LINE = {
    "player": 0
}

class App():
    def __init__(self):
        pyxel.init(128,128, "Exercice 3 — Sprites et animation", 30)
        pyxel.load("ress/Ex_3.pyxres")
        # Vars
        self.frame = 0
        self.x: int = 0
        self.y: int = 0
        self.player_anim_frame = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frame += 1
        if self.frame % 8 == 0:
            self.player_anim_frame = (self.player_anim_frame + 1) % 2


    def draw(self):
        pyxel.cls(0)
        src_x = 16 * self.player_anim_frame
        pyxel.blt(self.x, self.y, 0, u= src_x, v= ANIMATION_LINE["player"], w= 16, h= 16, colkey=pyxel.COLOR_DARK_BLUE)

App()