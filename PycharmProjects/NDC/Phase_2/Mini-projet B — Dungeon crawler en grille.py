r"""
================================================================================
  ____  _   _ _   _  ____ _____ ___  _   _      _     ______   ______ _____
 |  _ \| | | | \ | |/ ___| ____/ _ \| \ | |    / \   | _) / \ / / ___/ ___|
 | | | | | | |  \| | |  _|  _|| | | |  \| |   / _ \  |  _ \\ V /\___ \___ \
 | |_| | |_| | |\  | |_| | |__| |_| | |\  |  / ___ \ | |_) || |  ___) |__) |
 |____/ \___/|_| \_|\____|_____\___/|_| \_| /_/   \_\|____/ |_| |____/____/

================================================================================

DESCRIPTION:
    A retro top-down Dungeon Crawler based on a strict grid system.
    Players explore a maze rendered via tilemaps, managing visibility
    through a dynamic Fog of War system and interacting with a
    grid-based inventory.

FEATURES:
    * Grid-based movement with smooth interpolation.
    * Dynamic visibility system using line-of-sight (Ray-casting).
    * Smart camera with a dead-zone to prevent jitter.
    * State Management (Menu, Playing, Pause, Inventory, Game Over).
    * Engine: Pyxel (Retro Game Engine for Python).

CONTROLS:
    * ARROW KEYS : Move player / Navigate menus.
    * E          : Open/Close Inventory.
    * P          : Pause game.
    * ENTER      : Confirm selection in menus.

AUTHOR:
    Raphaël Villard (https://github.com/CrystalTime0)
================================================================================
"""

import math
from enum import Enum
from typing import Optional
from collections import deque

import pyxel

type GridPos = tuple[int, int]

WORLD_WIDTH: int = 512
WORLD_HEIGHT: int = 512
TILE_SIZE: int = 8
GRID_TILE_SIZE: int = 16

_SOLIDS: list[tuple[int, int]] = [
    (0, 10), (0, 12), (2, 10), (2, 12), (4, 10), (4, 12), (6, 10), (6, 12),
    (8, 10), (8, 12), (10, 8), (10, 10), (10, 12), (12, 8), (12, 10), (12, 12),
    (14, 8), (14, 10), (14, 12), (16, 8), (16, 10), (16, 12), (18, 10), (18, 12),
    (20, 8), (20, 10), (20, 12), (22, 8), (22, 10), (22, 12), (24, 8), (24, 10),
    (24, 12), (26, 8), (26, 10), (26, 12), (28, 8), (28, 10)
]
SOLIDS: list[tuple[int, int]] = [
    (x + dx, y + dy)
    for (x, y) in _SOLIDS
    for dx in (0, 1)
    for dy in (0, 1)
]


