import pyxel
from collections import deque

PLAYER_SPEED = 2
ENEMY_SPEED = 1

TILE_SIZE = 8
SOLIDS = [(1, 0)]
WORLD_WIDTH = 256
WORLD_HEIGHT = 256


def is_solid_at(px, py, ignore_boarder=False):
    if not ignore_boarder and (px < 0 or py < 0 or px >= WORLD_WIDTH or py >= WORLD_HEIGHT): return True
    x, y = px // TILE_SIZE, py // TILE_SIZE
    return pyxel.tilemaps[0].pget(x, y) in SOLIDS

def bfs(start, target):
    if start == target: return []
    frontier = deque([start])
    came_from = {start: None}
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # haut, bas, gauche, droite

    while frontier:
        current = frontier.popleft()
        if current == target:
            # Reconstruire le chemin
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path[1:]  # [1:] = exclure la position actuelle
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            print(neighbor)
            if 0 <= nx < WORLD_WIDTH // TILE_SIZE and 0 <= ny < WORLD_HEIGHT // TILE_SIZE and neighbor not in came_from:
                print(is_solid_at(nx, ny))
                if not is_solid_at(nx * TILE_SIZE, ny * TILE_SIZE):
                    came_from[neighbor] = current
                    frontier.append(neighbor)
    return []

class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.screen_width = float(pyxel.width)
        self.screen_height = float(pyxel.height)

    def follow(self, px, py) -> None:
        self.x = px - pyxel.width // 2
        self.y = py - pyxel.height // 2

        self.x = max(0, min(self.x, WORLD_WIDTH - self.screen_width))
        self.y = max(0, min(self.y, WORLD_HEIGHT - self.screen_height))

    def world_to_screen(self, wx, wy):
        return wx - self.x, wy - self.y

class Enemy:
    def __init__(self, x, y, width, height, player):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.player = player
        self.path = []
        self.speed = 1.0
        self.vx = 0.0
        self.vy = 0.0
        self.path_timer = 0

    def update(self):
        self.path_timer -= 1

        if not self.path or self.path_timer <= 0:
            self.path = bfs(
                (int(self.x) // TILE_SIZE, int(self.y) // TILE_SIZE),
                (self.player.x // TILE_SIZE, self.player.y // TILE_SIZE)
            )
            self.path_timer = 30

        if self.path:
            # Tuile cible en pixels
            target_x = self.path[0][0] * TILE_SIZE
            target_y = self.path[0][1] * TILE_SIZE

            dx = target_x - self.x
            dy = target_y - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist <= ENEMY_SPEED:
                # Tuile atteinte → tuile suivante
                self.x, self.y = float(target_x), float(target_y)
                self.path.pop(0)
            else:
                # Avancer vers la tuile
                self.x += (dx / dist) * ENEMY_SPEED
                self.y += (dy / dist) * ENEMY_SPEED

    def draw(self):
        pyxel.rect(int(self.x), int(self.y), self.width, self.height, 0)



class Player:
    def __init__(self):
        self.x = 32
        self.y = 88
        self.vx = 0
        self.vy = 0
        self.width = 8
        self.height = 8

    def update(self):
        self.vx = 0
        self.vy = 0

        if pyxel.btn(pyxel.KEY_Q):
            self.vx = -PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_D):
            self.vx = PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_Z):
            self.vy = -PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_S):
            self.vy = PLAYER_SPEED

        self._move_and_collide()

    def _move_and_collide(self):
        self.x += self.vx
        if self.vx > 0: # right
            for dy in range(self.height):
                if is_solid_at(self.x + self.width, self.y + dy):
                    self.x = (int(self.x + self.width) // TILE_SIZE) * TILE_SIZE - self.width
                    self.vx = 0
                    break

        elif self.vx < 0: # left
            for dy in range(self.height):
                if is_solid_at(self.x, self.y + dy):
                    self.x = (int(self.x) // TILE_SIZE + 1) * TILE_SIZE
                    self.vx = 0
                    break

        self.y += self.vy
        if self.vy > 0: # down
            for dx in range(self.width):
                if is_solid_at(self.x + dx, self.y + self.height):
                    self.y = (int(self.y + self.height) // TILE_SIZE) * TILE_SIZE - self.height
                    self.vy = 0
                    break

        elif self.vy < 0: # up
            for dx in range(self.width):
                if is_solid_at(self.x + dx, self.y):
                    self.y = (int(self.y) // TILE_SIZE + 1) * TILE_SIZE
                    self.vy = 0
                    break



    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 8)

class App:
    def __init__(self):
        pyxel.init(128, 128, "Exercice 11 — Pathfinding BFS pour les ennemis", 30)
        pyxel.load("ress/Ex_11.pyxres")

        self.player = Player()
        self.camera = Camera()
        self.enemy = Enemy(96, 96, TILE_SIZE, TILE_SIZE, self.player)

        pyxel.run(self.update, self.draw)
    def update(self):
        self.player.update()
        self.enemy.update()
        self.camera.follow(self.player.x + self.player.width // 2, self.player.y +  self.player.height // 2)

    def draw(self):
        pyxel.cls(0)

        pyxel.camera(int(self.camera.x), int(self.camera.y))

        pyxel.bltm(0, 0, 0, 0, 0, WORLD_WIDTH, WORLD_HEIGHT)
        self.player.draw()
        self.enemy.draw()

App()