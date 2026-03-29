from enum import Enum
from unittest import case

import pyxel
# Consts

# Utils
class State(Enum):
    MENU = 0
    PLAYING = 1
    PAUSE = 2
    GAMEOVER = 3

class App:
    def __init__(self):
        pyxel.init(128, 128, "Exercice 6 — Machine à états (State Machine)", 30)
        # Vars
        self.state = State.MENU

        pyxel.run(self.update, self.draw)

    def update(self):
        match self.state:
            case State.MENU: self._update_menu()
            case State.PLAYING: self._update_playing()
            case State.PAUSE: self._update_pause()
            case State.GAMEOVER: self._update_gameover()

    def _update_menu(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.state = State.PLAYING
            self._init_game()

    def _update_playing(self):
        if pyxel.btn(pyxel.KEY_P):
            self.state = State.PAUSE
        if pyxel.btn(pyxel.KEY_Q):
            self.state = State.GAMEOVER

    def _update_pause(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.state = State.PLAYING

    def _update_gameover(self):
        pass

    def draw(self):
        pyxel.cls(0)
        match self.state:
            case State.MENU:
                self._draw_menu()
            case State.PLAYING:
                self._draw_playing()
            case State.PAUSE:
                self._draw_pause()
            case State.GAMEOVER:
                self._draw_gameover()

    def _draw_menu(self):
        pyxel.cls(2)
        texte = "MENU"
        x = (pyxel.width - len(texte) * 4) // 2
        pyxel.text(x, 60, texte, 7)
        texte = "Press ENTER to Play"
        x = (pyxel.width - len(texte) * 4) // 2
        pyxel.text(x, 80, texte, 7)

    def _draw_playing(self):
        pyxel.cls(8)

    def _draw_pause(self):
        pyxel.cls(12)

    def _draw_gameover(self):
        pyxel.cls(0)
        texte = "GAME OVER"
        x = (pyxel.width - len(texte) * 4) // 2
        pyxel.text(x, 60, texte, 7)

    def _init_game(self):
        pass

App()