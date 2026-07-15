from enum import Enum
import pyxel

TILE_SIZE = 8
WORLD_WIDTH = 512
WORLD_HEIGHT = 512
PLAYER_SPEED = 4
MAX_SPEED = 8.0
PLAYER_JUMP_SPEED = -10.0
VITESSE_WALL_JUMP_X    = 3.0
GRAVITE                = 0.8
GRAVITE_CHUTE          = 1.0
GRAVITE_MUR            = 0.2
_SOLIDS = [(0,3), (2,3), (4,3), (6,3), (0,5), (2,5), (4,5), (6,5), (0,7), (2,7)]
SOLIDS = [(x + dx, y + dy) for (x, y) in _SOLIDS for dx in (0, 1) for dy in (0, 1)]

class Debug:
    FLAGS = {
        "collisions":    False,
        "solids":        False,
        "player_info":   False,
        "path":          False,
    }

    @staticmethod
    def enabled(flag):
        return Debug.FLAGS.get(flag, False)

    # ── Fonctions de debug ────────────────────────────────

    @staticmethod
    def draw_solids():
        if not Debug.enabled("solids"): return
        for ty in range(pyxel.height // TILE_SIZE):
            for tx in range(pyxel.width // TILE_SIZE):
                if pyxel.tilemaps[1].pget(tx, ty) in SOLIDS:
                    pyxel.rectb(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE, 8)


    @staticmethod
    def draw_player_info(player):
        if not Debug.enabled("player_info"): return
        pyxel.text(2, 2,  f"x:{player.x:.1f} y:{player.y:.1f}", 7)
        pyxel.text(2, 9,  f"vx:{player.vx:.1f} vy:{player.vy:.1f}", 7)
        pyxel.text(2, 16, f"sol:{player.au_sol} mur:{player.sur_mur}", 7)
        pyxel.text(2, 23, f"coy:{player.coyote_timer} wj:{player.wall_jump_timer}", 7)

    @staticmethod
    def draw_hitbox(entity, color=10):
        if not Debug.enabled("collisions"): return
        pyxel.rectb(int(entity.x), int(entity.y), entity.width, entity.height, color)

    @staticmethod
    def draw_path(path, color=11):
        if not Debug.enabled("path"): return
        for tx, ty in path:
            pyxel.rectb(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE, color)

def is_solid_at(px, py):
    if px < 0 or py < 0 or px >= WORLD_WIDTH or py >= WORLD_HEIGHT: return True
    return pyxel.tilemaps[1].pget(int(px // TILE_SIZE), int(py // TILE_SIZE)) in SOLIDS

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

        if abs(diff_x) > 32:
            self.x += diff_x * coef
        if abs(diff_y) > 32:
            self.y += diff_y * coef

        self.x = max(0.0, min(self.x, float(WORLD_WIDTH) - self.screen_width))
        self.y = max(0.0, min(self.y, float(WORLD_HEIGHT) - self.screen_height))

    def world_to_screen(self, wx, wy):
        return wx - self.x, wy - self.y

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.width = 8
        self.height = 16
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
            if pyxel.btn(pyxel.KEY_D): self.vx +=  PLAYER_SPEED
            if pyxel.btn(pyxel.KEY_Q): self.vx += -PLAYER_SPEED

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
                self.vy = PLAYER_JUMP_SPEED
                self.coyote_timer = 0
            elif peut_wall_jump:
                # ── Calcul de l'impulsion modulée ─────────────────
                input_dir = 0
                if pyxel.btn(pyxel.KEY_D): input_dir = 1
                if pyxel.btn(pyxel.KEY_Q): input_dir = -1

                impulsion = VITESSE_WALL_JUMP_X

                if input_dir == self.direction_mur:
                    impulsion *= 0.5
                    self.vy = PLAYER_JUMP_SPEED*0.8
                else:
                    self.vy = PLAYER_JUMP_SPEED

                self.vx = -self.direction_mur * impulsion
                self.wall_jump_timer = 10

        # ── Gravité ───────────────────────────────────────────
        if self.sur_mur and self.vy > 0:
            self.vy = self.vy * 1.02 + GRAVITE_MUR  # glisse lentement
        elif self.vy > 0:
            self.vy += GRAVITE_CHUTE
        else:
            self.vy += GRAVITE

        self.vy = min(self.vy, MAX_SPEED)

        # ── Collisions ────────────────────────────────────────
        self.au_sol  = False
        self.sur_mur = False
        self._deplacer_et_collider()

        if self.sur_mur and not self.deja_sur_mur and self.vy > 0 and not self. au_sol:
            self.vy = 0

    def draw(self):
        pyxel.blt(self.x,self.y,0,32,56, 8,16,7)

    def _deplacer_et_collider(self):
        self.sur_mur = False

        # ── Axe X ──────────────────────────────────────────────
        self.x += self.vx

        if self.vx > 0:  # Vers la droite
            for dy in range(self.height):
                if is_solid_at(self.x + self.width, self.y + dy):
                    self.x = (int(self.x + self.width) // TILE_SIZE) * TILE_SIZE - self.width
                    self.vx = 0
                    if self.coyote_timer == 0:
                        self.sur_mur = True
                        self.direction_mur = 1
                    break

        elif self.vx < 0:  # Vers la gauche
            for dy in range(self.height):
                if is_solid_at(self.x, self.y + dy):
                    self.x = (int(self.x) // TILE_SIZE + 1) * TILE_SIZE
                    self.vx = 0
                    if self.coyote_timer == 0:
                        self.sur_mur = True
                        self.direction_mur = -1
                    break

        # ── Axe Y ──────────────────────────────────────────────
        self.y += self.vy

        if self.vy > 0:  # Chute
            for dx in range(self.width):
                if is_solid_at(self.x + dx, self.y + self.height):
                    self.y = (int(self.y + self.height) // TILE_SIZE) * TILE_SIZE - self.height
                    self.vy = 0
                    self.au_sol = True
                    break
        elif self.vy < 0:  # Saut
            for dx in range(self.width):
                if is_solid_at(self.x + dx, self.y):
                    self.y = (int(self.y) // TILE_SIZE + 1) * TILE_SIZE
                    self.vy = 0
                    break

        # ── Probe de sécurité (Sticky Wall) ─────────────────────
        if not self.sur_mur and self.coyote_timer == 0 and not self.au_sol:
            # Check Droite
            if any(is_solid_at(self.x + self.width + 1, self.y + dy) for dy in range(self.height)):
                self.sur_mur = True
                self.direction_mur = 1
            elif any(is_solid_at(self.x - 1, self.y + dy) for dy in range(self.height)):
                self.sur_mur = True
                self.direction_mur = -1

class State(Enum):
    MENU = 0
    PLAYING = 1
    PAUSE = 2
    GAMEOVER = 3

class App:
    def __init__(self):
        pyxel.init(256, 256, "Mini-projet A — Platformer à une salle", 30)
        pyxel.load("ress/Mini-Projet_A.pyxres")

        self.state = State.MENU
        self.player = Player(128, 240)
        self.camera = Camera()

        self.menu_items = ["JOUER", "QUITTER"]
        self.menu_index = 0
        self.menu_blink = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        match self.state:
            case State.MENU: self._update_menu()
            case State.PLAYING: self._update_playing()
            case State.PAUSE: self._update_pause()
            case State.GAMEOVER: self._update_gameover()

        # ------------------- DEBUG -------------------
        if pyxel.btnp(pyxel.KEY_F1): Debug.FLAGS["collisions"] ^= True
        if pyxel.btnp(pyxel.KEY_F2): Debug.FLAGS["solids"] ^= True
        if pyxel.btnp(pyxel.KEY_F3): Debug.FLAGS["player_info"] ^= True

    def _update_menu(self):
        self.menu_blink = (self.menu_blink + 1) % 60

        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_Q):
            self.menu_index = (self.menu_index - 1) % len(self.menu_items)

        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.menu_index = (self.menu_index + 1) % len(self.menu_items)

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_index == 0:
                self.state = State.PLAYING
                self.player = Player(128, 240)
                self.camera = Camera()
            elif self.menu_index == 1:
                pyxel.quit()

    def _update_playing(self):
        self.player.update()
        self.camera.follow(self.player.x, self.player.y)

    def _update_pause(self):
        pass

    def _update_gameover(self):
        pass

    def draw(self):
        pyxel.cls(0)
        match self.state:
            case State.MENU: self._draw_menu()
            case State.PLAYING: self._draw_playing()
            case State.PAUSE: self._draw_pause()
            case State.GAMEOVER: self._draw_gameover()

            # ------------------- DEBUG -------------------
        Debug.draw_hitbox(self.player)
        Debug.draw_solids()
        Debug.draw_player_info(self.player)
        

    def _draw_menu(self):
        pyxel.cls(1)

        # Fond décoratif simple
        for y in range(0, pyxel.height, 16):
            for x in range(0, pyxel.width, 16):
                c = 1 if (x // 16 + y // 16) % 2 == 0 else 12
                pyxel.rect(x, y, 16, 16, c)

        # Bandeau titre
        pyxel.rect(0, 0, 256, 52, 5)
        pyxel.rectb(8, 8, 240, 36, 7)

        pyxel.text(54, 20, "PLATFORMER", 7)

        # Petit avatar décoratif
        pyxel.rect(28, 64, 24, 32, 8)
        pyxel.rectb(28, 64, 24, 32, 7)
        pyxel.blt(31, 72, 0, 32, 56, 8, 16, 7)

        # Cadre du menu
        pyxel.rect(64, 72, 128, 104, 0)
        pyxel.rectb(64, 72, 128, 104, 7)

        pyxel.text(100, 82, "MENU", 7)

        start_y = 106
        for i, item in enumerate(self.menu_items):
            y = start_y + i * 20
            selected = i == self.menu_index

            if selected:
                pyxel.rect(76, y - 2, 104, 10, 9 if self.menu_blink < 30 else 8)
                pyxel.text(86, y, ">" + item + "<", 7)
            else:
                pyxel.text(90, y, item, 6)

        # Aide
        pyxel.text(28, 196, "HAUT/BAS : choisir", 7)
        pyxel.text(28, 206, "ESPACE/ENTREE : valider", 7)

        # Footer
        pyxel.line(16, 236, 240, 236, 7)
        pyxel.text(46, 242, "Appuyez sur ESPACE pour commencer", 10)

    def _draw_playing(self):
        pyxel.camera(self.camera.x, self.camera.y)
        pyxel.bltm(0,0,0,0,0, WORLD_WIDTH, WORLD_HEIGHT)
        pyxel.bltm(0,0,1,0,0, WORLD_WIDTH, WORLD_HEIGHT, colkey=0)
        self.player.draw()

    def _draw_pause(self):
        pass

    def _draw_gameover(self):
        pass

App()