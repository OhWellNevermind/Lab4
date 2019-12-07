from tkinter import *
import random

WIDTH = 500
HEIGHT = 500
PAD_W = 5
PAD_H = 100
PAD_SPEED = 20
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0
ball_speed_up = 1.05
ball_max_speed = 40
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
BALL_RADIUS = 30
INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

right_line_distance = WIDTH - PAD_W


def create_canvas(root):
    return Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")


def create_text1(c):
    return c.create_text(WIDTH - WIDTH / 6, PAD_H / 4,
                         text=0,
                         font="Arial 20",
                         fill="white")


def create_text2(c):
    return c.create_text(WIDTH / 6, PAD_H / 4,
                         text=0,
                         font="Arial 20",
                         fill="white")


def create_ball(c):
    return c.create_oval(-70, -70, -100, -100, fill="white")


def update_score(c):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if c == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(player_1(c), text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(player_2(c), text=PLAYER_2_SCORE)


def move_ball(c, ball, coord):
    ball_left, ball_top, ball_right, ball_bot = c.coords(ball)
    c.move(ball, coord[2] - ball_right, coord[1] - ball_top)
    ball_center = (ball_top + ball_bot) / 2

    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(ball, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH / 2:
            if c.coords(create_right_pad(c))[1] < ball_center < c.coords(create_right_pad(c))[3]:
                bounce("strike")
            else:
                update_score("left")
                spawn_ball(c)
        else:
            if c.coords(create_left_pad(c))[1] < ball_center < c.coords(create_left_pad(c))[3]:
                bounce("strike")
            else:
                update_score("right")
                spawn_ball(c)
    else:
        if ball_right > WIDTH / 2:
            c.move(ball, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(ball, -ball_left + PAD_W, BALL_Y_SPEED)
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")



def create_left_pad(c):
    return c.create_line(PAD_W / 2, 0, PAD_W / 2, PAD_H, width=PAD_W, fill="yellow")


def create_right_pad(c):
    return c.create_line(WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2, PAD_H, width=PAD_W, fill="yellow")


def create_line_left(c):
    return c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")


def create_line_right(c):
    return c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")


def create_line_center(c):
    return c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")


def move_pads(c, pads):
    for pad in pads:

        c.move(pad, 0, pads[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])


def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < ball_max_speed:
            BALL_X_SPEED *= -ball_speed_up
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED


def player_1(c):
    return c.create_text(WIDTH - WIDTH / 6, PAD_H / 4,
                         text=PLAYER_1_SCORE,
                         font="Arial 20",
                         fill="white")


def player_2(c):
    return c.create_text(WIDTH / 6, PAD_H / 4,
                         text=PLAYER_2_SCORE,
                         font="Arial 20",
                         fill="white")


def spawn_ball(c):
    global BALL_X_SPEED
    c.coords(create_ball(c), WIDTH / 2 - BALL_RADIUS / 2,
             HEIGHT / 2 - BALL_RADIUS / 2,
             WIDTH / 2 + BALL_RADIUS / 2,
             HEIGHT / 2 + BALL_RADIUS / 2),
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)
