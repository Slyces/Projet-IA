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
import cmath, math, tkinter as tk

from Interface.Hexagons import Hexagon
from Virus.Structures import VIDE, BLANC, NOIR

# Try PIL imports
pil = True
try:
    from PIL import Image, ImageTk
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
    def load_image(path: str, resize =None):
        image = Image.open(path)
        if resize:
            image.thumbnail(resize, Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

# =============================================================================
# PIL available
class HexagonalCanvas(tk.Canvas):

    def __init__(self, master, height: int, hexwidth: int, path =None,**kwargs):
        tk.Canvas.__init__(self, master, bg= 'white', **kwargs)
        self.create_polygon = create_complex(self.create_polygon)
        self.board_height = height
        self.hexagon_width = hexwidth//2
        self.hexagons_dict = {}

    # -------------------------------------------------------------------------
    def coord2pixels(self, coords, origin: complex = None):
        origin = origin if origin else ((self.board_height // 2) * 2 *
                            self.hexagon_width + 5) * 1J + self.hexagon_width
        v = [cmath.rect(self.hexagon_width, math.pi / 6 + i * (math.pi / 3))
                                                             for i in range(6)]
        k = v[-1] + v[-2] if (coords[0] - self.board_height // 2) <= 0 else\
                                                                    v[0] + v[1]
        p = origin + coords[1] * (v[0] + v[-1]) + abs(coords[0] -
                                                   self.board_height // 2) * k
        return int(p.real), int(p.imag)
    # -------------------------------------------------------------------------
    def hexagon(self, x, y):
        """ Returns the hexagon in position < x ; y > """
        for (i,j),hex in self.hexagons_dict.items():
            if hex.enter(x, y):
                return i,j
    # -------------------------------------------------------------------------

# =============================================================================
class CanvasWithoutPIL(HexagonalCanvas):

    def __init__(self, master, height: int, hexwidth: int, **kwargs):
        HexagonalCanvas.__init__(self, master, height, hexwidth, **kwargs)
        self.colors = {VIDE: '#C0C0C0', BLEU: '#3D59AB', ROUGE: '#B22222'}
        self.outlines = {VIDE: '#000000', BLEU: '#191970', ROUGE: '#800000'}
        self.nmax = 100

    # -------------------------------------------------------------------------
    @create_complex
    def create_hexagon(self, x, y=None, hexwidth: (int, tuple)= 20, **kwargs):
        if type(x) is complex : x,y = x.real, y.imag
        if isinstance(hexwidth, (int, float)): hexwidth = [hexwidth for i in range(6)]
        points = []
        for i in range(6):
            points.append(x+y*1j+cmath.rect(hexwidth[i], math.pi/6+i*(math.pi / 3)))
        return self.create_polygon(*points,**kwargs)

    # -------------------------------------------------------------------------
    def display_hexagon(self, i, j, color):
        if (i,j) in self.hexagons_dict: self.hexagons_dict.pop((i,j))
        x, y = [int(k) for k in self.coord2pixels((i, j))]
        self.hexagons_dict[i, j] = Hexagon(self.hexagon_width, x, y)
        self.create_hexagon(x, y, fill=self.colors[color], width= 3,
                            outline= self.outlines[color],
                             activewidth=3, hexwidth=self.hexagon_width*0.9,
                            activeoutline='black', tag='%s,%s' % (i,j))

    # -------------------------------------------------------------------------
    def animate(self, i, j, color, _from=None, n=None):
        _from = VIDE if _from is None else _from
        self.delete('%s,%s' % (i,j))
        n = self.nmax if n is None else n
        ocolor = color
        color = color if n < 0 else _from
        x, y = self.coord2pixels((i, j))
        self.hexagons_dict[i, j] = Hexagon(self.hexagon_width, x, y)
        widths = [self.hexagon_width *0.9 if i in (1,4) else
                          self.hexagon_width*(abs(n)/self.nmax)*0.9 for i in range(6)]
        self.create_hexagon(x, y, fill=self.colors[color], width=3 if color != VIDE else 0,
                            outline=self.outlines[color],
                            activewidth=3, hexwidth= widths,
                            activeoutline='black', tag='%s,%s' % (i, j))
        self.tag_lower('%s,%s' % (i,j))
        n -= 1
        if n > -self.nmax:
            self.master.after(4, lambda args=(i, j, ocolor, _from, n): self.animate(*args))

# ============================================================================
class CanvasWithPIL(HexagonalCanvas):
    def __init__(self, master, height: int, hexwidth: int, path=None, *args,
                 **kwargs):
        HexagonalCanvas.__init__(self, master, height, hexwidth, **kwargs)
        path = path if path else "..\\Sprites\\"
        self.hexagonsImg = []
        for i in range(3):
            self.hexagonsImg.append(load_image(path + "Hexagon %s.png" % i,
                                                    (hexwidth, hexwidth)))
        # self.active = load_image(path + "Hexagon 0 active.png",
        #                                              (hexwidth, hexwidth))

    # -------------------------------------------------------------------------
    def display_hexagon(self, i, j, color):
        x,y =  self.coord2pixels((i,j))
        self.hexagons_dict[i,j] = Hexagon(self.hexagon_width, x, y)
        self.create_image(x, y, image=self.hexagonsImg[index(color)],
                          tag='%s,%s' % (i,j))