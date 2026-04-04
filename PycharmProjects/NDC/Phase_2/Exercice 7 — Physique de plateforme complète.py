import pyxel

VITESSE_DE_DEPLACEMENT = 2.0
VITESSE_DE_SAUT        = -4.0
VITESSE_WALL_JUMP_X    = 1.5   # impulsion horizontale au wall jump
GRAVITE                = 0.4
GRAVITE_CHUTE          = 0.5
GRAVITE_MUR            = 0.1   # glisse plus lentement sur le mur
VITESSE_MAX            = 8.0
TILE_SIZE              = 8     # cohérent avec pget(px // 8)

XVI_SOLIDS_TILES = [(0,0), (1,0)]
VIII_SOLIDES_TILES = [
    (tile[0]*2 + d[0], tile[1]*2 + d[1])
    for d in ((0,0),(1,0),(0,1),(1,1))
    for tile in XVI_SOLIDS_TILES
]


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.au_sol          = False
        self.sur_mur         = False
        self.direction_mur   = 0    # +1 = mur à droite, -1 = mur à gauche
        self.coyote_timer    = 0
        self.wall_jump_timer = 0    # bloque l'input pendant l'éjection

    def update(self):
        # ── Input horizontal ──────────────────────────────────
        # Pendant un wall jump, on préserve l'impulsion ; l'input est ignoré
        if self.wall_jump_timer > 0:
            self.wall_jump_timer -= 1
        elif not self.sur_mur:
            self.vx = 0
            if pyxel.btn(pyxel.KEY_D): self.vx =  VITESSE_DE_DEPLACEMENT
            if pyxel.btn(pyxel.KEY_Q): self.vx = -VITESSE_DE_DEPLACEMENT

        # ── Coyote timers ─────────────────────────────────────
        if self.au_sol:
            self.coyote_timer = 6
        elif self.coyote_timer > 0:
            self.coyote_timer -= 1

        # ── Logique de saut ───────────────────────────────────
        # Séparation claire : saut sol vs wall jump
        peut_sauter_sol  = self.au_sol or self.coyote_timer > 0
        peut_wall_jump   = (
            self.sur_mur
            and self.wall_jump_timer == 0
            and not self.au_sol          # évite le wall jump en touchant sol+mur
        )

        if pyxel.btnp(pyxel.KEY_SPACE):
            if peut_sauter_sol:
                self.vy = VITESSE_DE_SAUT
                self.coyote_timer = 0

            elif peut_wall_jump:
                self.vy = VITESSE_DE_SAUT
                # Éjection horizontale opposée au mur
                self.vx = -self.direction_mur * VITESSE_WALL_JUMP_X
                self.wall_jump_timer   = 10   # frames où l'input est gelé

        # ── Gravité ───────────────────────────────────────────
        if self.sur_mur and self.vy > 0:
            self.vy = self.vy * 1.02 + GRAVITE_MUR      # glisse lentement sur le mur
        elif self.vy > 0:
            self.vy += GRAVITE_CHUTE    # chute rapide
        else:
            self.vy += GRAVITE          # montée douce

        self.vy = min(self.vy, VITESSE_MAX)

        # ── Collisions (reset avant) ───────────────────────────
        self.au_sol  = False
        self.sur_mur = False
        self._deplacer_et_collider(4, 8)

    def draw(self):
        pyxel.rect(self.x, self.y, 4, 8, 4)

    def _is_solid_at(self, px, py):
        if px < 0 or py < 0 or px >= pyxel.width or py >= pyxel.height:
            return True
        return pyxel.tilemaps[0].pget(px // TILE_SIZE, py // TILE_SIZE) in VIII_SOLIDES_TILES

    def _deplacer_et_collider(self, largeur=4, hauteur=8):
        # ── Axe X ──
        self.x += self.vx

        if self.vx > 0:                                      # bord droit
            for dy in range(hauteur):
                if self._is_solid_at(int(self.x + largeur), int(self.y) + dy):
                    self.x = (int(self.x + largeur) // TILE_SIZE) * TILE_SIZE - largeur
                    self.vx = 0
                    self.sur_mur = True
                    self.direction_mur = 1   # mur à droite
                    break

        elif self.vx < 0:                                    # bord gauche
            for dy in range(hauteur):
                if self._is_solid_at(int(self.x), int(self.y) + dy):
                    self.x = (int(self.x) // TILE_SIZE + 1) * TILE_SIZE
                    self.vx = 0
                    self.sur_mur = True
                    self.direction_mur = -1  # mur à gauche
                    break

        # ── Axe Y ──
        self.y += self.vy

        if self.vy > 0:                                      # sol
            for dx in [0, largeur - 1]:
                if self._is_solid_at(int(self.x) + dx, int(self.y + hauteur)):
                    self.y = (int(self.y + hauteur) // TILE_SIZE) * TILE_SIZE - hauteur
                    self.vy = 0
                    self.au_sol = True
                    break

        elif self.vy < 0:                                    # plafond
            for dx in [0, largeur - 1]:
                if self._is_solid_at(int(self.x) + dx, int(self.y)):
                    self.y = (int(self.y) // TILE_SIZE + 1) * TILE_SIZE
                    self.vy = 0
                    break
        print(self.sur_mur)


class App:
    def __init__(self):
        pyxel.init(128, 128, "Exercice 7 — Physique de plateforme complète", 30)
        pyxel.load("ress/Ex_8.pyxres")
        # Vars
        self.player = Player(8, 32)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0,0,0,0,0, pyxel.width, pyxel.height)
        self.player.draw()


App()