import pyxel
# Consts
TILE_SIZE = 8
SOLIDS = [(0, 0), (1, 0), (0, 1)]

class App():
    def __init__(self):
        pyxel.init(128, 128, "Exercice 4 — Tilemap et dessin de niveau", 30)
        pyxel.load("ress/Ex_4.pyxres")

        self.x = 0
        self.y = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        print(self.is_solid(40,80))

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0,0, 0, 0, 0, pyxel.width, pyxel.height, pyxel.COLOR_BLACK)

    def get_tile(self, px, py):
        tx = max(0, min(int(px) // TILE_SIZE, 255))
        ty = max(0, min(int(py) // TILE_SIZE, 255))
        print(tx,ty)
        print(pyxel.tilemaps[0].pget(tx, ty))
        return pyxel.tilemaps[0].pget(tx, ty)

    def is_solid(self, px, py):
        return self.get_tile(px, py) in SOLIDS


App()