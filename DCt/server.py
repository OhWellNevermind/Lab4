import json
import socket, random, threading
import time

host = '192.168.1.10'
port = 9090

clients = []

WIDTH = 500
HEIGHT = 500
PAD_W = 1
PAD_H = 100

ball_speed_up = 0
ball_max_speed = 40
BALL_RADIUS = 15

INITIAL_SPEED = 30
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
quit = False

COORD = [WIDTH / 2 - BALL_RADIUS / 2,
                     HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2,
                     HEIGHT / 2 + BALL_RADIUS / 2]


def check_contact(data, ball_center):
    try:
        pad_coords = json.loads(data)
        if pad_coords[1] < ball_center < pad_coords[3]:
            return True
    except:
        pass
    return False


print('Server started')


direction_x = direction_y = 1
while not quit:
    try:
        data, addr = s.recvfrom(1024)

        if addr not in clients and len(clients) < 3:
            clients.append(addr)

        if len(clients) == 3:
            current_client = 0

            client_coord = list(COORD)
            ball_left, ball_top, ball_right, ball_bot = client_coord
            ball_center = (ball_top + ball_bot) / 2

            if COORD[0] - PAD_W <= 0:
                if check_contact(data, ball_center) == False:
                    print("Right win")
                direction_x = 1
            elif COORD[0] + BALL_X_SPEED > (WIDTH * 3):
                if check_contact(data, ball_center) == False:
                    print("Left win")
                direction_x = -1

            if COORD[1] + BALL_Y_SPEED < BALL_RADIUS or COORD[3] + BALL_Y_SPEED > HEIGHT:
                direction_y *= -1

            if direction_x == 1:
                if COORD[0] < WIDTH:
                    current_client = 0
                elif COORD[0] - BALL_RADIUS - PAD_W * 2 > WIDTH * 2:
                    current_client = 2
                elif COORD[0] - PAD_W - BALL_RADIUS > WIDTH:
                    current_client = 1
            else:
                if COORD[0] + BALL_RADIUS + PAD_W < WIDTH:
                    current_client = 0
                elif COORD[0] + BALL_RADIUS + PAD_W * 2 > WIDTH * 2:
                    current_client = 2
                elif COORD[0] + BALL_RADIUS + PAD_W > WIDTH:
                    current_client = 1

            COORD[0] += INITIAL_SPEED * direction_x
            COORD[1] += INITIAL_SPEED * direction_y
            COORD[2] += INITIAL_SPEED * direction_x
            COORD[3] += INITIAL_SPEED * direction_y

            client_coord = list(COORD)
            if current_client != 0:
                client_coord[0] -= WIDTH * current_client + 1
                client_coord[2] -= WIDTH * current_client + 1
            s.sendto(bytes(json.dumps(client_coord), 'utf-8'), clients[current_client])
            time.sleep(0.1)

    except NameError:
        print('/n[Server stopped]')
        quit = True

s.close()
