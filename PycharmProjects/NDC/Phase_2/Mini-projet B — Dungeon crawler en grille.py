import pyxel
from enum import Enum
import math

WORLD_WIDTH = 512
WORLD_HEIGHT = 512
TILE_SIZE = 8
GRID_TILE_SIZE = 16
_SOLIDS = [(0,10),(0,12),(2,10),(2,12),(4,10),(4,12),(6,10),(6,12),(8,10),(8,12), (10,8),(10,10),(10,12),(12,8),(12,10),(12,12),(14,8),(14,10),(14,12),(16,8),(16,10),(16,12),(18,10),(18,12),(20,8),(20,10),(20,12),(22,8),(22,10),(22,12),(24,8),(24,10),(24,12),(26,8),(26,10),(26,12),(28,8),(28,10)]
SOLIDS = [(x + dx, y + dy) for (x, y) in _SOLIDS for dx in (0, 1) for dy in (0, 1)]

class Utils:

    @staticmethod
    def is_solid_at(px, py):
        if px < 0 or py < 0 or px >= WORLD_WIDTH or py >= WORLD_HEIGHT: return True
        return pyxel.tilemaps[1].pget(px // TILE_SIZE, py // TILE_SIZE) in SOLIDS

    @staticmethod
    def has_line_of_sight(fx0, fy0, fx1, fy1):
        """
        Bresenham entièrement en fog-grid (tuiles 16px).
        Retourne (True, None) si LOS libre.
        Retourne (False, (wx, wy)) si un mur bloque — le mur est marqué visible.
        """
        x0, y0 = fx0, fy0
        x1, y1 = fx1, fy1

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while x0 != x1 or y0 != y1:
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

            # Chaque tuile fog (16px) couvre 4 tuiles 8px → on vérifie les 4
            is_solid = any(
                pyxel.tilemaps[1].pget(x0 * 2 + ddx, y0 * 2 + ddy) in SOLIDS
                for ddx in range(2) for ddy in range(2)
            )
            if is_solid:
                return False, (x0, y0)

        return True, None

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

        if abs(diff_x) > 16:
            self.x += diff_x * coef
        if abs(diff_y) > 16:
            self.y += diff_y * coef

        self.x = max(0.0, min(self.x, float(WORLD_WIDTH) - self.screen_width))
        self.y = max(0.0, min(self.y, float(WORLD_HEIGHT) - self.screen_height))

    def world_to_screen(self, wx, wy):
        return wx - self.x, wy - self.y

class FogOfWar:
    UNSEEN, SEEN, VISIBLE = 0, 1, 2
    RADIUS = 6

    def __init__(self):
        self.cols = WORLD_WIDTH // 16
        self.rows = WORLD_HEIGHT // 16
        self.fog = [[self.UNSEEN for _ in range(self.cols)] for _ in range(self.rows)]

    def _is_surrounded_by_walls(self, x, y):
        """Vérifie si une tuile est entourée uniquement de solides."""
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue

                nx, ny = x + dx, y + dy
                # Si on dépasse les bords, on considère que c'est un mur
                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    if not self._is_solid(nx, ny):
                        return False  # Il y a du vide à côté, donc c'est une façade
        return True

    @staticmethod
    def _is_solid(fx, fy):
        """Vérifie si la tuile fog contient au moins une tuile 8px solide."""
        return any(
            pyxel.tilemaps[1].pget(fx * 2 + ddx, fy * 2 + ddy) in SOLIDS
            for ddx in range(2) for ddy in range(2)
        )

    def update(self, player_x, player_y):
        # VISIBLE → SEEN uniquement pour les tuiles NON solides
        for y in range(self.rows):
            for x in range(self.cols):
                if self.fog[y][x] == self.VISIBLE and not self._is_solid(x, y):
                    self.fog[y][x] = self.SEEN

        px, py = player_x // 16, player_y // 16

        for ty in range(max(0, py - self.RADIUS), min(self.rows, py + self.RADIUS + 1)):
            for tx in range(max(0, px - self.RADIUS), min(self.cols, px + self.RADIUS + 1)):
                if math.sqrt((tx - px) ** 2 + (ty - py) ** 2) <= self.RADIUS:
                    if self._is_surrounded_by_walls(tx, ty):
                        self.fog[ty][tx] = self.VISIBLE

                    visible, wall = Utils.has_line_of_sight(px, py, tx, ty)
                    if visible:
                        self.fog[ty][tx] = self.VISIBLE
                    elif wall:
                        wx, wy = wall
                        if 0 <= wx < self.cols and 0 <= wy < self.rows:
                            self.fog[wy][wx] = self.VISIBLE  # Le mur est visible

    def draw(self):
        for ty in range(self.rows):
            for tx in range(self.cols):
                state = self.fog[ty][tx]
                if state != self.VISIBLE:
                    x_pos, y_pos = tx * 16, ty * 16
                    for y in range(y_pos, y_pos + 16, 2):
                        for x in range(x_pos, x_pos + 16, 2):
                            is_checker_a = ((x // 2) + (y // 2)) % 2 == 0
                            if is_checker_a:
                                pyxel.rect(x, y, 2, 2, 13)
                            else:
                                if state == self.UNSEEN:
                                    pyxel.rect(x, y, 2, 2, 5)

class Inventory:

    ITEMS = {
        1: ("sword", (0,0)),
        2: ("shield", (16,0)),
        3: ("axe", (0,16)),
        4: ("potion", (16,16)),
    }

    def __init__(self):
        self.items = [1,2,3,4,2,3]
        self.selected_item = (0, 0)

    def add_item(self, item_id):
        if len(self.items) >= 40: return
        self.items.append(item_id)

    def remove_item(self, item_id):
        self.items.remove(item_id)

    def has_item(self, item_id):
        return item_id in self.items

    def get_item_name(self, item_id):
        return self.ITEMS[item_id][0]

    def update(self):
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.selected_item = (self.selected_item[0] + 1, self.selected_item[1])
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.selected_item = (self.selected_item[0] - 1, self.selected_item[1])
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_item = (self.selected_item[0], self.selected_item[1] - 1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_item = (self.selected_item[0], self.selected_item[1] + 1)

        self.selected_item = (self.selected_item[0] % 8, self.selected_item[1] % 5)

    def draw(self):
        pyxel.rect(48, 64, 160, 128, 6)

        pyxel.rectb(52, 68, 152, 16, 12)
        pyxel.rect(54, 70, 148, 12, 5)
        texte = "INVENTORY"
        x = (pyxel.width - len(texte) * 4) // 2
        pyxel.text(x, 74, texte, 7)

        pyxel.rect(52, 88, 152, 100, 12)

        for i in range(5):
            for j in range(8):
                pyxel.rect(57 + j*18, 92 + i*19, 16,16, 5)
                item = None

                if i*8+j < len(self.items):
                    item = self.ITEMS[self.items[i * 8 + j]]
                    pyxel.blt(57 + j * 18, 92 + i * 19, 2, item[1][0], item[1][1], 16, 16, 0)

                if (j, i) == self.selected_item:
                    pyxel.rectb(57 + j * 18, 92 + i * 19, 16, 16, 7)
                    if item:
                        pyxel.text(48, 52, item[0], 7)


class Player:
    def __init__(self):
        self.x = 0           # position logique (grille)
        self.y = 16
        self.render_x = 0    # position visuelle (interpolée)colkey
        self.render_y = 0
        self.start_x = 0     # point de départ du glissement
        self.start_y = 0
        self.vx = 0
        self.vy = 0
        self.width = 16
        self.height = 16
        self.move_timer = 0
        self.move_duration = 12
        self.direction = (0, 1)

    def update(self):
        self.vx = 0
        self.vy = 0

        if self.move_timer == 0:
            if pyxel.btnp(pyxel.KEY_LEFT):   self.vx = -GRID_TILE_SIZE
            elif pyxel.btnp(pyxel.KEY_RIGHT): self.vx =  GRID_TILE_SIZE
            elif pyxel.btnp(pyxel.KEY_UP):    self.vy = -GRID_TILE_SIZE
            elif pyxel.btnp(pyxel.KEY_DOWN):  self.vy =  GRID_TILE_SIZE
            self.move_and_collide()

        if self.move_timer > 0:
            self.move_timer -= 1
            t = 1.0 - (self.move_timer / self.move_duration)
            self.render_x = int(self.start_x + (self.x - self.start_x) * t)
            self.render_y = int(self.start_y + (self.y - self.start_y) * t)
        else:
            self.render_x = self.x
            self.render_y = self.y

    def draw(self):
        u = 0
        match self.direction:
            case (0, -1): u = 96
            case (0, 1):  u = 64
            case (-1, 0): u = 32
            case (1, 0):  u = 0

        frame = (u + 16) if (self.move_timer > 0 and (self.move_timer % self.move_duration) >= self.move_duration // 2) else u
        pyxel.blt(self.render_x, self.render_y, 2, frame, 112, self.width, self.height, 2)

    def move_and_collide(self):
        self.start_x = self.x
        self.start_y = self.y

        self.x += self.vx
        if Utils.is_solid_at(self.x, self.y):
            self.x -= self.vx

        self.y += self.vy
        if Utils.is_solid_at(self.x, self.y):
            self.y -= self.vy

        if (pyxel.sgn(self.vx), pyxel.sgn(self.vy)) != (0, 0):
            self.direction = (pyxel.sgn(self.vx), pyxel.sgn(self.vy))

        if self.x != self.start_x or self.y != self.start_y:
            self.move_timer = self.move_duration


class State(Enum):
    MENU = 0
    PLAYING = 1
    PAUSE = 2
    INVENTORY = 3
    GAMEOVER = 4

class App:
    def __init__(self):
        pyxel.init(256, 256, "Mini-projet B — Dungeon crawler en grille", 30)
        pyxel.load("ress/Mini-Projet_B.pyxres")
        self.state = State.MENU
        self.player = Player()
        self.inventory = Inventory()
        self.fog_of_war = FogOfWar()
        self.camera = Camera()

        self.menu_selected_item = 0
        self.pause_selected_item = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        match self.state:
            case State.MENU : self._update_menu()
            case State.PLAYING : self._update_playing()
            case State.PAUSE : self._update_pause()
            case State.INVENTORY: self._update_inventory()
            case State.GAMEOVER : self._update_gameover()

    def _update_menu(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            match self.menu_selected_item:
                case 0: self.state = State.PLAYING
                case 1: pyxel.quit()

        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_selected_item = (self.menu_selected_item - 1) % 2
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_selected_item = (self.menu_selected_item + 1) % 2


    def _update_playing(self):
        self.fog_of_war.update(self.player.x, self.player.y)
        self.player.update()
        self.camera.follow(self.player.x, self.player.y)

        if pyxel.btnp(pyxel.KEY_E):
            self.state = State.INVENTORY
        if pyxel.btnp(pyxel.KEY_P):
            self.state = State.PAUSE

    def _update_pause(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            match self.pause_selected_item:
                case 0:
                    self.state = State.PLAYING
                case 1:
                    pyxel.quit()

        if pyxel.btnp(pyxel.KEY_UP):
            self.pause_selected_item = (self.pause_selected_item - 1) % 2
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.pause_selected_item = (self.pause_selected_item + 1) % 2

    def _update_inventory(self):
        self.inventory.update()

        if pyxel.btnp(pyxel.KEY_E):
            self.state = State.PLAYING

    def _update_gameover(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)

        match self.state:
            case State.MENU: self._draw_menu()
            case State.PLAYING: self._draw_playing()
            case State.PAUSE: self._draw_pause()
            case State.INVENTORY: self._draw_inventory()
            case State.GAMEOVER: self._draw_gameover()

    def _draw_menu(self):
        pyxel.blt(0,0,0,0,0,pyxel.width,pyxel.height)
        couleur = 7 if (pyxel.frame_count // 15) % 2 == 0 else 12

        pyxel.text(90 if self.menu_selected_item == 0 else 98,
                   140,
                   "> FALL INTO ABYSS" if self.menu_selected_item == 0 else "FALL INTO ABYSS",
                   couleur if self.menu_selected_item == 0 else 7)

        pyxel.text(104 if self.menu_selected_item == 1 else 112,
                160,
                "> RUN AWAY" if self.menu_selected_item == 1 else "RUN AWAY",
                couleur if self.menu_selected_item == 1 else 7)

    def _draw_playing(self):
        pyxel.camera(int(self.camera.x), int(self.camera.y))

        pyxel.bltm(0, 0, 0, 0, 0, WORLD_WIDTH, WORLD_HEIGHT)
        pyxel.bltm(0, 0, 1, 0, 0, WORLD_WIDTH, WORLD_HEIGHT, colkey=8)


        self.player.draw()

        self.fog_of_war.draw()

    def _draw_pause(self):
        self._draw_playing()

        for y in range(0, pyxel.height, 2):
            pyxel.line(0, y, WORLD_WIDTH, y, 0)

        pyxel.blt(0,0,1,0,0,pyxel.width,pyxel.height, 0)

        pyxel.blt(156,100,2, 0, 32, 64, 16, 0)
        pyxel.blt(156, 140, 2, 0, 48, 40, 16, 0)

        blink_u = 48 if (pyxel.frame_count // 15) % 2 == 0 else 40

        if self.pause_selected_item == 0:
            pyxel.blt(140,100,2,blink_u, 48, 8, 16, 0)
        elif self.pause_selected_item == 1:
            pyxel.blt(140,140,2,blink_u, 48, 8, 16, 0)

    def _draw_inventory(self):
        self._draw_playing()

        for i in range(pyxel.height):
            for j in range(pyxel.width):
                if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                    pyxel.pset(j, i, 0)

        self.inventory.draw()

    def _draw_gameover(self):
        pass

App()