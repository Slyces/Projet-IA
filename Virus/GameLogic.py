# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '08/02/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
from Virus.Structures import *
# =============================================================================
class Game(Plateau):
    def __init__(self, height: int= 5, width: int= 5):
        Plateau.__init__(self, height, width)
        self.player = 0
        self.token = 0
        self.finished = False

    # -------------------------------------------------------------------------
    @property
    def color(self):
        return [BLANC, NOIR][self.player]

    # -------------------------------------------------------------------------
    def reset(self):
        self.player, self.token = 0, 0
        Plateau.__init__(self, self.largeur, self.hauteur)
        self.finished = False

    # -------------------------------------------------------------------------
    def play(self, i, j, color= None, out= False):
        """ Plays in position <i,j> as player <color>. Output yields coords """
        color = color if color else self.color
        if self[i,j].estAccessible(color) and self.player == self.token:
            if out: yield (i, j), self[i,j].valeur
            self[i,j].valeur = color
            for voisin in self[i,j].voisins:
                if voisin.valeur == Case.reverse(color):
                    if out: yield self.pos2coord(voisin.position), voisin.valeur
                    voisin.valeur = color

    # -------------------------------------------------------------------------
    def check_state(self):
        return True in [self.jouables(color) == 0 for color in (BLANC, NOIR)]
