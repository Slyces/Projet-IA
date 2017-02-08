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
from math import sqrt, cos, pi
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