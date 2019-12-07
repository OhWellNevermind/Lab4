import json, lib
from tkinter import *
import socket, threading

shutdown = False
join = False

host = '192.168.1.13'
port = 9096

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

server = ('192.168.1.10', 9090)

root = Tk()
root.title("pong2")

c = lib.create_canvas(root)
c.pack()
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

BALL = lib.create_ball(c)
lib.create_line_center(c)

playerName = 'Player2' #input('Enter you name:')


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                coord, addr = sock.recvfrom(1024)
                lib.move_ball(c, BALL, json.loads(coord))
                data = [0, 0, 0, 0]
                s.sendto(bytes(json.dumps(data), 'utf-8'), server)
        except:
            pass


def main():
    global join
    if join == False:
        s.sendto(playerName.encode('utf-8'), server)
        join = True


rT = threading.Thread(target=receving, args=('RecvThreads', s))
rT.start()

main()
root.mainloop()
