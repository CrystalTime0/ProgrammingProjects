import pyxel
# Consts
RAYON: int = 8
GRAVITY: float = 0.2

class App:
    def __init__(self):
        pyxel.init(128, 128, "Exercice 2 — Balle rebondissante", 30)
        # Vars
        self.x: float = RAYON
        self.y: float = RAYON
        self.x_vel: float = 4
        self.y_vel: float = 2
        self.rebounds: int = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        print(self.x, self.y, f"{self.x_vel:.2f}", self.y_vel)
        self.x += self.x_vel
        self.y += self.y_vel

        if self.x < RAYON:
            self.x = RAYON
            self.x_vel *= -1
        if self.x + RAYON > pyxel.width:
            self.x = pyxel.width - RAYON
            self.x_vel *= -1
        if self.y < RAYON:
            self.y = RAYON
            self.y_vel *= -1
        if self.y + RAYON > pyxel.height:
            self.y = pyxel.height - RAYON
            self.y_vel *= -0.5
            self.x_vel *= 0.7
            if -10**-2 < self.x_vel < 10**-2:
                self.x_vel = 0


        self.y_vel += GRAVITY

    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.x, self.y, RAYON, pyxel.COLOR_WHITE)

App()