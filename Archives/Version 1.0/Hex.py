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
import tkinter as tk
from cmath import rect
from math import pi, cos, sqrt

from Main import *
from PIL import Image, ImageTk


# =============================================================================

class Game(tk.Tk):
    def __init__(self, p: 'Plateau' = Plateau(5, 7)):
        tk.Tk.__init__(self)
        self.title("You Lost The Game")
        self.p = p
        self.lastp = self.p
        self.width = 40
        self.canvas = Workspace(self, p.hauteur, self.width)
        self.canvas.pack(expand=True, fill='both')
        self.__hexagons = {}
        self.__images = [None for i in range(3)]

        self.player = NOIR

        # Placer les pions
        self.p[0].valeur = NOIR
        self.p[-1].valeur = NOIR
        self.p[0,self.p.largeur-1].valeur = BLANC
        self.p[self.p.hauteur-1,0].valeur = BLANC

        self.__originals = [None] * 3

        for i in range(3):
            maxsize = (2*self.width, 2*self.width)
            image = Image.open("Hexagon {}.png".format(i))
            self.__originals[i] = image.copy()
            image.thumbnail(maxsize, Image.ANTIALIAS)
            self.__images[i] = ImageTk.PhotoImage(image)

        self.canvas['height'] = self.p.hauteur*self.width*1.7
        self.canvas['width'] = (2*self.p.largeur + self.p.hauteur//2 )*1.08*self.width
        self.bind('<Button-1>', self.on_click)
        # self.bind('<Button-3>', self.on_right_click)
        self.bind('<space>', self.test)
        print("=" * 60)
        self.display()
        self.mainloop()

    def __getitem__(self, item):
        return self.__hexagons.__getitem__(item)

    def __setitem__(self, key, value):
        self.__hexagons.__setitem__(key, value)

    def on_right_click(self, ev):
        self.on_click(ev, BLANC)

    def test(self, ev):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()
        for (i,j),hex in self.__hexagons.items():
            if hex.enter(x, y):
                print("En toi, forte est la force : {}".format(self.p[i,j].force(BLANC)))
        # print([x.force(BLANC) for x in self.p.jouablesTriees(BLANC)])

    def on_click(self, ev):
        color = self.player
        for (i,j),hex in self.__hexagons.items():
            if hex.enter(ev.x, ev.y) and self.p[i,j].estAccessible(color):
                # self.animate(i, j, self.p[i,j].valeur, color)
                self.p[i,j].valeur = color
                for cell in self.p[i,j].voisins:
                    if cell.valeur != VIDE and cell.valeur != color:
                        # self.animate(i, j, self.p[self.p.pos2coord(cell.position)].valeur, color)
                        cell.valeur = color
                self.player = NOIR if self.player == BLANC else BLANC
                self.display()

    def display(self):
        self.canvas.delete("all")

        for (i,j) in self.p.keys():
            p = self.canvas.coord2pixels((i,j),
                        origin= ((self.p.hauteur//2)*2*self.width)*1J + self.width)
            self[i,j] = Hexagon(self.width, int(p.real), int(p.imag))
            img = self.__images[{VIDE: 0, BLANC: 1, NOIR: 2}[self.p[i,j].valeur]]
            self.canvas.create_image(p.real, p.imag, image=img, tag="%s,%s" % (i,j))
            self.p[i,j].estAccessible(BLANC) and self.p[i,j].estAccessible(NOIR)
            # if True :
            #     self.canvas.create_text(p.real, p.imag, text = str((i,j)))

    # def animate(self, i, j, _from=VIDE, _to=BLANC, n=50):
    #     p = self.canvas.coord2pixels((i, j),
    #             origin=((self.p.hauteur // 2) * 2 * self.width) * 1J + self.width)
    #     k = {VIDE: 0, BLANC: 1, NOIR: 2}[_from if n >= 0 else _to]
    #     self.canvas.delete("%s,%s" % (i,j))
    #     print("Call number", n)
    #     img = self.__originals[k].copy()
    #     img.thumbnail(((abs(n)/50)*2*self.width + 1,self.width*2), Image.ANTIALIAS)
    #     I = ImageTk.PhotoImage(img)
    #     self.canvas.create_image(p.real, p.imag, image=I, tag="%s,%s" % (i,j))
    #     # n -= 1
    #     # if n > -50 :
    #     #     self.after(5, lambda h=i, l=j, m=_from, o=_to, p=n: self.animate(h,l,m,o,p))


# =============================================================================

def create_complex(create):
    def decorator(*args, **kwargs):
        newargs = []
        for element in args:
            if type(element) is complex:
                newargs += [element.real] + [element.imag]
            else :
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

    @create_complex
    def create_hexagon(self, width: int, x, y=None, angle: float = pi/6):
        if y is None: x,y = x.real, x.imag
        points = []
        for i in range(6):
            points.append(x + y*1j + rect(width, angle + i*(pi/3)))
        self.create_polygon(*points, fill='white', outline='black')

    def coord2pixels(self, coords, origin:complex = 50 + 200 * 1J):
        v = [rect(self.hexagon_width, pi/6 + i * (pi / 3)) for i in range(6)]
        k = v[-1] + v[-2] if (coords[0] - self.board_height // 2) <= 0 else v[0] + v[1]
        return origin + coords[1]*(v[0]+v[-1]) + abs(coords[0]-self.board_height//2)*k

# =============================================================================

class Hexagon(object):
    id = 0
    def __init__(self, width: int, x:int, y:int, tag:str = ''):
        self.tag = tag if tag else str(Hexagon.id)
        Hexagon.id += 1
        self.width = width
        self.x, self.y = x, y

    def enter(self, x:int, y:int):
        p = abs(self.x - x) + abs(self.y - y) * 1j
        if sqrt(p.real**2 +p.imag**2) > self.width:
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
        width = self.width * cos(pi/6)
        height = sqrt(self.width**2 - width**2)
        # First : rectangle check
        if p.real < width and p.imag < height:
            return True
        # Second : triangle check
        p0 = 0 + height*1j ; p1 = width + height*1j ; p2 = 0 + self.width*1j
        Area = 0.5 * (-p1.imag * p2.real + p0.imag * (-p1.real + p2.real) + p0.real * (p1.imag - p2.imag) + p1.real * p2.imag)
        s = 1 / (2 * Area) * (p0.imag * p2.real - p0.real * p2.imag + (p2.imag - p0.imag) * p.real + (p0.real - p2.real) * p.imag)
        t = 1 / (2 * Area) * (p0.real * p1.imag - p0.imag * p1.real + (p0.imag - p1.imag) * p.real + (p1.real - p0.real) * p.imag)

        if s > 0 and t > 0 and 1 - s - t > 0:
            return True
        return False

if __name__ == '__main__':
    game = Game()