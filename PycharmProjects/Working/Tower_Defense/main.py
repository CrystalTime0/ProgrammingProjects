import pyxel
from enum import Enum
import random

TILE_SIZE = 8

class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.angle = angle

    def move(self):
        self.x += self.vx
        self.y += self.vy

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 10
        self.damage = 10
        self.attack_speed = 100
        self.last_shot_time = 0

    def draw(self):
        pyxel.circ(self.x, self.y, 4, 8)

    def update(self):
        pass

    def shoot(self, x, y):
        if pyxel.frame_count - self.last_shot_time > self.attack_speed:
            self.last_shot_time = pyxel.frame_count
            angle = pyxel.atan2(y - self.y, x - self.x)
            return Projectile(self.x, self.y, angle)
        return None

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LevelManager:
    def __init__(self):
        self.level = 0
        self.towers = []
        self.enemies = []

    def handle_click(self, x, y):
        if pyxel.tilemaps[0].pget(x//TILE_SIZE,y//TILE_SIZE) in ((1,7),(1,8),(2,7),(2,8),(5,7),(5,8),(6,7),(6,8)):
            if (x, y) in [(tower.x, tower.y) for tower in self.towers]:
                return
            self.towers.append(Tower(x//TILE_SIZE*TILE_SIZE,y//TILE_SIZE*TILE_SIZE))

    def draw(self):
        pyxel.bltm(0,0,0,self.level*pyxel.width, 0, pyxel.width, pyxel.height)

        for tower in self.towers:
            tower.draw()

    def update(self):
        for tower in self.towers:
            tower.update()

class Debug:
    def __init__(self):
        self.flags = {49 : False # GRID
                      }

    def toggle(self, key):
        if key in self.flags:
            self.flags[key] = not self.flags[key]
        else:
            print("unknown debug_key")

    def update_debug(self):
        pass

    def draw_debug(self):
        if self.flags[49]:
            self.debug_grid()

    @staticmethod
    def debug_grid():
        for i in range(0,256,TILE_SIZE):
            for j in range(0,256,TILE_SIZE):
                pyxel.pset(i,j,7)


class State(Enum):
    MENU = 0
    PLAYING = 1
    PAUSE = 2
    GAMEOVER = 3

class App:
    def __init__(self):
        pyxel.init(256, 256, "Tower_Defense", 30)
        pyxel.load("asset.pyxres")
        pyxel.mouse(True)
        self.state = State.PLAYING
        self.debug = Debug()
        self.level_manager = LevelManager()

        pyxel.run(self.update, self.draw)

    def update(self):
        for key in pyxel.input_keys:
            if key in list(range(pyxel.KEY_0,pyxel.KEY_9)):
                self.debug.toggle(key)

        match self.state:
            case State.MENU:
                self.update_menu()
            case State.PLAYING:
                self.update_playing()
            case State.PAUSE:
                self.update_pause()
            case State.GAMEOVER:
                self.update_gameover()

        self.debug.update_debug()

    def update_menu(self):
        pass

    def update_playing(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.level_manager.handle_click(pyxel.mouse_x, pyxel.mouse_y)

    def update_pause(self):
        pass

    def update_gameover(self):
        pass

    def draw(self):
        pyxel.cls(0)
        match self.state:
            case State.MENU:
                self.draw_menu()
            case State.PLAYING:
                self.draw_playing()
            case State.PAUSE:
                self.draw_pause()
            case State.GAMEOVER:
                self.draw_gameover()

        self.debug.draw_debug()

    def draw_menu(self):
        pass

    def draw_playing(self):
        self.level_manager.draw()

    def draw_pause(self):
        pass

    def draw_gameover(self):
        pass


App()