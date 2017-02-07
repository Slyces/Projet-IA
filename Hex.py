# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille & Loizel Antoine'
__version__ = ''
__date__ = '26/01/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr & antoine.loizel@etu.u-bordeaux.fr'
__status__ = 'TD'
# =============================================================================
import socket
import threading
import tkinter as tk
from cmath import rect
from math import pi, cos, sqrt
from typing import Callable

from PIL import Image, ImageTk

import network
from Main import *


# =============================================================================
def load_image(path: str, resize: Tuple[int,int]=None) -> 'ImageTk.PhotoImage':
    image = Image.open(path)
    if resize:
        image.thumbnail(resize, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)

# =============================================================================
class Game(tk.Tk):
    def __init__(self, p: 'Plateau' = Plateau(11, 11), online: bool=True):
        # Init of tk window
        tk.Tk.__init__(self)
        self.title("You Lost The Game")

        # Attributes
        self.p = p
        self.width = 30
        self.player = 0
        self.__hexagons = {}
        self.__images = {}
        self.__tokens = []
        self.__victory = []
        self.finished = False

        # Init of tk canvas
        self.canvas = Workspace(self, p.hauteur, self.width)
        self.canvas.pack(expand=True, fill='both')
        self.canvas['height'] = self.p.hauteur * self.width * 1.7
        self.canvas['width'] = (2 * self.p.largeur + self.p.hauteur // 2) * 1.08 * self.width

        # Images init
        size = (self.width*2, self.width*2)
        for i in range(3):
            if i > 0:
                self.__images[i, '_'] = load_image("Sprites/Hexagon {} _.png".format(i), size)
            if i < 2:
                self.__tokens.append(load_image("Sprites/Token {}.png".format(i),(self.width,self.width)))
                self.__victory.append(load_image("Sprites/Victory {}.png".format(i+1)))
            self.__images[i] = load_image("Sprites/Hexagon {}.png".format(i), size)

        # Bindings
        self.bind('<Button-1>', self.on_click)
        self.bind('<space>', self.test)
        self.bind('<Key>', self.replay)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Networking
        if online:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((network.HOST, network.PORT))
            # self.socket.connect(('92.89.71.131', network.PORT))
            print(" Connected to the server ".center(80, "="))
            thread = threading.Thread(target=self.server_input, daemon=True)
            thread.start()
            self.token = 0

        print("=" * 30 + " Game Started " + "=" * 30)
        self.reset()
        self.display()
        self.mainloop()

    # -------------------------------------------------------------------------
    def server_input(self):
        rest = bytes()
        while True:
            try:
                # blocks
                (msgs, rest) = network.recv_msgs(self.socket, rest)
                for msg in msgs:
                    self.handle_requests(msg)
            except ConnectionError:
                print('Connection to server closed')
                self.socket.close()
                break

    # -------------------------------------------------------------------------
    def handle_requests(self, request: str):
        print("received request : ", request)
        eval(request)

    # -------------------------------------------------------------------------
    def reset(self):
        # Reset the Plateau
        self.finished = False
        self.p = Plateau(self.p.largeur, self.p.hauteur)
        self.p[0].valeur = NOIR
        self.p[-1].valeur = NOIR
        self.p[0, self.p.largeur - 1].valeur = BLANC
        self.p[self.p.hauteur - 1, 0].valeur = BLANC
        self.token = 0
        self.display()

    # -------------------------------------------------------------------------
    def check_victory(self):
        if (not self.p.jouables(NOIR)) or (not self.p.jouables(BLANC)):
            if self.p.jouables(NOIR):
                self.p.jouables(NOIR)[0].valeur = NOIR
            elif self.p.jouables(BLANC):
                self.p.jouables(BLANC)[0].valeur = BLANC
            self.display()
        if len(self.p.libres) > 0:
            self.after(1750, self.check_victory)
        else:
            self.on_game_end()

    # -------------------------------------------------------------------------
    def on_game_end(self):
        self.finished = True
        scores = [len(list(filter(lambda x: x.valeur == color, self.p.configuration))) for color in (BLANC, NOIR)]
        winner = 0 if scores[0] > scores[1] else 1
        self.canvas.create_image(self.winfo_width() * 0.5, self.winfo_height() * 0.5, image=self.__victory[winner])

    # -------------------------------------------------------------------------
    def replay(self, unused_ev):
        if self.finished:
            network.send_msg(self.socket, "replay")

    # ------------------------------------------------------------------------
    def on_closing(self):
        # Some code
        print("\n" + "=" * 31 + " Game Ended " + "=" * 31)
        self.destroy()

    # -------------------------------------------------------------------------
    def __getitem__(self, item):
        return self.__hexagons.__getitem__(item)

    # -------------------------------------------------------------------------
    def __setitem__(self, key, value):
        self.__hexagons.__setitem__(key, value)

    # -------------------------------------------------------------------------
    def play(self, i, j, color=None):
        color = [BLANC, NOIR][self.token] if color == None else color
        self.p[i, j].valeur = color
        for cell in self.p[i, j].voisins:
            if cell.valeur != VIDE and cell.valeur != color:
                cell.valeur = color
                self.display([self.p.pos2coord(cell.position)])
        self.display([(i,j)])
        self.check_victory()

    # -------------------------------------------------------------------------
    def test(self, ev):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()
        for (i, j), hex in self.__hexagons.items():
            if hex.enter(x, y):
                pass

    # -------------------------------------------------------------------------
    def on_click(self, ev):
        print("Player :", self.player, "Token :", self.token)
        for (i, j), hex in self.__hexagons.items():
            if hex.enter(ev.x, ev.y) and self.p[i, j].estAccessible([BLANC,NOIR][self.player]):
                network.send_msg(self.socket, "click {} {}".format(i, j))

    # -------------------------------------------------------------------------
    def display(self, coords = ()):
        if not coords:
            self.canvas.delete("all")
        else:
            for coord in coords:
                self.canvas.delete("%s,%s" % coord)
        if not coords:
            coords = [self.p.pos2coord(x.position) for x in self.p.configuration]
        self.canvas.create_image(self.width/2, self.width/1.8, image=self.__tokens[self.token])
        for i,j in coords:
            # i,j = self.p.pos2coord(x.position)
            p = self.canvas.coord2pixels((i, j),
               origin=((self.p.hauteur // 2) * 2 * self.width) * 1J + self.width)
            self[i, j] = Hexagon(self.width, int(p.real), int(p.imag))
            index = {VIDE: 0, BLANC: 1, NOIR: 2}[self.p[i, j].valeur]
            image = self.__images[index]
            self.canvas.create_image(p.real, p.imag, image=image, tags=("%s,%s") % (i, j))
            # if True :
            #     self.canvas.create_text(p.real, p.imag, text = str((i,j)))

# =============================================================================
def create_complex(create: Callable[[Tuple,Dict], None])\
                                                -> Callable[[Tuple,Dict], None]:
    " Décorateur pour permettre l'utilisation de complexes comme coordonnées "
    def decorator(*args, **kwargs):
        newargs = []
        for element in args:
            if type(element) is complex:
                newargs += [element.real] + [element.imag]
            else:
                newargs.append(element)
        create(*newargs, **kwargs)

    return decorator
# =============================================================================

class Workspace(tk.Canvas):
    def __init__(self, master, h, w, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, bg='#FFFFFF', **kwargs)
        self.create_polygon = create_complex(self.create_polygon)
        self.create_line = create_complex(self.create_line)
        self.board_height = h
        self.hexagon_width = w

    # -------------------------------------------------------------------------
    @create_complex
    def create_hexagon(self, width: int, x, y=None, angle: float = pi / 6):
        if y is None: x, y = x.real, x.imag
        points = []
        for i in range(6):
            points.append(x + y * 1j + rect(width, angle + i * (pi / 3)))
        self.create_polygon(*points, fill='white', outline='black')

    # -------------------------------------------------------------------------
    def coord2pixels(self, coords, origin: complex = 50 + 200 * 1J):
        v = [rect(self.hexagon_width, pi / 6 + i * (pi / 3)) for i in range(6)]
        k = v[-1] + v[-2] if (coords[0] - self.board_height // 2) <= 0 else v[0] + v[1]
        return origin + coords[1] * (v[0] + v[-1]) + abs(coords[0] - self.board_height // 2) * k
    # -------------------------------------------------------------------------

# =============================================================================
class Hexagon(object):
    id = 0

    def __init__(self, width: int, x: int, y: int, tag: str = ''):
        """ Stocke les coordonnées et dimensions d'un Hexagone"""
        self.tag = tag if tag else str(Hexagon.id)
        Hexagon.id += 1
        self.width = width
        self.x, self.y = x, y

    # -------------------------------------------------------------------------
    def enter(self, x: int, y: int):
        p = abs(self.x - x) + abs(self.y - y) * 1j
        if sqrt(p.real ** 2 + p.imag ** 2) > self.width:
            return False
        # |- - _ _
        # |        - - _ _
        # |     triangle   - - _ _
        # |                        - - _ _
        # |                               |
        # |                               |
        # |          Rectangle            | height
        # |                               |
        # | ___________width_____________ |
        width = self.width * cos(pi / 6)
        height = sqrt(self.width ** 2 - width ** 2)
        # First : rectangle check
        if p.real < width and p.imag < height:
            return True
        # Second : triangle check
        p0 = 0 + height * 1j
        p1 = width + height * 1j
        p2 = 0 + self.width * 1j
        Area = 0.5 * (-p1.imag * p2.real + p0.imag * (-p1.real + p2.real)
                      + p0.real * (p1.imag - p2.imag) + p1.real * p2.imag)
        s = 1 / (2 * Area) * (p0.imag * p2.real - p0.real * p2.imag +
                    (p2.imag - p0.imag) * p.real + (p0.real - p2.real) * p.imag)
        t = 1 / (2 * Area) * (p0.real * p1.imag - p0.imag * p1.real +
                    (p0.imag - p1.imag) * p.real + (p1.real - p0.real) * p.imag)

        if s > 0 and t > 0 and 1 - s - t > 0:
            return True
        return False
        # -------------------------------------------------------------------------


if __name__ == '__main__':
    game = Game()