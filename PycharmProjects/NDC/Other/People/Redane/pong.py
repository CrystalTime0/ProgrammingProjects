import time

import pyxel

# Global constants
WINDOW_WIDTH: int = 256
WINDOW_HEIGHT: int = 256
PADDLE_WIDTH: int = 4
PADDLE_HEIGHT: int = 32
BALL_RADIUS: int = 4
PADDLE_SPEED: int = 4
BALL_SPEED: int = 4
PADDLE_MARGIN: int = 8
WIN_SCORE: int = 10
MIDDLE_LINE_X: int = 126
MIDDLE_LINE_SEGMENT_HEIGHT: int = 16
MIDDLE_LINE_GAP: int = 8
UI_COLOR: int = 14
BACKGROUND_COLOR: int = 0


# Global game state
left_paddle_x: int = 12
left_paddle_y: int = 108
right_paddle_x: int = 240
right_paddle_y: int = 108
ball_x: int = 20
ball_y: int = 116
ball_velocity_x: int = 4
ball_velocity_y: int = 4
score_left: int = 0
score_right: int = 0


def update() -> None:
    """Update the game logic for the current frame."""
    global left_paddle_x, left_paddle_y, right_paddle_x, right_paddle_y
    global score_left, score_right
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y

    # Player 1 controls
    if pyxel.btn(pyxel.KEY_Z):
        left_paddle_y -= PADDLE_SPEED
    if pyxel.btn(pyxel.KEY_S):
        left_paddle_y += PADDLE_SPEED

    # Player 2 controls
    if pyxel.btn(pyxel.KEY_UP):
        right_paddle_y -= PADDLE_SPEED
    if pyxel.btn(pyxel.KEY_DOWN):
        right_paddle_y += PADDLE_SPEED

    # Keep paddles inside the screen
    left_paddle_y = max(PADDLE_MARGIN, min(left_paddle_y, pyxel.height - PADDLE_HEIGHT - PADDLE_MARGIN))
    right_paddle_y = max(PADDLE_MARGIN, min(right_paddle_y, pyxel.height - PADDLE_HEIGHT - PADDLE_MARGIN))

    # Move the ball
    ball_x -= ball_velocity_x
    ball_y -= ball_velocity_y

    # Bounce on top and bottom walls
    if ball_y <= 10 or ball_y >= 246:
        ball_velocity_y = -ball_velocity_y

    # Bounce on the left paddle
    if (
        left_paddle_y <= ball_y + BALL_RADIUS
        and ball_y - BALL_RADIUS <= left_paddle_y + PADDLE_HEIGHT
        and left_paddle_x + BALL_RADIUS >= ball_x >= left_paddle_x - BALL_RADIUS
    ):
        ball_velocity_x = -ball_velocity_x
        ball_x = left_paddle_x + 6

    # Bounce on the right paddle
    if (
        right_paddle_y <= ball_y + BALL_RADIUS
        and ball_y - BALL_RADIUS <= right_paddle_y + PADDLE_HEIGHT
        and right_paddle_x - BALL_RADIUS <= ball_x <= right_paddle_x + BALL_RADIUS
    ):
        ball_velocity_x = -ball_velocity_x
        ball_x = right_paddle_x - 2

    # Score handling
    if ball_x <= 3:
        time.sleep(1)
        score_right += 1
        ball_x = right_paddle_x - 4
        ball_y = right_paddle_y + 16
        ball_velocity_x = -BALL_SPEED
    elif ball_x >= 253:
        time.sleep(1)
        score_left += 1
        ball_x = left_paddle_x + 8
        ball_y = left_paddle_y + 16
        ball_velocity_x = BALL_SPEED

    # Reset the game when someone wins
    if score_left == WIN_SCORE or score_right == WIN_SCORE:
        pyxel.reset()


def draw() -> None:
    """Draw the game objects on the screen."""
    pyxel.cls(BACKGROUND_COLOR)  # Clear the screen with a black background

    # Top and bottom borders
    pyxel.rect(0, 0, WINDOW_WIDTH, 8, UI_COLOR)
    pyxel.rect(0, 248, WINDOW_WIDTH, 8, UI_COLOR)

    # Center dashed line
    for segment_index in range(11):
        pyxel.rect(
            MIDDLE_LINE_X,
            segment_index * 24,
            4,
            MIDDLE_LINE_SEGMENT_HEIGHT,
            UI_COLOR,
        )

    # Paddles
    pyxel.rect(left_paddle_x, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, UI_COLOR)
    pyxel.rect(right_paddle_x, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, UI_COLOR)

    # Ball
    pyxel.circ(ball_x, ball_y, BALL_RADIUS, UI_COLOR)

    # Scores
    pyxel.text(110, 20, str(score_left), UI_COLOR)
    pyxel.text(140, 20, str(score_right), UI_COLOR)


# Start the game
pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)
pyxel.run(update, draw)