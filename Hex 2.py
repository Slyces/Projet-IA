# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '19/01/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
import tkinter as tk
from cmath import rect
from math import pi, cos, sqrt

from Main import *


class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("You Lost The Game")
        canvas = Workspace(self)
        canvas.pack(expand=True, fill='both')

        width = 25

        p = Plateau(7,7)
        canvas.draw_board(width, p.h, p.keys())

        self.mainloop()

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

class Workspace(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, bg='#E7E7E7', **kwargs)
        self.bind('<Button-1>',lambda ev : self.create_hexagon(60, ev.x, ev.y))
        self.create_polygon = create_complex(self.create_polygon)
        self.create_line = create_complex(self.create_line)

        self.hexagons = []
        self.bind('<Motion>', self.check)

    @create_complex
    def create_hexagon(self, width: int, x, y=None, angle: float = pi/6):
        if y is None: x,y = x.real, x.imag
        points = []
        for i in range(6):
            points.append(x + y*1j + rect(width, angle + i*(pi/3)))
        self.create_polygon(*points, fill='white', outline='black')
        self.hexagons.append(Hexagon(width, x, y))

    def draw_board(self, width, h, coords, angle: float = pi/6):
        print(coords)
        v = [rect(width, angle + i*(pi/3)) for i in range(6)]
        p0 = 120 + 160*1J
        for (i,j) in coords:
            print(i - h//2, j)
            k = v[-1]+v[-2] if (i-h//2) <= 0 else v[0] + v[1]
            p = p0 + j*(v[0]+v[-1]) + abs(i-h//2)*k

            self.create_hexagon(width, p, angle=angle)

    def check(self, ev):
        entered = False
        for hex in self.hexagons:
            entered = entered or hex.enter(ev.x, ev.y)
        if entered:
            print("Entered")
        else :
            print('')

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