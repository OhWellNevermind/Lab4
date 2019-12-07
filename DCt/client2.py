import json, lib
from tkinter import *
import socket, threading

PAD_SPEED = 0.5
RIGHT_PAD_SPEED = 0
HEIGHT = 500


shutdown = False
join = False

host = '192.168.1.12'
port = 9097

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

server = ('192.168.1.10', 9090)

root = Tk()
root.title("pong3")

c = lib.create_canvas(root)
c.pack()

BALL = lib.create_ball(c)
RIGHT_PAD = lib.create_right_pad(c)
lib.create_line_right(c)
lib.bounce(c)

playerName = 'Player3' #input('Enter you name:')




def receving(name, sock):
    while not shutdown:
        try:
            while True:
                lib.move_pads(c, {RIGHT_PAD: RIGHT_PAD_SPEED})
                coord, addr = sock.recvfrom(1024)
                lib.move_ball(c, BALL, json.loads(coord))
                s.sendto(bytes(json.dumps(c.coords(RIGHT_PAD)), 'utf-8'), server)
        except:
            pass


def movement_handler(event):
    global RIGHT_PAD_SPEED
    if event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED


def stop_pad(event):
    global RIGHT_PAD_SPEED
    if event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0


def main():
    global join
    if join == False:
        s.sendto(playerName.encode('utf-8'), server)
        join = True


c.bind("<KeyRelease>", stop_pad)
c.bind("<KeyPress>", movement_handler)
c.focus_set()
rT = threading.Thread(target=receving, args=('RecvThreads', s))
rT.start()

main()
root.mainloop()
