import pyxel
# Consts
TAILLE: int = 16
VITESSE: int = 2
DIRECTION_COLOR = {
    "right": pyxel.COLOR_RED,
    "left": pyxel.COLOR_LIGHT_BLUE,
    "up": pyxel.COLOR_YELLOW,
    "down": pyxel.COLOR_GREEN,
}

class App:
    def __init__(self):
        pyxel.init(128, 128, "Exercice 1 : Carré mobile et gestion des inputs", 30)
        # Vars
        self.x: int = 0
        self.y: int = 0
        self.direction: str = "right"

        pyxel.run(self.update, self.draw)

    def update(self):
        # Keys
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += VITESSE
            self.direction = "right"
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= VITESSE
            self.direction = "left"
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= VITESSE
            self.direction = "up"
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += VITESSE
            self.direction = "down"

        self.x = max(0, min(self.x, pyxel.width - TAILLE))
        self.y = max(0, min(self.y, pyxel.height - TAILLE))

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, self.y, TAILLE, TAILLE, DIRECTION_COLOR[self.direction])

App()