class Utils:
    """
    Utility functions for game mechanics.
    """

    @staticmethod
    def is_solid_at(px: int, py: int) -> bool:
        """Check if a tile is solid (wall) at the given position."""
        # Outside, the map is considered blocked to prevent out-of-bounds movement.
        if px < 0 or py < 0 or px >= WORLD_WIDTH or py >= WORLD_HEIGHT:
            return True
        return pyxel.tilemaps[1].pget(px // TILE_SIZE, py // TILE_SIZE) in SOLIDS

    @staticmethod
    def has_line_of_sight(fx0: int, fy0: int, fx1: int, fy1: int) -> tuple[bool, Optional[tuple[int, int]]]:
        """Check if there is a line of sight between two points."""
        x0, y0 = fx0, fy0
        x1, y1 = fx1, fy1

        dx: int = abs(x1 - x0)
        dy: int = abs(y1 - y0)
        sx: int = 1 if x0 < x1 else -1
        sy: int = 1 if y0 < y1 else -1
        err: int = dx - dy

        while x0 != x1 or y0 != y1:
            e2: int = 2 * err

            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

            # Each fog cell maps to a 2x2 block of 8px tiles.
            # We check all underlying tiles because one visible wall pixel is enough
            # to stop the line of sight.
            is_solid: bool = any(
                pyxel.tilemaps[1].pget(x0 * 2 + ddx, y0 * 2 + ddy) in SOLIDS
                for ddx in range(2)
                for ddy in range(2)
            )
            if is_solid:
                return False, (x0, y0)

        return True, None


class Camera:
    """
    Manages camera movement and coordinate transformations.

    
    :var x: Camera position on the X-axis.
    :var y: Camera position on the Y-axis.
    :var screen_width: Width of the visible screen in pixels.
    :var screen_height: Height of the visible screen in pixels.
    """

    def __init__(self) -> None:
        """ Initialize the camera with the default position and size."""
        self.x: float = 0.0
        self.y: float = 0.0
        self.screen_width: float = float(pyxel.width)
        self.screen_height: float = float(pyxel.height)

    def follow(self, px: int, py: int, coef: float = 0.1) -> None:
        """ Move the camera to follow the given position."""
        target_x: float = float(px - self.screen_width // 2)
        target_y: float = float(py - self.screen_height // 2)

        diff_x: float = target_x - self.x
        diff_y: float = target_y - self.y

        # Small dead-zone to avoid constant camera jitter on tiny movements.
        if abs(diff_x) > 16:
            self.x += diff_x * coef
        if abs(diff_y) > 16:
            self.y += diff_y * coef

        self.x = max(0.0, min(self.x, float(WORLD_WIDTH) - self.screen_width))
        self.y = max(0.0, min(self.y, float(WORLD_HEIGHT) - self.screen_height))

    def world_to_screen(self, wx: float, wy: float) -> tuple[float, float]:
        """ Convert world coordinates to screen coordinates."""
        return wx - self.x, wy - self.y


class FogOfWar:
    """
    Manages and renders a fog of war system for a game.

    The `FogOfWar` class handles updating and drawing a fog of war system where
    different regions of the game world are either unseen, seen, or visible
    based on the player's position. It uses line-of-sight calculations
    and manages the visibility state of grid cells.

    :var cols: Number of columns in the fog grid.
    :var rows: Number of rows in the fog grid.
    :var fog: A 2D list representing the visibility state of each cell in the fog grid.
        Possible states are `UNSEEN`, `SEEN`, and `VISIBLE`.
    """
    UNSEEN: int = 0
    SEEN: int = 1
    VISIBLE: int = 2
    RADIUS: int = 6

    def __init__(self) -> None:
        self.cols: int = WORLD_WIDTH // 16
        self.rows: int = WORLD_HEIGHT // 16
        self.fog: list[list[int]] = [
            [self.UNSEEN for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def _is_surrounded_by_walls(self, x: int, y: int) -> bool:
        """Return True if every neighbour is solid or outside the visible grid."""
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy

                # Treat the border as walls by simply ignoring out-of-range cells.
                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    if not self._is_solid(nx, ny):
                        return False
        return True

    @staticmethod
    def _is_solid(fx: int, fy: int) -> bool:
        """Check whether a fog cell contains at least one solid 8px tile."""
        return any(
            pyxel.tilemaps[1].pget(fx * 2 + ddx, fy * 2 + ddy) in SOLIDS
            for ddx in range(2)
            for ddy in range(2)
        )

    def update(self, player_x: int, player_y: int) -> None:
        """ Update the fog of war based on the player's current position."""
        # First pass: previously visible non-solid cells become SEEN.
        for y in range(self.rows):
            for x in range(self.cols):
                if self.fog[y][x] == self.VISIBLE and not self._is_solid(x, y):
                    self.fog[y][x] = self.SEEN

        px: int = player_x // 16
        py: int = player_y // 16

        # Only check cells inside a circular radius around the player.
        for ty in range(max(0, py - self.RADIUS), min(self.rows, py + self.RADIUS + 1)):
            for tx in range(max(0, px - self.RADIUS), min(self.cols, px + self.RADIUS + 1)):
                if math.sqrt((tx - px) ** 2 + (ty - py) ** 2) <= self.RADIUS:
                    # If walls fully surround a cell, reveal it directly.
                    # This helps keep enclosed spaces visible even with strict LOS.
                    if self._is_surrounded_by_walls(tx, ty):
                        self.fog[ty][tx] = self.VISIBLE

                    visible, wall = Utils.has_line_of_sight(px, py, tx, ty)
                    if visible:
                        self.fog[ty][tx] = self.VISIBLE
                    elif wall:
                        wx, wy = wall
                        if 0 <= wx < self.cols and 0 <= wy < self.rows:
                            # Reveal the blocking wall cell itself.
                            self.fog[wy][wx] = self.VISIBLE

    def draw(self) -> None:
        """ Draw the fog of war to the screen."""

        for ty in range(self.rows):
            for tx in range(self.cols):
                state: int = self.fog[ty][tx]
                if state != self.VISIBLE:
                    x_pos: int = tx * 16
                    y_pos: int = ty * 16

                    if state == self.SEEN:
                        pyxel.blt(x_pos, y_pos, 2, 240, 112, 16, 16, 0)
                    else:
                        pyxel.blt(x_pos, y_pos, 2, 224, 112, 16, 16, 0)


class Inventory:
    """
    Manages an inventory system with item handling, selection, and rendering.

    :var items: List of item IDs currently in the inventory.
    :var selected_item: Tuple representing the currently selected item’s grid position (column, row).
    """
    ITEMS: dict[int, tuple[str, tuple[int, int]]] = {
        1: ("sword", (0, 0)),
        2: ("shield", (16, 0)),
        3: ("axe", (0, 16)),
        4: ("potion", (16, 16)),
    }

    def __init__(self) -> None:
        """ Initialize the inventory without any objects or items."""
        self.items: list[int] = [1, 2, 3, 4, 2, 3]
        self.selected_item: tuple[int, int] = (0, 0)

    def add_item(self, item_id: int) -> None:
        """ Add an item to the inventory if it's not full"""
        if len(self.items) >= 40: return
        self.items.append(item_id)

    def remove_item(self, item_id: int) -> None:
        """ Remove an item from the inventory if it exists"""
        self.items.remove(item_id)

    def has_item(self, item_id: int) -> bool:
        """ Check if an item is currently in the inventory"""
        return item_id in self.items

    def get_item_name(self, item_id: int) -> str:
        """ Get the name of an item based on its ID"""
        return self.ITEMS[item_id][0]

    def update(self) -> None:
        """ Update the inventory state based on user input."""
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.selected_item = (self.selected_item[0] + 1, self.selected_item[1])
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.selected_item = (self.selected_item[0] - 1, self.selected_item[1])
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_item = (self.selected_item[0], self.selected_item[1] - 1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_item = (self.selected_item[0], self.selected_item[1] + 1)

        self.selected_item = (self.selected_item[0] % 8, self.selected_item[1] % 5)

    def draw(self) -> None:
        """ Draw the inventory to the screen."""
        pyxel.rect(48, 64, 160, 128, 6)

        pyxel.rectb(52, 68, 152, 16, 12)
        pyxel.rect(54, 70, 148, 12, 5)
        texte = "INVENTORY"
        x = (pyxel.width - len(texte) * 4) // 2
        pyxel.text(x, 74, texte, 7)

        pyxel.rect(52, 88, 152, 100, 12)

        for i in range(5):
            for j in range(8):
                pyxel.rect(57 + j * 18, 92 + i * 19, 16, 16, 5)
                item = None

                if i * 8 + j < len(self.items):
                    item = self.ITEMS[self.items[i * 8 + j]]
                    pyxel.blt(57 + j * 18, 92 + i * 19, 2, item[1][0], item[1][1], 16, 16, 0)

                if (j, i) == self.selected_item:
                    pyxel.rectb(57 + j * 18, 92 + i * 19, 16, 16, 7)
                    if item:
                        pyxel.text(48, 52, item[0], 7)

#---------------------------------------------------------------#
#                           ENEMIES                             #
#---------------------------------------------------------------#

class Enemy:
    """
    Represents an enemy entity within a game context.

    This class encapsulates the properties and behaviours of an enemy. It is used
    to define the characteristics of various enemy types, including their
    location on a grid, movement speed, and categorization.

    :var x: The x-coordinate of the enemy's position.
    :var y: The y-coordinate of the enemy's position.
    :var speed: The movement speed of the enemy. frame per move
    :var type_name: The type or category of the enemy.
    """
    def __init__(self, x: int, y: int, type_name: str, player: Player) -> None:
        self.x: int = x
        self.y: int = y
        self.type_name: str = type_name
        self.player: Player = player
        self.path: list[GridPos] | None = []
        self.direction: tuple[int, int] = (1,0)
        self.move_timer: int = 0

    def bfs(self, target: GridPos) -> list[GridPos] | None:
        """
        Performs a breadth-first search (BFS) to find the shortest path between the
        current position and a specified target in a grid-based world. This method
        returns the path as a list of grid positions, excluding the starting position.

        :param target: The target grid position to which the path will be found.
        :return: A list of grid positions representing the shortest path to the target.
            If the target is unreachable or the start and target positions are the same,
            an empty list is returned.
        """
        start: GridPos = (self.x // TILE_SIZE, self.y // TILE_SIZE)

        if start == target: return []

        frontier = deque([start])
        came_from: dict[GridPos, GridPos | None] = {start: None}

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while frontier:
            current: GridPos = frontier.popleft()

            if current == target:
                path: list[GridPos] = []
                temp_curr: GridPos | None = current
                while temp_curr is not None:
                    path.append(temp_curr)
                    temp_curr = came_from[temp_curr]
                path.reverse()
                return path[1:]

            for dx, dy in directions:
                neighbor: GridPos = (current[0] + dx, current[1] + dy)

                # Check if the neighbour is within the world bounds and not already visited
                if (0 <= neighbor[0] < WORLD_WIDTH // TILE_SIZE and
                        0 <= neighbor[1] < WORLD_HEIGHT // TILE_SIZE and
                        neighbor not in came_from):

                    # Check if the neighbour is solid
                    if not Utils.is_solid_at(neighbor[0] * TILE_SIZE, neighbor[1] * TILE_SIZE):
                        came_from[neighbor] = current
                        frontier.append(neighbor)
        return []


class Troll(Enemy):
    SPEED = 30

    def __init__(self, x: int, y: int, player: Player) -> None:
        super().__init__(x, y, type_name="troll", player= player)
        self.path_timer: int = 0

    def update(self):
        self.path_timer -= 1

        if not self.path or self.path_timer <= 0:
            self.path = self.bfs((self.player.x // TILE_SIZE, self.player.y // TILE_SIZE))
            self.path_timer = 30

        if self.path:
            start_x = self.x
            start_y = self.y

            # Tuile cible en pixels
            target_x = self.path[0][0] * GRID_TILE_SIZE
            target_y = self.path[0][1] * GRID_TILE_SIZE

            dx = target_x - start_x
            dy = target_y - start_y

            if (pyxel.sgn(dx), pyxel.sgn(dy)) != (0, 0):
                self.direction = (int(pyxel.sgn(dx)), int(pyxel.sgn(dy)))

            if self.move_timer > 0:
                self.move_timer -= 1

                # Interpolate between start and destination so movement feels smooth
                # even though gameplay logic is grid-based.
                t: float = 1.0 - (self.move_timer / self.SPEED)
                self.x = int(start_x + (target_x - start_x) * t)
                self.y = int(start_y + (target_y - start_y) * t)
            else:
                self.path.pop(0)
                self.move_timer = self.SPEED

    def draw(self):
        u: int = 0
        match self.direction:
            case (0, -1):
                u = 96
            case (0, 1):
                u = 64
            case (-1, 0):
                u = 32
            case (1, 0):
                u = 0

        # Alternate between two frames while moving to create a walk animation.
        frame: int = (
            u + 16
            if (self.move_timer > 0 and (self.move_timer % self.SPEED) >= self.SPEED // 2)
            else u
        )
        pyxel.blt(self.y, self.x, 2, frame, 160, GRID_TILE_SIZE, GRID_TILE_SIZE, 8)


class Player:
    """
    Represents a player character in a grid-based 2D game with smooth movement
    and animation.

    This class is responsible for managing the player's position, movement, and
    animation. The position is updated based on user input, and movement across
    the grid appears smooth through interpolation. The class also handles
    collision detection to ensure valid movement inside the game.

    :var x: The player's logical x-coordinate on the grid.
    :var y: The player's logical y-coordinate on the grid.
    :var render_x: The player's interpolated x-coordinate for smooth rendering of movement.
    :var render_y: The player's interpolated y-coordinate for smooth rendering of movement.
    :var start_x: The player's starting x-coordinate at the beginning of the current movement animation.
    :var start_y: The player's starting y-coordinate at the beginning of the current movement animation.
    :var vx: The horizontal velocity of the player, used for determining the movement direction.
    :var vy: The vertical velocity of the player, used for determining the movement direction.
    :var width: The width of the player's sprite.
    :var height: The height of the player's sprite.
    :var move_timer: A counter for tracking the remaining time for the current movement animation.
    :var move_duration: The duration of the movement animation, controlling its speed.
    :var direction: A tuple representing the player's current movement direction as (x, y).
    :var fog_of_war: Instance of FogOfWar used to manage visibility and obscured areas of the game map.
    """

    def __init__(self, fog_of_war: FogOfWar) -> None:
        """ Initialize the player at the start of the game."""
        self.x: int = 0  # Logical grid position.
        self.y: int = 16

        self.render_x: int = 0  # Interpolated drawing position.
        self.render_y: int = 0

        self.start_x: int = 0  # Start of the current movement animation.
        self.start_y: int = 0

        self.vx: int = 0
        self.vy: int = 0
        self.width: int = 16
        self.height: int = 16
        self.move_timer: int = 0
        self.move_duration: int = 16
        self.direction: tuple[int, int] = (0, 1)

        self.fog_of_war = fog_of_war
        self.fog_of_war.update(self.x, self.y)

    def update(self) -> None:
        """ Update the player's position based on user input and movement logic."""
        self.vx = 0
        self.vy = 0

        if self.move_timer == 0:
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.vx = -GRID_TILE_SIZE
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.vx = GRID_TILE_SIZE
            elif pyxel.btnp(pyxel.KEY_UP):
                self.vy = -GRID_TILE_SIZE
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.vy = GRID_TILE_SIZE

            self.move_and_collide()

        if self.move_timer > 0:
            self.move_timer -= 1

            # Interpolate between start and destination so movement feels smooth
            # even though gameplay logic is grid-based.
            t: float = 1.0 - (self.move_timer / self.move_duration)
            self.render_x = int(self.start_x + (self.x - self.start_x) * t)
            self.render_y = int(self.start_y + (self.y - self.start_y) * t)
        else:
            self.render_x = self.x
            self.render_y = self.y

    def draw(self) -> None:
        """ Draw the player's sprite at its interpolated position."""
        u: int = 0
        match self.direction:
            case (0, -1):
                u = 96
            case (0, 1):
                u = 64
            case (-1, 0):
                u = 32
            case (1, 0):
                u = 0

        # Alternate between two frames while moving to create a walk animation.
        frame: int = (
            u + 16
            if (self.move_timer > 0 and (self.move_timer % self.move_duration) >= self.move_duration // 2)
            else u
        )
        pyxel.blt(self.render_x, self.render_y, 2, frame, 112, self.width, self.height, 2)

    def move_and_collide(self) -> None:
        """ Move the player in the direction specified by their velocity, handling collisions."""
        self.start_x = self.x
        self.start_y = self.y

        # Move on X, then revert if the target tile is blocked.
        self.x += self.vx
        if Utils.is_solid_at(self.x, self.y):
            self.x -= self.vx

        # Move on Y, then revert if the target tile is blocked.
        self.y += self.vy
        if Utils.is_solid_at(self.x, self.y):
            self.y -= self.vy

        if (pyxel.sgn(self.vx), pyxel.sgn(self.vy)) != (0, 0):
            self.direction = (int(pyxel.sgn(self.vx)), int(pyxel.sgn(self.vy)))

        if self.x != self.start_x or self.y != self.start_y:
            self.move_timer = self.move_duration
            self.fog_of_war.update(self.x, self.y)


class State(Enum):
    """ Enum representing the different game states."""
    MENU = 0
    PLAYING = 1
    PAUSE = 2
    INVENTORY = 3
    GAMEOVER = 4


class App:
    """
    Manages the dungeon crawler game application, including menu, gameplay, pause,
    inventory, and gameover states.

    This class initializes the main game loop, updates the game state, and handles
    the rendering of the game based on the current state.

    :var state: Represents the current state of the game, such as MENU, PLAYING, PAUSE, INVENTORY, or GAMEOVER.
    :var player: Player instance representing the player's character and its behaviour.
    :var inventory: Inventory instance representing the player's inventory.
    :var fog_of_war: FogOfWar instance is used to manage visibility and obscured areas of the game map.
    :var camera: Camera instance used to follow the player and determine the viewport in the game world.
    :var menu_selected_item: Index of the currently selected menu item in the main menu.
    :var pause_selected_item: Index of the currently selected menu item in the pause menu.
    """

    def __init__(self) -> None:
        """ Initialize the game state and start the main game loop."""
        pyxel.init(256, 256, "Mini-projet B — Dungeon crawler en grille", 30)
        pyxel.load("ress/Mini-Projet_B.pyxres")
        self.state = State.MENU
        self.fog_of_war = FogOfWar()
        self.player = Player(self.fog_of_war)
        self.inventory = Inventory()
        self.camera = Camera()

        self.enemies: list[Enemy] = [Troll(16, 16, self.player)]

        self.menu_selected_item: int = 0
        self.pause_selected_item: int = 0

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """ Update the game state based on user input and game state."""
        match self.state:
            case State.MENU:
                self._update_menu()
            case State.PLAYING:
                self._update_playing()
            case State.PAUSE:
                self._update_pause()
            case State.INVENTORY:
                self._update_inventory()
            case State.GAMEOVER:
                self._update_gameover()

    def _update_menu(self) -> None:
        """ Update the menu state based on user input and menu logic."""
        if pyxel.btnp(pyxel.KEY_RETURN):
            match self.menu_selected_item:
                case 0:
                    self.state = State.PLAYING
                case 1:
                    pyxel.quit()

        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_selected_item = (self.menu_selected_item - 1) % 2
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_selected_item = (self.menu_selected_item + 1) % 2

    def _update_playing(self) -> None:
        """ Update the playing state based on user input and game logic."""
        # Update fog before movement so visibility is always based on the current frame state.
        #self.fog_of_war.update(self.player.x, self.player.y)
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        self.camera.follow(self.player.render_x, self.player.render_y)

        if pyxel.btnp(pyxel.KEY_E):
            self.state = State.INVENTORY
        if pyxel.btnp(pyxel.KEY_P):
            self.state = State.PAUSE

    def _update_pause(self) -> None:
        """ Update the pause state based on user input and pause logic."""
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

    def _update_inventory(self) -> None:
        """ Update the inventory state based on user input and inventory logic."""
        self.inventory.update()

        if pyxel.btnp(pyxel.KEY_E):
            self.state = State.PLAYING

    def _update_gameover(self) -> None:
        """ Update the gameover state based on user input and game over logic."""
        pass

    def draw(self) -> None:
        """ Render the current game state to the screen."""
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)

        match self.state:
            case State.MENU:
                self._draw_menu()
            case State.PLAYING:
                self._draw_playing()
            case State.PAUSE:
                self._draw_pause()
            case State.INVENTORY:
                self._draw_inventory()
            case State.GAMEOVER:
                self._draw_gameover()

    def _draw_menu(self) -> None:
        """ Draw the main menu to the screen."""
        pyxel.blt(0, 0, 0, 0, 0, pyxel.width, pyxel.height)
        couleur: int = 7 if (pyxel.frame_count // 15) % 2 == 0 else 12

        pyxel.text(90 if self.menu_selected_item == 0 else 98,
                   140,
                   "> FALL INTO ABYSS" if self.menu_selected_item == 0 else "FALL INTO ABYSS",
                   couleur if self.menu_selected_item == 0 else 7)

        pyxel.text(
            104 if self.menu_selected_item == 1 else 112,
            160,
            "> RUN AWAY" if self.menu_selected_item == 1 else "RUN AWAY",
            couleur if self.menu_selected_item == 1 else 7
        )

    def _draw_playing(self) -> None:
        """ Draw the playing state to the screen."""
        # Pyxel camera shifts the whole world drawing space.
        pyxel.camera(int(self.camera.x), int(self.camera.y))

        pyxel.bltm(0, 0, 0, 0, 0, WORLD_WIDTH, WORLD_HEIGHT)
        pyxel.bltm(0, 0, 1, 0, 0, WORLD_WIDTH, WORLD_HEIGHT, colkey=8)

        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()
        self.fog_of_war.draw()

    def _draw_pause(self) -> None:
        """ Draw the pause menu to the screen."""
        self._draw_playing()
        # Darken the screen with lines to add depths to the paused state.
        for y in range(0, pyxel.height, 2):
            pyxel.line(0, y, WORLD_WIDTH, y, 0)

        pyxel.blt(0, 0, 1, 0, 0, pyxel.width, pyxel.height, 0)

        pyxel.blt(156, 100, 2, 0, 32, 64, 16, 0)
        pyxel.blt(156, 140, 2, 0, 48, 40, 16, 0)

        blink_u: int = 48 if (pyxel.frame_count // 15) % 2 == 0 else 40

        if self.pause_selected_item == 0:
            pyxel.blt(140, 100, 2, blink_u, 48, 8, 16, 0)
        elif self.pause_selected_item == 1:
            pyxel.blt(140, 140, 2, blink_u, 48, 8, 16, 0)

    def _draw_inventory(self) -> None:
        """ Draw the inventory menu to the screen."""
        self._draw_playing()

        pyxel.camera(self.camera.x, self.camera.y)

        # Add a checker overlay over the world to make the inventory screen feel modal.
        for i in range(pyxel.height):
            for j in range(pyxel.width):
                if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                    pyxel.pset(j, i, 0)

        self.inventory.draw()

    def _draw_gameover(self) -> None:
        """ Draw the gameover menu to the screen."""
        pass


App()