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

from Virus.Structures import VIDE, BLANC, NOIR

# Try PIL imports
pil = True
try:
    import PIL
except ImportError:
    pil = False
# =============================================================================
# Constants
def index(color):
    return {VIDE: 0, BLANC: 1, NOIR: 2}

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

    def __init__(self, height: int, width: int, *args, **kwargs):
        tk.Canvas.__init__(self, *args, bg= 'white', **kwargs)
        self.create_polygon = create_complex(self.create_polygon)
        self.board_height = height
        self.hexagon_width = width//2

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


    # -------------------------------------------------------------------------

# =============================================================================
class withoutPIL(HexagonalCanvas):

    def __init__(self, height: int, width: int, *args, **kwargs):
        HexagonalCanvas.__init__(self, height, width, *args, **kwargs)

    # -------------------------------------------------------------------------
    @create_complex
    def create_hexagon(self, width: int, x, y=None, angle = math.pi / 6):
        points = []
        for i in range(6):
            points.append(x+y*1j+cmath.rect(width, angle + i *(math.pi / 3)))
        self.create_polygon(*points, fill='white', outline='black')
        #@TODO return tuple of ints
    # -------------------------------------------------------------------------


# =============================================================================
if pil:
    class withPIL(HexagonalCanvas):
        def __init__(self, height: int, width: int, path=None, *args, **kwargs):
            HexagonalCanvas.__init__(self, height, width, *args, **kwargs)
            path = path if path else "..\\Sprites\\"
            self.hexagons = []
            for i in range(3):
                self.hexagons.append(load_image(path + "Hexagons %s" % i,
                                                               (width, width)))

        # ---------------------------------------------------------------------
        def display_Hexagon(self, i, j, color):
            #@TODO display one hexagon
            pass