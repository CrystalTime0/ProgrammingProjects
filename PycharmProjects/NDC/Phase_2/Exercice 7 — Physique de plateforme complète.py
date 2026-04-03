import pyxel
# Consts
VITESSE_DE_DEPLACEMENT = 2.0
VITESS_DE_SAUT = -5.0
GRAVITE = 0.4
GRAVITE_CHUTE = 0.7
GRAVITE_MUR = 0.3
VITESSE_MAX = 8.0

TILE_SIZE = 16
XVI_SOLIDS_TILES = [(0,0), (1,0)]
VIII_SOLIDES_TILES = [(tile[0]*2+decal[0], tile[1]*2+decal[1]) for decal in ((0,0), (1,0), (0,1), (1,1)) for tile in XVI_SOLIDS_TILES]
print(VIII_SOLIDES_TILES)

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.au_sol = False
        self.sur_mur = False
        self.coyote_timer = 0
        self.wall_coyote_timer = 0
        self.wall_jump_timer = 0

    def update(self):
        print(self.wall_coyote_timer)
        # Déplacement Horizontal
        self.vx = 0
        if pyxel.btn(pyxel.KEY_D): self.vx = VITESSE_DE_DEPLACEMENT
        if pyxel.btn(pyxel.KEY_Q): self.vx = -VITESSE_DE_DEPLACEMENT
        if pyxel.btn(pyxel.KEY_D) and pyxel.btn(pyxel.KEY_Q): self.vx = 0

        # Coyote Time
        if self.au_sol:
            self.coyote_timer = 6
        elif self.coyote_timer > 0:
            self.coyote_timer -= 1

        if self.sur_mur:
            self.wall_coyote_timer = 10
        elif self.wall_coyote_timer > 0:
            self.wall_coyote_timer -= 1

        if self.wall_jump_timer > 0:
            self.wall_jump_timer -= 1


        # Saut
        can_jump = (self.au_sol or self.coyote_timer > 0 or self.sur_mur) or (self.wall_jump_timer == 0 or self.wall_coyote_timer)
        print(can_jump)
        if pyxel.btnp(pyxel.KEY_SPACE) and can_jump:
            self.vy = VITESS_DE_SAUT
            self.coyote_timer = 0
            self.wall_jump_timer = 10

        # Correct
        if self.vy > 0 and not self.sur_mur:  # descente = gravité forte
            self.vy += GRAVITE_CHUTE
        elif self.sur_mur:
            self.vy += GRAVITE_MUR
        else:  # montée = gravité douce
            self.vy += GRAVITE

        self.vy = min(self.vy, VITESSE_MAX)

        # Collisions
        self.au_sol = False
        self._deplacer_et_collider(4, 8)

    def draw(self):
        pyxel.rect(self.x, self.y, 4, 8, 4)

    def _is_solid_at(self, px, py):
        if px < 0 or py < 0 or px >= pyxel.width or py >= pyxel.height: return True  # bords = solides
        solid = pyxel.tilemaps[0].pget(px // 8, py // 8) in VIII_SOLIDES_TILES
        return solid

    def _deplacer_et_collider(self, largeur=16, hauteur=16):
        # ── Axe X d'abord ──
        self.x += self.vx
        if self.vx > 0:  # on va à droite : tester le bord droit
            for dy in range(hauteur):  # tester en haut et en bas du personnage
                if self._is_solid_at(int(self.x) + largeur, int(self.y) + dy):
                    self.x = (int(self.x + largeur) // TILE_SIZE) * TILE_SIZE - largeur
                    self.vx = 0
                    if not self.sur_mur:
                        self.vy = 0
                    self.sur_mur = True
                    break
            else:
                self.sur_mur = False

        elif self.vx < 0:  # on va à gauche : tester le bord gauche
            for dy in range(hauteur):
                if self._is_solid_at(int(self.x), int(self.y) + dy):
                    self.x = (int(self.x) // TILE_SIZE + 1) * TILE_SIZE
                    self.vx = 0
                    if not self.sur_mur:
                        self.vy = 0
                    self.sur_mur = True
                    break
            else:
                self.sur_mur = False

        # ── Axe Y ensuite ──
        self.y += self.vy
        if self.vy > 0:  # on tombe : tester le sol
            for dx in [1, largeur - 1]:
                if self._is_solid_at(int(self.x) + dx, int(self.y) + hauteur):
                    self.y = (int(self.y + hauteur) // TILE_SIZE) * TILE_SIZE - hauteur
                    self.vy = 0
                    self.au_sol = True
                    break
        elif self.vy < 0:  # on monte : tester le plafond
            for dx in [1, largeur - 1]:
                if self._is_solid_at(int(self.x) + dx, int(self.y)):
                    self.y = (int(self.y) // TILE_SIZE + 1) * TILE_SIZE
                    self.vy = 0
                    break


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