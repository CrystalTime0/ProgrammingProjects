import pyxel


class Projectile:
    def __init__(self):
        self.actif = False
        self.x = self.y = 0.0
        self.vx =  self.vy = 0.0

class ProjectilesSystem:

    POOL_SIZE = 30
    COOLDOWN = 20

    def __init__(self):
        self.pool = [Projectile() for _ in range(self.POOL_SIZE)]
        self.timer_cooldown = 0

    def shoot(self, x, y, vx, vy):
        if self.timer_cooldown > 0: return
        for p in self.pool:
            if not p.actif:
                p.actif = True
                p.x, p.y = float(x), float(y)
                p.vx, p.vy = float(vx), float(vy)
                self.timer_cooldown = self.COOLDOWN
                return

    def update(self):
        self.timer_cooldown -= 1
        for p in self.pool:
            if not p.actif: continue
            p.x += p.vx
            p.y += p.vy
            if p.x < 0 or p.x > pyxel.width or p.y < 0 or p.y > pyxel.height:
                p.actif = False

    def draw(self):
        for p in self.pool:
            if not p.actif: continue
            pyxel.circ(p.x, p.y, 2, pyxel.COLOR_WHITE)

class App():
    def __init__(self):
        pyxel.init(128, 128, "Exercice 10 — Système de projectiles avec pool", 30)

        self.ProjectilesSystem = ProjectilesSystem()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.ProjectilesSystem.update()
        if pyxel.btn(pyxel.KEY_Q):
            self.ProjectilesSystem.shoot(64, 64, 2, 1)

    def draw(self):
        pyxel.cls(0)
        self.ProjectilesSystem.draw()

App()