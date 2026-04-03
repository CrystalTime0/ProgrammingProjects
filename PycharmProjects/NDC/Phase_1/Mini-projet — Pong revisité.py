from enum import Enum
import random
import pyxel
# Consts
class State(Enum):
    MENU = 0
    PLAYING = 1
    PAUSE = 2
    SCORED = 3
    GAMEOVER = 4

RACKET_LENGTH = 32
BALL_RADIUS = 5
SPEED = 2.5
TILE_SIZE = 16
SOLIDS = [(2, 0), (2, 1), (3, 0), (3, 1)]
MAX_SPEED = 5.0
SHAKE_STRENGTH = 2
MAX_ANGLE = 45
MIN_ANGLE = 10
X_REBOUND_TOLERANCE = 6
BLINK_FRAMES = 10


class App:
    def __init__(self):
        pyxel.init(128, 128, "Mini-projet — Pong revisité", 30)
        pyxel.load("ress/Mini-projet.pyxres")
        # Class
        self.state = State.MENU

        # Vars
        self.score = [4, 4]
        self.last_score: int | None = None # 0 for p1 and 1 for p2
        self.particles = []
        self.blink = False

        # Timers
        self.UI_timer = 0

        pyxel.playm(0, loop= True)
        pyxel.run(self.update, self.draw)

    def update(self):
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[5] -= 1
        self.particles = [p for p in self.particles if p[5] > 0]

        match self.state:
            case State.MENU: self._update_menu()
            case State.PLAYING: self._update_playing()
            case State.PAUSE: self._update_pause()
            case State.SCORED:
                self._update_scored()
                self.UI_timer += 1
            case State.GAMEOVER:
                self._update_gameover()
                self.gameover_particles_timer += 1
                self.UI_timer += 1

    def _update_menu(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.state = State.PLAYING
            self._init_game()

    def _update_playing(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.state = State.PAUSE

        if pyxel.btn(pyxel.KEY_Z):
            self.p1_y -= SPEED
        if pyxel.btn(pyxel.KEY_S):
            self.p1_y += SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.p2_y -= SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.p2_y += SPEED

        self.p1_y = max(0, min(self.p1_y, pyxel.height - RACKET_LENGTH))
        self.p2_y = max(0, min(self.p2_y, pyxel.height - RACKET_LENGTH))

        self.ball_x += self.ball_x_vel
        self.ball_y += self.ball_y_vel
        if self.ball_x_vel > 0:
            if self.p2_x  < self.ball_x + BALL_RADIUS < self.p2_x + X_REBOUND_TOLERANCE and self.p2_y + RACKET_LENGTH + BALL_RADIUS > self.ball_y > self.p2_y - BALL_RADIUS:
                self._rebond_raquette(self.p2_y, -1)
                self.shake = SHAKE_STRENGTH
                self._spawn_particles(self.ball_x, self.ball_y, [3,11])
                self.last_hit = 1
                pyxel.play(3, 0)
        if self.ball_x_vel < 0:
            if self.p1_x + TILE_SIZE - X_REBOUND_TOLERANCE  < self.ball_x - BALL_RADIUS < self.p1_x + TILE_SIZE  and self.p1_y + RACKET_LENGTH + BALL_RADIUS > self.ball_y > self.p1_y - BALL_RADIUS:
                self._rebond_raquette(self.p1_y, +1)
                self.shake = SHAKE_STRENGTH
                self._spawn_particles(self.ball_x, self.ball_y, [8,9])
                self.last_hit = 0
                pyxel.play(3, 0)


        if self.ball_y - BALL_RADIUS < 0:
            self.ball_y_vel *= -1.05
        if self.ball_y > pyxel.height - BALL_RADIUS:
            self.ball_y_vel *= -1.05

        speed = pyxel.sqrt(self.ball_x_vel ** 2 + self.ball_y_vel ** 2)
        if speed > MAX_SPEED:
            self.ball_x_vel = self.ball_x_vel / speed * MAX_SPEED
            self.ball_y_vel = self.ball_y_vel / speed * MAX_SPEED

        if self.shake > 0:
            pyxel.camera(random.randint(-1, 1) * self.shake, random.randint(-1, 1) * self.shake)
            self.shake -= 1
        else:
            pyxel.camera(0, 0)

        if self.ball_x + BALL_RADIUS > pyxel.width:
            self._score(0)
        elif self.ball_x < 0:
            self._score(1)

    def _update_pause(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.state = State.PLAYING

    def _update_scored(self):
        self.ball_x += self.ball_x_vel
        self.ball_y += self.ball_y_vel

        self.blink = True if self.UI_timer % (2*BLINK_FRAMES) < BLINK_FRAMES else False

        if self.UI_timer >= 90:
            self.state = State.PLAYING
            self._init_game()

    def _update_gameover(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.state = State.PLAYING
            self.score = [0,0]
            self._init_game()

        if self.gameover_particles_timer % 3 == 0 and self.UI_timer <= 30:
            if self.last_hit == 0:
                self._spawn_particles(116, 80, [9, 8, 7], 500, 15)
            if self.last_hit == 1:
                self._spawn_particles(12, 80, [3, 11, 7], 500, 15)

    def draw(self):
        pyxel.cls(0)
        match self.state:
            case State.MENU: self._draw_menu()
            case State.PLAYING: self._draw_playing()
            case State.PAUSE: self._draw_pause()
            case State.SCORED: self._draw_scored()
            case State.GAMEOVER: self._draw_gameover()

    def _draw_menu(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)

        text = "MENU"
        text_x = (pyxel.width - len(text) * 4) // 2
        pyxel.text(text_x, 60, text, 7)

        text = "Press ENTER to start"
        text_x = (pyxel.width - len(text) * 4) // 2
        pyxel.text(text_x, 70, text, 7)

    def _draw_playing(self):
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)

        text = f"{self.score[0]}"
        pyxel.text(15, 22, text, 9)
        text = f"{self.score[1]}"
        pyxel.text(110, 22, text, 11)

        pyxel.blt(0, 64, 0, 0, 144, 24, 32, 2)
        pyxel.blt(104, 64, 0, 32, 144, 24, 32, 2)


        pyxel.blt(self.p1_x, self.p1_y, 0, 32,0, 16, 32, colkey=pyxel.COLOR_BLACK)
        pyxel.blt(self.p2_x, self.p2_y, 0, 48,0, 16, 32, colkey=pyxel.COLOR_BLACK)

        pyxel.blt(self.ball_x-8, self.ball_y-8, 0, 16,self.last_hit*16, 16, 16, colkey=pyxel.COLOR_BLACK)

        for p in self.particles:
            pyxel.pset(int(p[0]), int(p[1]), p[4])

    def _draw_pause(self):
        self._draw_playing()
        for y in range(0, 128, 2):
            pyxel.line(0, y, 128, y, 0)

        text = "PAUSE"
        text_x = (pyxel.width - len(text) * 4) // 2
        pyxel.text(text_x, 60, text, 7)

        text = f"Score : Player 1 : {self.score[0]}, Player 2 : {self.score[1]}"
        pyxel.text(0, 0, text, 7)


    def _draw_gameover(self):
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)

        if self.UI_timer <= 30:
            pyxel.blt(0, 64, 0, 0, 144, 24, 32, 2)
            pyxel.blt(104, 64, 0, 32, 144, 24, 32, 2)
        else:
            if self.last_hit == 0:
                pyxel.blt(0, 64, 0, 0, 144, 24, 32, 2)
            else:
                pyxel.blt(104, 64, 0, 32, 144, 24, 32, 2)

        text = f"PLAYER {self.score.index(max(self.score)) + 1} win"
        text_x = (pyxel.width - len(text) * 4) // 2
        pyxel.text(text_x, 60, text, 7)

        text = "Press R to restart"
        text_x = (pyxel.width - len(text) * 4) // 2
        pyxel.text(text_x, 80, text, 7)

        for p in self.particles:
            pyxel.pset(int(p[0]), int(p[1]), p[4])

    def _draw_scored(self):
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)

        pyxel.blt(0, 64, 0, 0, 144, 24, 32, 2)
        pyxel.blt(104, 64, 0, 32, 144, 24, 32, 2)

        text = f"{self.score[0]}"
        pyxel.text(15, 22, text, 9)
        text = f"{self.score[1]}"
        pyxel.text(110, 22, text, 11)



        if self.blink:
            if self.last_hit == 0:
                pyxel.blt(self.p2_x, self.p2_y, 0, 72, 0, 16, 32, colkey=pyxel.COLOR_BLACK)
                pyxel.blt(self.p1_x, self.p1_y, 0, 32, 0, 16, 32, colkey=pyxel.COLOR_BLACK)
            else:
                pyxel.blt(self.p1_x, self.p1_y, 0, 56, 0, 16, 32, colkey=pyxel.COLOR_BLACK)
                pyxel.blt(self.p2_x, self.p2_y, 0, 48, 0, 16, 32, colkey=pyxel.COLOR_BLACK)
        else:
            pyxel.blt(self.p1_x, self.p1_y, 0, 32, 0, 16, 32, colkey=pyxel.COLOR_BLACK)
            pyxel.blt(self.p2_x, self.p2_y, 0, 48, 0, 16, 32, colkey=pyxel.COLOR_BLACK)

        pyxel.blt(self.ball_x - 8, self.ball_y - 8, 0, 16, self.last_hit * 16, 16, 16, colkey=pyxel.COLOR_BLACK)

    def _rebond_raquette(self, raquette_y, direction_x):
        centre_raquette = raquette_y + RACKET_LENGTH / 2
        relatif = (self.ball_y - centre_raquette) / (RACKET_LENGTH / 2)
        relatif = max(-1.0, min(1.0, relatif))

        angle = relatif * MAX_ANGLE
        angle = max(-MAX_ANGLE, min(MAX_ANGLE, angle))

        if abs(angle) < MIN_ANGLE:
            if self.ball_y_vel >= 0:
                angle = MIN_ANGLE
            else:
                angle = -MIN_ANGLE

        speed = pyxel.sqrt(self.ball_x_vel ** 2 + self.ball_y_vel ** 2)
        speed = min(speed * 1.05, MAX_SPEED)

        self.ball_x_vel = pyxel.cos(angle) * speed * direction_x
        self.ball_y_vel = pyxel.sin(angle) * speed

    def _init_game(self):
        self.shake = 0
        self.p1_x = 16
        self.p1_y = 64

        self.p2_x = 96
        self.p2_y = 64

        self.ball_x = 64
        self.ball_y = 64

        self.ball_x_vel = random.choice([-1, 1]) * random.uniform(0.4, 1.0)
        self.ball_y_vel = random.choice([-1, 1]) * random.uniform(0.3, 1.0)

        self.last_hit = 0 if self.ball_x_vel > 0 else 1


    def _score(self, player):
        self.score[player] += 1
        self.last_score = player
        self.UI_timer = 0

        if max(self.score) >= 5:
            self.gameover_particles_timer = 0
            self.state = State.GAMEOVER
        else:
            self.state = State.SCORED

    def _spawn_particles(self, x, y, color, number= 12, life= 7):
        for _ in range(number):
            angle = random.uniform(0, 360)
            speed = random.uniform(1, 1.5)
            self.particles.append([
                float(x), float(y),
                pyxel.cos(angle) * speed,
                pyxel.sin(angle) * speed,
                random.choice(color),
                life
            ])
App()