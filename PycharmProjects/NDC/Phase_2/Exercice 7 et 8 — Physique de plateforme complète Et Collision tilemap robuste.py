import pyxel

VITESSE_DE_DEPLACEMENT = 2.0
VITESSE_DE_SAUT        = -4.0
VITESSE_WALL_JUMP_X    = 1.5
GRAVITE                = 0.4
GRAVITE_CHUTE          = 0.5
GRAVITE_MUR            = 0.1
VITESSE_MAX            = 8.0
TILE_SIZE              = 8

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
        self.direction_mur   = 0
        self.deja_sur_mur    = False
        self.coyote_timer    = 0
        self.wall_jump_timer = 0

    def update(self):
        self.deja_sur_mur = self.sur_mur

        if self.wall_jump_timer > 0:
            self.wall_jump_timer -= 1
        elif self.sur_mur and not self.au_sol:
            self.vx = 0
        else:
            self.vx = 0
            if pyxel.btn(pyxel.KEY_D): self.vx =  VITESSE_DE_DEPLACEMENT
            if pyxel.btn(pyxel.KEY_Q): self.vx = -VITESSE_DE_DEPLACEMENT

        # ── Coyote timer ──────────────────────────────────────
        if self.au_sol:
            self.coyote_timer = 6
        elif self.coyote_timer > 0:
            self.coyote_timer -= 1

        # ── Logique de saut ───────────────────────────────────
        peut_sauter_sol = self.au_sol or self.coyote_timer > 0
        peut_wall_jump  = (
            self.sur_mur
            and self.wall_jump_timer == 0
            and not self.au_sol
        )

        if pyxel.btnp(pyxel.KEY_SPACE):
            if peut_sauter_sol:
                self.vy = VITESSE_DE_SAUT
                self.coyote_timer = 0
            elif peut_wall_jump:
                # ── Calcul de l'impulsion modulée ─────────────────
                input_dir = 0
                if pyxel.btn(pyxel.KEY_D): input_dir = 1
                if pyxel.btn(pyxel.KEY_Q): input_dir = -1

                impulsion = VITESSE_WALL_JUMP_X

                if input_dir == self.direction_mur:
                    impulsion *= 0.5
                    self.vy = VITESSE_DE_SAUT*0.8
                else:
                    self.vy = VITESSE_DE_SAUT

                self.vx = -self.direction_mur * impulsion
                self.wall_jump_timer = 10

        # ── Gravité ───────────────────────────────────────────
        if self.sur_mur and self.vy > 0:
            self.vy = self.vy * 1.02 + GRAVITE_MUR  # glisse lentement
        elif self.vy > 0:
            self.vy += GRAVITE_CHUTE
        else:
            self.vy += GRAVITE

        self.vy = min(self.vy, VITESSE_MAX)

        # ── Collisions ────────────────────────────────────────
        self.au_sol  = False
        self.sur_mur = False
        self._deplacer_et_collider(4, 8)

        if self.sur_mur and not self.deja_sur_mur and self.vy > 0 and not self. au_sol:
            self.vy = 0

    def draw(self):
        pyxel.rect(self.x, self.y, 4, 8, 8)

    def _is_solid_at(self, px, py):
        if px < 0 or py < 0 or px >= pyxel.width or py >= pyxel.height:
            return True
        return pyxel.tilemaps[0].pget(px // TILE_SIZE, py // TILE_SIZE) in VIII_SOLIDES_TILES

    def _deplacer_et_collider(self, largeur=4, hauteur=8):
        self.sur_mur = False

        # ── Axe X ──────────────────────────────────────────────
        self.x += self.vx

        if self.vx > 0:  # Vers la droite
            for dy in range(hauteur):
                for py in [self.y, self.y + hauteur - 1]:
                    if self._is_solid_at(self.x + largeur, py):
                        self.x = (int(self.x + largeur) // TILE_SIZE) * TILE_SIZE - largeur
                        self.vx = 0
                        if self.coyote_timer == 0:
                            self.sur_mur = True
                            self.direction_mur = 1
                        break

        elif self.vx < 0:  # Vers la gauche
            for py in [self.y, self.y + hauteur - 1]:
                if self._is_solid_at(self.x, py):
                    self.x = (int(self.x) // TILE_SIZE + 1) * TILE_SIZE
                    self.vx = 0
                    if self.coyote_timer == 0:
                        self.sur_mur = True
                        self.direction_mur = -1
                    break

        # ── Axe Y ──────────────────────────────────────────────
        self.y += self.vy

        if self.vy > 0:  # Chute
            for dx in [0, largeur - 0.1]: # Marge pour éviter bugs
                if self._is_solid_at(self.x + dx, self.y + hauteur):
                    self.y = (int(self.y + hauteur) // TILE_SIZE) * TILE_SIZE - hauteur
                    self.vy = 0
                    self.au_sol = True
                    break
        elif self.vy < 0:  # Saut
            for dx in [0, largeur - 0.1]: # Marge pour éviter bugs
                if self._is_solid_at(self.x + dx, self.y):
                    self.y = (int(self.y) // TILE_SIZE + 1) * TILE_SIZE
                    self.vy = 0
                    break

        # ── Probe de sécurité (Sticky Wall) ─────────────────────
        if not self.sur_mur and self.coyote_timer == 0 and not self.au_sol:
            # Check Droite
            if any(self._is_solid_at(self.x + largeur + 0.1, self.y + dy) for dy in [0, hauteur - 1]):
                self.sur_mur = True
                self.direction_mur = 1
            # Check Gauche
            elif any(self._is_solid_at(self.x - 0.1, self.y + dy) for dy in [0, hauteur - 1]):
                self.sur_mur = True
                self.direction_mur = -1


class App:
    def __init__(self):
        pyxel.init(128, 128, "Exercice 7 — Physique de plateforme complète", 30)
        pyxel.load("ress/Ex_7_8.pyxres")
        self.player = Player(8, 32)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)
        self.player.draw()


App()