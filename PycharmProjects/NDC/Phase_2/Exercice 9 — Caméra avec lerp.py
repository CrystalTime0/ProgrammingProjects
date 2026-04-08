import pyxel

PLAYER_SPEED = 2
WORLD_WIDTH = 256
WORLD_HEIGHT = 256

class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.screen_width = float(pyxel.width)
        self.screen_height = float(pyxel.height)

    def follow(self, px, py, coef=0.1):
        target_x = float(px - self.screen_width // 2)
        target_y = float(py - self.screen_height // 2)

        diff_x = target_x - self.x
        diff_y = target_y - self.y

        if abs(diff_x) > 5:
            self.x += diff_x * coef
        if abs(diff_y) > 5:
            self.y += diff_y * coef

        self.x = max(0.0, min(self.x, float(WORLD_WIDTH) - self.screen_width))
        self.y = max(0.0, min(self.y, float(WORLD_HEIGHT) - self.screen_height))

    def world_to_screen(self, wx, wy):
        return wx - self.x, wy - self.y

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 4
        self.height = 8

    def update(self):
        if pyxel.btn(pyxel.KEY_Q): self.x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_D): self.x += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_Z): self.y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_S): self.y += PLAYER_SPEED

        self.x = max(0, min(WORLD_WIDTH - self.width, self.x))
        self.y = max(0, min(WORLD_HEIGHT - self.height, self.y))

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 8)

class App:
    def __init__(self):
        pyxel.init(128, 128, "Exercice 9 — Caméra avec lerp", 30)
        pyxel.load("ress/Ex_9.pyxres")
        self.world_width = 256
        self.world_height = 256
        self.player = Player()
        self.camera = Camera()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.camera.follow(self.player.x, self.player.y, coef=0.1)

    def draw(self):
        pyxel.cls(0)
        pyxel.camera(int(self.camera.x), int(self.camera.y))

        pyxel.bltm(0, 0, 0, 0, 0, self.world_width, self.world_height)


        self.player.draw()

App()