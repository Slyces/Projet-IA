# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille & Antoine Loizel'
__version__ = ''
__date__ = '08/02/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__email__ += ' & ' + 'antoine.loizel@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
# Imports
import cmath
import math
import tkinter as tk

from Interface.Hexagons import Hexagon
from Virus.Structures import VIDE, BLANC, NOIR

# Try PIL imports
pil = True
try:
    import PIL
except ImportError:
    pil = False
# =============================================================================
# Constants
BLEU, ROUGE = BLANC, NOIR
def index(color):
    return {VIDE: 0, BLEU: 1, ROUGE: 2}[color]
# =============================================================================
def create_complex(create):
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
if pil:
    def load_image(path: str, resize):
        image = PIL.Image.open(path)
        if resize:
            image.thumbnail(resize, PIL.Image.ANTIALIAS)
        return PIL.ImageTk.PhotoImage(image)

# =============================================================================
# PIL available
class HexagonalCanvas(tk.Canvas):

    def __init__(self, master, height: int, hexwidth: int, **kwargs):
        tk.Canvas.__init__(self, master, bg= 'white', **kwargs)
        self.create_polygon = create_complex(self.create_polygon)
        self.board_height = height
        self.hexagon_width = hexwidth//2
        self.__hexagons = {}

    # -------------------------------------------------------------------------
    def coord2pixels(self, coords, origin: complex = None):
        origin = origin if origin else ((self.board_height // 2) * 2 *
                                self.hexagon_width) * 1J + self.hexagon_width
        v = [cmath.rect(self.hexagon_width, math.pi / 6 + i * (math.pi / 3))
                                                             for i in range(6)]
        k = v[-1] + v[-2] if (coords[0] - self.board_height // 2) <= 0 else\
                                                                    v[0] + v[1]
        p = origin + coords[1] * (v[0] + v[-1]) + abs(coords[0] -
                                                   self.board_height // 2) * k
        return p.real, p.imag
    # -------------------------------------------------------------------------
    def hexagon(self, x, y):
        """ Returns the hexagon in position < x ; y > """
        for (i,j),hex in self.__hexagons.items():
            if hex.enter(x, y):
                return i,j
    # -------------------------------------------------------------------------

# =============================================================================
class withoutPIL(HexagonalCanvas):

    def __init__(self, master, height: int, hexwidth: int, **kwargs):
        HexagonalCanvas.__init__(self, master, height, hexwidth, **kwargs)
        self.colors = {VIDE: '##EAEAEA', BLEU: '#3D59AB', ROUGE: '#B22222'}
        self.outlines = {VIDE: '#696969', BLEU: '#191970', ROUGE: '#800000'}

    # -------------------------------------------------------------------------
    @create_complex
    def create_hexagon(self, width: int, x, y=None, **kwargs):
        points = []
        for i in range(6):
            points.append(x+y*1j+cmath.rect(width, math.pi/6+i*(math.pi / 3)))
        return self.create_polygon(*points,**kwargs)

    # -------------------------------------------------------------------------
    def display_hexagon(self, i, j, color):
        x, y = [int(k) for k in self.coord2pixels((i, j))]
        self.__hexagons[i, j] = Hexagon(self.hexagon_width, x, y)
        self.create_hexagon(x, y, fill=self.colors[color], width= 3,
                            outlines=self.outlines[color], activewidth=6,
                            activeoutline='black', tag='%s,%s' % (i,j))

# =============================================================================
if pil:
    class withPIL(HexagonalCanvas):
        def __init__(self, master, height: int, hexwidth: int, path=None, *args,
                     **kwargs):
            HexagonalCanvas.__init__(self, master, height, hexwidth, **kwargs)
            path = path if path else "..\\Sprites\\"
            self.hexagons = []
            for i in range(3):
                self.hexagons.append(load_image(path + "Hexagons %s" % i,
                                                               (width, width)))
            self.active = load_image(path + "Hexagon 0 active", (width, width))

        # ---------------------------------------------------------------------
        def display_hexagon(self, i, j, color):
            x,y = [int(k) for k in self.coord2pixels((i,j))]
            self.__hexagons[i,j] = Hexagon(self.hexagon_width, x, y)
            self.create_image(x, y, image=self.hexagons[index(color)])

if pil :
    HexCanvas = withPIL
else:
    HexCanvas = withoutPIL